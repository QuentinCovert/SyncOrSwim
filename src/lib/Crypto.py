from cryptography.fernet import Fernet
import os
import base64
import lib.Settings
from lib.FileSystemObject import FileSystemObject, File, Directory


class Crypto:

    def __init__(self, settings):
        self.key = settings.key
        self.fernet = Fernet(self.key)
        self.GlobalSettings = settings
        self.MINIMUM_SPLIT_SIZE = self.GlobalSettings.minimum_split_size
        self.BLOCK_SIZE = self.GlobalSettings.block_size

    def generateKey():
        return Fernet.generate_key()

    def encrypt(self, file):
        #TODO: config class operation
        #TODO: test file size. If over a certain size use split method, otherwise just encrypt
        rootPath = self.GlobalSettings.rootPath
        encryptedFolder = self.GlobalSettings.encryptedFolder
        fileSize = os.path.getsize(rootPath + file.path)

        if fileSize < self.MINIMUM_SPLIT_SIZE:
            # encrypt in one file
            inFile = open(rootPath + file.path, "rb")
            outFile = open(encryptedFolder + file.encryptedFilePath, "wb")
            outData = self.fernet.encrypt(inFile.read())
            outDataBin = base64.urlsafe_b64decode(outData)
            outFile.write(outDataBin)
            inFile.close()
            outFile.close()

        else:
            # encrypt in chunks
            chunkIndex = 0
            inFile = open(rootPath + file.path, "rb")
            chunk = inFile.read(self.BLOCK_SIZE)
            while chunk != b'':
                # verify folder exists or create if necessary
                filename = encryptedFolder + file.encryptedFilePath + "/chunk" + str(chunkIndex)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                outFile = open(filename, "wb")
                outData = self.fernet.encrypt(chunk)
                outDataBin = base64.urlsafe_b64decode(outData)
                outFile.write(outDataBin)
                outFile.close()
                chunkIndex += 1
                chunk = inFile.read(self.BLOCK_SIZE)
            inFile.close()

    def decrypt(self, file):
        # test if encrypted path is a file or directory. This will determine method of decryption

        rootPath = self.GlobalSettings.rootPath
        encryptedFolder = self.GlobalSettings.encryptedFolder
        if os.path.isfile(encryptedFolder + file.encryptedFilePath):
            # single encrypted file. Decrypt as normal
            inFile = open(encryptedFolder + file.encryptedFilePath, "rb")
            if file.path[0] == '/':
                outFile = open(rootPath + file.path[1:], "wb")
            else:
                outFile = open(rootPath + file.path, "wb")
            outDataBin = base64.urlsafe_b64encode(inFile.read())
            outData = self.fernet.decrypt(outDataBin)
            outFile.write(outData)
            inFile.close()
            outFile.close()
        else:
            # must decrypt multiple files and append together
            chunkIndex = 0
            filename = encryptedFolder + file.encryptedFilePath + "/chunk" + str(chunkIndex)
            outFile = open(rootPath + file.path, "wb")
            while os.path.exists(filename):
                # chunk exists, decrypt and write to output
                inFile = open(filename, "rb")
                outDataEnc = base64.urlsafe_b64encode(inFile.read())
                outData = self.fernet.decrypt(outDataEnc)
                outFile.write(outData)
                inFile.close()
                chunkIndex += 1
                filename = encryptedFolder + file.encryptedFilePath + "/chunk" + str(chunkIndex)

            outFile.close()
