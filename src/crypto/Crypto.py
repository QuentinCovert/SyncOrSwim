from cryptography.fernet import Fernet
import os
import base64

MINIMUM_SPLIT_SIZE = 400000000
BLOCK_SIZE = 10000000


class Crypto:

    def __init__(self, crypto_key):
        self.key = crypto_key
        self.fernet = Fernet(self.key)

    def generateKey():
        return Fernet.generate_key()

    def encrypt(self, file):
        #TODO: config class operation
        #TODO: test file size. If over a certain size use split method, otherwise just encrypt
        fileSize = os.path.getsize(file.filePath)

        if fileSize < MINIMUM_SPLIT_SIZE:
            # encrypt in one file
            inFile = open(file.filePath, "rb")
            outFile = open(file.encryptedFilePath, "wb")
            outData = self.fernet.encrypt(inFile.read())
            outDataBin = base64.urlsafe_b64decode(outData)
            outFile.write(outDataBin)
            inFile.close()
            outFile.close()

        else:
            # encrypt in chunks
            chunkIndex = 0
            inFile = open(file.filePath, "rb")
            chunk = inFile.read(BLOCK_SIZE)
            while chunk != b'':
                # verify folder exists or create if necessary
                filename = file.encryptedFilePath + "/chunk" + str(chunkIndex)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                outFile = open(filename, "wb")
                outData = self.fernet.encrypt(chunk)
                outDataBin = base64.urlsafe_b64decode(outData)
                outFile.write(outDataBin)
                outFile.close()
                chunkIndex += 1
                chunk = inFile.read(BLOCK_SIZE)
            inFile.close()

    def decrypt(self, file):
        # test if encrypted path is a file or directory. This will determine method of decryption

        if os.path.isfile(file.encryptedFilePath):
            # single encrypted file. Decrypt as normal
            inFile = open(file.encryptedFilePath, "rb")
            outFile = open(file.filePath, "wb")
            outDataBin = base64.urlsafe_b64encode(inFile.read())
            outData = self.fernet.decrypt(outDataBin)
            outFile.write(outData)
            inFile.close()
            outFile.close()
        else:
            # must decrypt multiple files and append together
            chunkIndex = 0
            filename = file.encryptedFilePath + "/chunk" + str(chunkIndex)
            outFile = open(file.filePath, "wb")
            while os.path.exists(filename):
                # chunk exists, decrypt and write to output
                inFile = open(filename, "rb")
                outDataEnc = base64.urlsafe_b64encode(inFile.read())
                outData = self.fernet.decrypt(outDataEnc)
                outFile.write(outData)
                inFile.close()
                chunkIndex += 1
                filename = file.encryptedFilePath + "/chunk" + str(chunkIndex)

            outFile.close()
