from abc import ABCMeta, abstractmethod
import os
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
        self.encryptedFilePath = str(ePath)


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
        
    def setEncrypt(e):
        self.encryptionOn = e
        for file in self.files:
            if(type(file) is File):
                file.encryptionOn = e
            else:
                file.setEncrypt(e)

    def retrieve(self, path):
        if(path[0] != '/'):
            path = '/' +path
        if(path == self.path):
            return self
        else:
            for file in self.files:
                p = file.path
                if (p[-1:] != '/'):
                    p = p + '/'
                if(file.path == path):
                    return file
                if(path.startswith(p) and isinstance(file, Directory)):
                    return file.retrieve(path)
            return False

    def store(self, fd):
        if(fd.path[0] != '/'):
            fd.path = '/' + fd.path
        if(fd.path == self.path):
             self.lastModified = fd.lastModified
             self.fileDeleted = fd.fileDeleted
             self.encryptionOn = fd.encryptionOn
             self.lastSyncTime = fd.lastSyncTime
             self.files = fd.files
             return None
        else:
            for file in self.files:
                p = file.path
                if (p[-1:] != '/'):
                    p = p + '/'
                if(file.path == fd.path):
                    file.lastModified = fd.lastModified
                    file.fileDeleted = fd.fileDeleted
                    file.encryptionOn = fd.encryptionOn
                    file.lastSyncTime = fd.lastSyncTime
                    file.encryptedFilePath = fd.encryptedFilePath
                    return None
                if(fd.path.startswith(p) and isinstance(file, Directory)):
                    file.store(fd)
                    return None
            #if directory doesn't exist, create next directory and continues
            #print("fd path: " + fd.path)
            rel = os.path.relpath(fd.path, self.path)
            if(self.path == ""):
                rel = fd.path[1:]
            #print("rel: " + rel)
            split = rel.split('/')
            if(len(split) == 1):             #if there are no more subdirectories, insert the file
                #print("inserted file, no more subdirectories")
                self.files.append(fd)
            else:                            #create another subdirectory
                #print("insert subdirectories")
                path = self.path + "/" + rel.split('/')[0]
                if((path[0] == '/') and (path[1] =='/')):
                    path = path[1:]
                #print("self.path: " + self.path)
                #print(rel.split('/'))
                #print(path)
                self.files.insert(0, Directory(path, fd.lastModified, fd.fileDeleted, fd.encryptionOn, fd.lastSyncTime, []))
                #print(self.files[0].path)
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

