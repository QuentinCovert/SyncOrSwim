import FileSystemObject.py
import hashlib

class File(FileSystemObject):

    def __init__(self, fileName, path, mod, deleted, encrypted, lastSync, ePath, hash):
        super(self, path, mod, deleted, encrypted, lastSync, fileName)
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