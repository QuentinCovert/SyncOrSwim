import os
import json
import socket

class Watchman:
    def __init__(self):
        # To be defined later.
        self.default_trigger_command = ''

    def getSocketLocation(self):
        # Use command line to retrieve socket location
        # and parse it from the JSON formatted output
        sock_info = os.popen('watchman get-sockname').read()
        sock_path = json.loads(sock_info)['sockname']
        return sock_path

    def socketCommunicate(self, msgObj):
        sock_path = self.getSocketLocation()
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(sock_path)

        # Convert msgObj to JSON and send
        # Must be utf-8 encoded
        jsonObj = json.dumps(msgObj) + '\n'
        s.send(jsonObj.encode())
        data = s.recv(1024)
        s.close
        return data.decode()

    def checkVersion(self):
        response = self.socketCommunicate(['version'])
        version = json.loads(response)['version']
        return version

    def subscribe(self, path_to_root, trigger_name, ignored_files):
        expression = [
            ['anyof', ['type', 'f'], ['type', 'd']]
        ]

        #TODO: Add ignored files filter
        #TODO: Add command to run on trigger
        command = ['']

    def unsubscribe(self, path_to_root, trigger_name):
        unsubRequest = ['unsubscribe', path_to_root, trigger_name]
        response = self.socketCommunicate(unsubRequest)
        print(response)

class Trigger:
    __init__(self, name, expression, command):
        self.name = name
        self.expression = expression
        self.command = command
