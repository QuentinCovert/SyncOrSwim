from abc import ABCMeta, abstractmethod
import hashlib

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

class File(FileSystemObject):

    def __init__(self, fileName, path, mod, deleted, encrypted, lastSync, ePath, hash):
        super().__init__(fileName, path, mod, deleted, encrypted, lastSync)
        self.encryptedFilePath = ePath
        self.hash = hash
    
    def encrypt(self, crypto):
        return encrypt(crypto, self)
    
    def decrypt(self, crypto):
        return decrypt(crypto, self)
        
    def verify(self):
        # Open,close, read file and calculate MD5 on its contents 
        with open(self.fileName) as file:
            # read contents of the file
            data = file.read()    
            # pipe contents of the file through
            md5_returned = hashlib.md5(data).hexdigest()

        # Finally compare original MD5 with freshly calculated
        if orginal_md5 == md5_returned:
            return true
        else:
            return false

class Directory(FileSystemObject):
    
    def __init__(self, fileName, path, mod, deleted, encrypted, lastSync, files):
        super().__init__(fileName, path, mod, deleted, encrypted, lastSync)
        self.files = files
    
    def encrypt(self, crypto):
        for file in files:
            encrypt(file, crypto)
        return files
        
    def decrypt(self, crypto):
        for file in files:
            encrypt(file, crypto)
        return files
