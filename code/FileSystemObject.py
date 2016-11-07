from abc import ABCMeta, abstractmethod

class FileSystemObject(metaclass=ABCMeta):

    __metaclass__ = ABCMeta
    
    def __init__(self, fileName, path, mod, deleted, encrypted, lastSync):
        self.filePath = path
        self.lastModified = mod
        self.fileDeleted = deleted
        self.encryptionOn = encrypted
        self.lastSyncTime = lastSync
        self.fileName = fileName

    @abstractmethod
    def encrypt(self, crypto): pass
    
    @abstractmethod
    def decrypt(self, crypto): pass