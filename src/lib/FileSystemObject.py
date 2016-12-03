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


class File(FileSystemObject):

    def __init__(self, path, mod, deleted, encrypted, lastSync, ePath):
        super().__init__(path, mod, deleted, encrypted, lastSync)
        self.encryptedFilePath = ePath


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

    def printDirectoryNoChildren(self):
        print("Directory:")
        print(self.path)

    def retrieve(self, path):
        if(path == self.path):
            return self
        else:
            for file in self.files:
                if(file.path == path):
                    return file
                if(path.startswith(self.path)):
                    return file.retrieve(path)
            return False

    def store(self, fd):
        if(fd.path == self.path):
             self.lastModified = fd.lastModified
             self.fileDeleted = fd.fileDeleted
             self.encryptionOn = fd.encryptionOn
             self.lastSyncTime = fd.lastSyncTime
             self.files = fd.files
             return None
        else:
            #for i in range(len(self.files)):
            for file in self.files:
                if(file.path == path):
                    file.lastModified = fd.lastModified
                    file.fileDeleted = fd.fileDeleted
                    file.encryptionOn = fd.encryptionOn
                    file.lastSyncTime = fd.lastSyncTime
                    file.encryptedFilePath = fd.encryptedFilePath
                    return None
                if(fd.path.startswith(self.path)):
                    file.store(fd)
                    return None
            #if directory doesn't exist, create next directory and continue
            path = self.path + (os.path.relpath(path,bar).split('/')[0])
            self.files.insert(0, Directory(path, fd.lastModified, fd.fileDeleted, fd.encryptionOn, fd.lastSyncTime, []))
            self.files[0].store(fd)
            return None



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

