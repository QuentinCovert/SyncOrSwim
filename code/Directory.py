import FileSystemObject.py

class Directory(FileSystemObject):
    
    def __init__(self, fileName, path, mod, deleted, encrypted, lastSync, files):
        super(self, path, mod, deleted, encrypted, lastSync, fileName)
        self.files = files
    
    def encrypt(self, crypto):
        for file in files
            encrypt(file, crypto)
        return files
        
    def decrypt(self, crypto):
        for file in files
            encrypt(file, crypto)
        return files