import os
import json
import socket
import time

class Watchman:
    def __init__(self):
        self.sock_path = None

    def getSocketLocation(self):
        # Use command line to retrieve socket location
        # and parse it from the JSON formatted output
        sock_info = os.popen('watchman get-sockname').read()
        sock_path = json.loads(sock_info)['sockname']
        return sock_path

    def socketCommunicate(self, msgObj):
        if self.sock_path is None:
            self.sock_path = self.getSocketLocation()

        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.sock_path)

        # Convert msgObj to JSON and send
        # Must be utf-8 encoded
        jsonObj = json.dumps(msgObj) + '\n'
        s.send(jsonObj.encode())
        data = s.recv(1024)
        s.close

        response = data.decode()
        # Check for error in response
        responseObj = json.loads(response)
        if 'error' in responseObj:
            print('ERROR: ' + responseObj['error'])

        # Return the JSON formatted response
        return response

    def checkVersion(self):
        response = self.socketCommunicate(['version'])
        version = json.loads(response)['version']
        return version

    def fileListToExpression(self, files_list):
        # Pass in a list of files/directories (string)
        # relative to the root directory
        # to convert into Watchman's expression syntax
        # Can also support wildcard character (*)
        if type(ignored_files_list) == type([]):
            expression = []
            for item in files_list:
                expression.append(['match', item, 'wholename'])

            return expression
        else:
            return None

    def subscribe(self, path_to_root, subscription_name, ignored_files_list = None):
        # Watch anything that is a file (f) or directory (d) in this root directory
        expression = {'expression': ['anyof', ['type', 'f'], ['type', 'd']]}

        # Add ignored files to the filter
        # only if this is given
        if not (ignored_files_list is None):
            ignored_expression = self.fileListToExpression(ignored_files_list)
            expression['expression'].append(['not', ignored_expression])

        subRequest = ['subscribe', path_to_root, subscription_name, expression]

        response = self.socketCommunicate(subRequest)
        subResponse = json.loads(response)
        return subResponse

    def unsubscribe(self, path_to_root, subscription_name):
        unsubRequest = ['unsubscribe', path_to_root, subscription_name]
        response = self.socketCommunicate(unsubRequest)
        unsubResponse = json.loads(response)
        return unsubResponse

    def clock(self, path_to_root):
        # Returns current clock_spec for the watched root
        clockRequest = ['clock', path_to_root]
        response = self.socketCommunicate(clockRequest)
        clock = json.loads(response)['clock']
        return clock

    # TODO: Implement ignored_files_list as optional argument here too.
    def since(self, path_to_root, clock_spec, ignored_files_list = None):
        sinceObj = {'since': clock_spec}
        sinceRequest = ['query', path_to_root, sinceObj]
        response = self.socketCommunicate(sinceRequest)
        result = json.loads(response)
        return result
