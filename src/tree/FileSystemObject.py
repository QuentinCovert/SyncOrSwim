from abc import ABCMeta, abstractmethod

class FileSystemObject(metaclass=ABCMeta):

    __metaclass__ = ABCMeta
    
    def __init__(self, path, mod, deleted, encrypted, lastSync):
        self.path = path
        self.lastModified = mod
        self.fileDeleted = deleted
        self.encryptionOn = encrypted
        self.lastSyncTime = lastSync

    def getPath(self):
        return self.path
    
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

    def printFile(self):
        print("File:")
        print(self.path)

class Directory(FileSystemObject):
    
    def __init__(self, path, mod, deleted, encrypted, lastSync, files):
        super().__init__(path, mod, deleted, encrypted, lastSync)
        self.files = files

    def __len__(self):
        return len(self.files)

    def __getitem__(self,index):
        return self.files[index]
    
    def addFile(self, file):
        self.files.append(file)

    def encrypt(self, crypto):
        for file in files:
            encrypt(file, crypto)
        return files
        
    def decrypt(self, crypto):
        for file in files:
            encrypt(file, crypto)
        return files
    
    def printDirectoryNoChildren(self):
        print("Directory:")
        print(self.path)
    
    def printDirectory(self):
        print("Directory:")
        print(self.path)
        for file in self.files:
            if(isinstance(file, File)):
                print("File:")
                file.printFile()
            elif(isinstance(file, Directory)):
                print("Directory:")
                file.printDirectory()
                
