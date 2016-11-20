import os
import json
import socket

class Watchman:

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

    def subscribe(self, path_to_root, subscription_name, ignored_files_list = None):
        # Watch anything that is a file (f) or directory (d) in this root directory
        expression = {'expression': ['anyof', ['type', 'f'], ['type', 'd']]}

        # Add ignored files to the filter
        # If they are specified
        if not (ignored_files_list is None or type(ignored_files_list) != type([])):
            expression['expression'].append(['not', ignored_files_list])

        subRequest = ['subscribe', path_to_root, subscription_name, expression]

        response = self.socketCommunicate(subRequest)
        print(response)
        return response

    def unsubscribe(self, path_to_root, subscription_name):
        unsubRequest = ['unsubscribe', path_to_root, subscription_name]
        response = self.socketCommunicate(unsubRequest)
        print(response)
        return response

    def clock(self, path_to_root):
        clockRequest = ['clock', path_to_root]
        response = self.socketCommunicate(clockRequest)
        print(response)
        return response

    def since(self, path_to_root, subscription_name, clockSpec):
        sinceObj = {'since': clockSpec}
        sinceRequest = ['query', path_to_root, sinceObj]
        response = self.socketCommunicate(sinceRequest)
        print(response)
        return response
