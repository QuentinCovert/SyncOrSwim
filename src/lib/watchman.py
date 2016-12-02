import os
import json
import socket

class Watchman:
    def __init__(self):
        self.sock_path = None

    def getSocketLocation(self):
        # Use command line to retrieve socket location
        # and parse it from the JSON formatted output
        sock_info = os.popen('watchman get-sockname').read()
        sock_path = json.loads(sock_info)['sockname']
        return sock_path

    # This now sends and receives separately
    # Sends the json message of the one (1) parameter
    # Receives a response if no parameter is set
    def socketCommunicate(self, msgObj = None):
        if self.sock_path is None:
            self.sock_path = self.getSocketLocation()

        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.setblocking(0)
        s.connect(self.sock_path)

        # Sends the request
        # Only run if sending a message
        if not (msgObj is None):
            # Convert msgObj to JSON and send
            # Must be utf-8 encoded
            jsonObj = json.dumps(msgObj) + '\n'
            s.send(jsonObj.encode())

        # Receives the response
        # Only run if not sending a message
        data = None
        if (msgObj is None):
            data = s.recv(1024)

        s.close()

        # Only run if the message received is non-empty
        if not (data is None):
            response = data.decode()

            # Check for error in response
            responseObj = json.loads(response)
            if 'error' in responseObj:
                print('ERROR: ' + responseObj['error'])

            # Return the JSON formatted response
            return response
        else:
            print('This data\'s empty. YEET!')      # For debugging.
            return None

    def checkVersion(self):
        response = self.socketCommunicate(['version'])
        version = json.loads(response)['version']
        return version

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

    def subscribe(self, path_to_root, subscription_name, ignore_files_list = None):
        # Watch anything that is a file (f) or directory (d) in this root directory
        expression = {'expression': ['allof', ['anyof', ['type', 'f'], ['type', 'd']]]}

        # Add ignored files to the filter
        # only if this is given
        if not (ignored_files_list is None):
            ignore_expression = self.ignoredFilesToExpression(ignore_files_list)
            if not (ignore_expression is None):
                expression['expression'].append(ignore_expression)

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

    def since(self, path_to_root, clock_spec, ignore_files_list = None):
        sinceObj = {'since': clock_spec, 'expression': ['allof', ['anyof', ['type', 'f'], ['type', 'd']]]}

        if not (ignore_files_list is None):
            ignore_expression = self.ignoredFilesToExpression(ignore_files_list)
            if not (ignore_expression is None):
                sinceObj['expression'].append(ignore_expression)


        sinceRequest = ['query', path_to_root, sinceObj]

        response = self.socketCommunicate(sinceRequest)
        result = json.loads(response)
        return result
