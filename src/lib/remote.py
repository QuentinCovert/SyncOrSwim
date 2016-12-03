from lib.FileSystemObject import FileSystemObject, File, Directory
import os
from shutil import copytree, copyfile, rmtree
from cryptography.fernet import Fernet
import base64

#NOTE: encryptedFilePath MUST be a relative path. I need a way to get the absolute path

class Remote:

    def __init__(self, path, settings):
        # store absolute path of this root
        self.location = path
        self.GlobalSettings = settings

    def push(self, fileSO):
        #get path to root directory from settings module
        encryptedFolder = self.GlobalSettings.encryptedFolder
        rootPath = self.GlobalSettings.rootPath
        #check if file or Directory
        if isinstance(fileSO, File):
            #check if file is supposed to be encrypted
            if fileSO.encryptionOn:
                #the file is encrypted, copy from encrypted path to remote path
                #check if folder or single encrypted file
                if os.path.isdir(encryptedFolder + fileSO.encryptedFilePath):
                    #its a directory, must copy whole thing
                    dst = self.location + fileSO.encryptedFilePath
                    if os.path.exists(dst):
                        rmtree(dst)
                    copytree(encryptedFolder + fileSO.encryptedFilePath, dst)
                else:
                    #single file, just copy
                    dst = self.location + fileSO.encryptedFilePath
                    copyfile(encryptedFolder + fileSO.encryptedFilePath, dst)
            else:
                #it's not supposed to be encrypted, so just copy from root
                dst = self.location + fileSO.path
                copyfile(rootPath + fileSO.path, dst)
        elif isinstance(fileSO, Directory):
            #it's a directory, iterate over all children
            for file in fileSO.files:
                self.push(file)

    def pull(self, fileSO):
        #get path to root directory from settings module
        encryptedFolder = self.GlobalSettings.encryptedFolder
        rootPath = self.GlobalSettings.rootPath
        #check if file or directory
        if isinstance(fileSO, File):
            #check if file is supposed to be encrypted
            if fileSO.encryptionOn:
                #the file is encrypted, copy from encrypted path
                #check if folder or single encrypted file
                if os.path.isdir(self.location + fileSO.encryptedFilePath):
                    #it is a directory, download into folder in local encrypted folder
                    dst = encryptedFolder + fileSO.encryptedFilePath
                    rmtree(dst)
                    copytree(self.location + fileSO.encryptedFilePath, dst)
                else:
                    #single file, just copy
                    dst = encryptedFolder + fileSO.encryptedFilePath
                    copyfile(self.location + fileSO.encryptedFilePath, dst)
            else:
                #not encrypted, just copy straight to destination
                dst = rootPath + fileSO.path
                copyfile(self.location + fileSO.path, dst)
        elif isinstance(fileSO, Directory):
            #it's a directory, iterate over all children
            for file in fileSO.files:
                self.pull(file)

    def delete(self, fileSO):
        #get path to root directory from settings module
        encryptedFolder = self.GlobalSettings.encryptedFolder
        rootPath = self.GlobalSettings.rootPath
        #check if file or directory
        if isinstance(fileSO, File):
            #check if file is supposed to be encrypted
            if fileSO.encryptionOn:
                #the file is encrypted, copy from encrypted path to remote path
                #check if folder or single encrypted file
                if os.path.isdir(encryptedFolder + fileSO.encryptedFilePath):
                    #its a directory, must delete whole thing
                    shutil.rmtree(encryptedFolder + fileSO.encryptedFilePath)
                else:
                    #single file, just delete
                    os.remove(encryptedFolder + fileSO.encryptedFilePath)
            else:
                #it's not supposed to be encrypted, so just delete from root
                os.remove(rootPath + fileSO.path)
        elif isinstance(fileSO, Directory):
            shutil.rmtree(encryptedFolder + fileSO.path)
            
    def uploadDatabase(self, resourcesPath):
        #encrypt local database
        myFernet = Fernet(self.GlobalSettings.key)
        inFile = open(resourcesPath + 'SyncOrSwimDB.db', 'rb')
        outFile = open(self.GlobalSettings.encryptedFolder + 'SyncOrSwimDB', 'wb')
        outData = myFernet.encrypt(inFile.read())
        outDataBin = base64.urlsafe_b64decode(outData)
        outFile.write(outDataBin)
        inFile.close()
        outFile.close()
        #copy to remote
        dst = self.location + 'SyncOrSwimDB'
        copyfile(self.GlobalSettings.encryptedFolder + 'SyncOrSwimDB', dst)

    def downloadDatabase(self, resourcesPath):
        #decrypt remote database
        myFernet = Fernet(self.GlobalSettings.key)
        inFile = open(self.GlobalSettings.encryptedFolder + 'SyncOrSwimDB', 'wb')
        outFile = open(resourcesPath + 'SyncOrSwimDB.db', 'rb')
        outData = myFernet.decrypt(inFile.read())
        outDataBin = base64.urlsafe_b64decode(outData)
        outFile.write(outDataBin)
        inFile.close()
        outFile.close()

