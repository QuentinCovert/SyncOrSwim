from abc import ABCMeta, abstractmethod
import hashlib

class FileSystemObject(metaclass=ABCMeta):

    __metaclass__ = ABCMeta
    
    def __init__(self, path, mod, deleted, encrypted, lastSync):
        self.path = path
        self.lastModified = mod
        self.fileDeleted = deleted
        self.encryptionOn = encrypted
        self.lastSyncTime = lastSync

    @abstractmethod
    def encrypt(self, crypto): pass
    
    @abstractmethod
    def decrypt(self, crypto): pass

class File(FileSystemObject):

    def __init__(self, path, mod, deleted, encrypted, lastSync, ePath):
        super().__init__(path, mod, deleted, encrypted, lastSync)
        self.encryptedFilePath = ePath
    
    def encrypt(self, crypto):
        return encrypt(crypto, self)
    
    def decrypt(self, crypto):
        return decrypt(crypto, self)

class Directory(FileSystemObject):
    
    def __init__(self, path, mod, deleted, encrypted, lastSync, files):
        super().__init__(path, mod, deleted, encrypted, lastSync)
        self.files = files
    
    def encrypt(self, crypto):
        for file in files:
            encrypt(file, crypto)
        return files
        
    def decrypt(self, crypto):
        for file in files:
            encrypt(file, crypto)
        return files
