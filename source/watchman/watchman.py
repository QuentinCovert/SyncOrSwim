import os
import json
import socket

class Watchman:
    def __init__(self):
        self.sock_path = getSocketLocation()

    def getSocketLocation():
        # Use command line to retrieve socket location
        # and parse it from the JSON formatted output
        sock_info = os.open('watchman get-sockname').read()
        sock_path = json.loads(sock_info)['sockname']
        return sock_path

    def socketCommunicate(self, msgObj):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.sock_path)

        # Convert msgObj to JSON and send
        # Must be utf-8 encoded
        msgJson = json.dumps(jsonObj) + '\n'
        s.send(msgJson.encode())

        data = s.recv(1024)
        s.close
        return data.decode()


    def checkVersion(self):
        versionReq = ['version']
        response = self.socketCommunicate(versionReq)
        print(response)
        return response

    def subscribe(root_directory):
        return False

    def unsubscribe(root_directory):
        return False
