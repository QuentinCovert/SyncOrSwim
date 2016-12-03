import os
import json
import socket
import select
from lib.FileSystemObject import FileSystemObject, File, Directory
from lib.Crypto import Crypto
from lib.remote import Remote
import lib.database
from datetime import datetime
import random
from PyQt4.QtCore import qDebug

class Watchman:
    def __init__(self, rootPath, root, crypto, remote, settings):
        self.sock_addr = Watchman.getSocketLocation()
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.rootPath = rootPath
        self.rootDirectory = root
        self.crypto = crypto
        self.remote = remote
        self.settings = settings
        try:
            self.sock.connect(self.sock_addr)
        except socket.error as msg:
            print(msg)

    def getSocketLocation():
        # Use command line to retrieve socket location
        # and parse it from the JSON formatted output
        sock_info = os.popen('watchman get-sockname').read()
        sock_path = json.loads(sock_info)['sockname']
        return sock_path

    # This now sends and receives separately
    # Sends the json message of the one (1) parameter
    # Receives a response if no parameter is set
    def socketCommunicate(self, msgObj):

        # Sends the request
        # Only run if sending a message

        # Convert msgObj to JSON and send
        # Must be utf-8 encoded
        jsonObj = json.dumps(msgObj) + '\n'
        writeList = [self.sock]
        read, write, err = select.select([], writeList, [])
        while not write:
            read, write, err = select.select([], writeList, [])
        self.sock.send(jsonObj.encode())

    def checkVersion(self):
        self.socketCommunicate(['version'])

    def fileListToExpression(self, files_list):
        # Pass in a list of files/directories (string)
        # relative to the root directory
        # to convert into Watchman's expression syntax
        # Can also support wildcard character (*)
        if type(files_list) == type([]):
            expression = []
            for item in files_list:
                expression.append(['match', item, 'wholename'])

            return expression
        else:
            return None

    def ignoredFilesToExpression(self, ignored_files_list):
        # In order to ignore every "*.extension" on every level/depth of the directory
        # You need to input as "**/*.extension"
        # Otherwise, it just applies on the immediate directory only
        file_expressions = self.fileListToExpression(ignored_files_list)
        if not (file_expressions is None):
            ignore_expression = ['not']
            ignore_expression.extend(file_expressions)
            return ignore_expression
        else:
            return None

    def subscribe(self):
        # Watch anything that is a file (f) or directory (d) in this root directory
        expression = {'expression': ['allof', ['type', 'f']]}

        # Add ignored files to the filter
        # only if this is given
        #if not (ignored_files_list is None):
        #    ignore_expression = self.ignoredFilesToExpression(ignore_files_list)
        #    if not (ignore_expression is None):
        #        expression['expression'].append(ignore_expression)

        subRequest = ['subscribe', self.rootPath, 'sub1', expression]

        self.socketCommunicate(subRequest)

    def unsubscribe(self, path_to_root, subscription_name):
        unsubRequest = ['unsubscribe', path_to_root, subscription_name]
        self.socketCommunicate(unsubRequest)

    def clock(self, path_to_root):
        # Returns current clock_spec for the watched root
        clockRequest = ['clock', path_to_root]
        self.socketCommunicate(clockRequest)

    def since(self, path_to_root, clock_spec, ignore_files_list = None):
        sinceObj = {'since': clock_spec, 'expression': ['allof', ['anyof', ['type', 'f'], ['type', 'd']]]}

        if not (ignore_files_list is None):
            ignore_expression = self.ignoredFilesToExpression(ignore_files_list)
            if not (ignore_expression is None):
                sinceObj['expression'].append(ignore_expression)


        sinceRequest = ['query', path_to_root, sinceObj]

        self.socketCommunicate(sinceRequest)

    def parse(self):
        #check if there is a new message
        qDebug("Started parse.")
        readList = [self.sock]
        read, write, err = select.select(readList, [], [], 0)
        while read:
            qDebug("Entered read loop.")
            #parse the message and perform task
            readSock = read.pop()
            data = readSock.recv(1024)
            jsonObj = json.loads(data.decode("utf-8"))
            try:
                files = jsonObj["files"]
            except Exception as e:
                qDebug("Key error - disregard")
                return
            for file in files:
                name = file["name"]
                new = file["new"]
                exists = file["exists"]

                if new == True:
                    qDebug("New file added.")
                    #create file object
                    randomName = random.randint(1, 1000000)
                    #check if random name was already used
                    while os.path.exists(self.settings.remotePath + str(randomName)):
                        randomName = random.randint(1, 1000000)
                    modTime = datetime.fromtimestamp(os.path.getmtime(self.rootPath + name))
                    myFile = File(name, modTime, 0, 1, datetime.today(), randomName)
                    lib.database.store(myFile)
                    self.crypto.encrypt(myFile)
                    self.remote.push(myFile)
                elif exists == True:
                    qDebug("Modified file.")
                    #encrypt and upload
                    fileObject = self.rootDirectory.retrieve(name)
                    self.crypto.encrypt(fileObject)
                    self.remote.push(fileObject)
                    fileObject.lastModified = os.path.getmtime(self.rootPath + name)
                    lib.database.store(fileObject)
                else:
                    qDebug("Deleted file.")
                    #file was deleted
                    fileObject = self.rootDirectory.retrieve(name)
                    fileObject.deleted = True
                    lib.database.store(fileObject)
            read, write, err = select.select(readList, [], [], 0)
        qDebug("Exiting busy loop")

