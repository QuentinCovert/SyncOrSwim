from sqlalchemy import create_engine, Column, Integer, Boolean, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import hashlib
from FileSystemObject import File, Directory




engine = create_engine('sqlite:///SyncOrSwimDB.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class FileObject(Base):
        __tablename__ = 'files'
        path = Column(String, primary_key=True)
        lastModified = Column(DateTime, default=datetime.datetime.utcnow)
        deleted = Column(Boolean)
        toEncrypt = Column(Boolean)
        lastSync = Column(DateTime, default=datetime.datetime.utcnow)
        encryptedPath = Column(String)
        
#	def __init__(self, path, lastModified, deleted, toEncrypt, lastSync, encryptedPath):
#		self.path = path
#		self.lastModified = lastModified
#		self.deleted = deleted
#		self.toEncrypt = toEncrypt
#		self.lastSync = lastSync
#		self.encryptedPath = encryptedPath
        def __init__(self, *args):
            if(len(args)==1):
                self.path = args[0].filePath
                self.lastModified = args[0].lastModified
                self.deleted = args[0].fileDeleted
                self.toEncrypt = args[0].encryptionOn
                self.lastSync = args[0].lastSyncTime
                self.encryptedPath = args[0].encryptedFilePath
            else:
                self.path = args[0]
                self.lastModified = args[1]
                self.deleted = args[2]
                self.toEncrypt = args[3]
                self.lastSync = args[4]
                self.encryptedPath = args[5]
      
        def convert(self):
            return File(self.path, self.path, self.lastModified, self.deleted, self.toEncrypt, self.lastSync, self.encryptedPath, hash)
class DirectoryObject(Base):
        __tablename__ = 'directories'
        path = Column(String, primary_key=True)
        lastModified = Column(DateTime, default=datetime.datetime.utcnow)
        deleted = Column(Boolean)
        toEncrypt = Column(Boolean)
        lastSync = Column(DateTime, default=datetime.datetime.utcnow)
        children = Column(Integer)
        
#	def __init__(self, path, lastModified, deleted, toEncrypt, lastSync, children):
#		self.path = path
#		self.lastModified = lastModified
#		self.deleted = deleted
#		self.toEncrypt = toEncrypt
#		self.lastSync = lastSync
#		self.children = children
#
        def __init__(self, *args):
            if(len(args)==1):
                self.path = args[0].filePath
                self.lastModified = args[0].lastModified
                self.deleted = args[0].fileDeleted
                self.toEncrypt = args[0].encryptionOn
                self.lastSync = args[0].lastSyncTime
                self.children = len(args[0].files)
            else:
                self.path = args[0]
                self.lastModified = args[1]
                self.deleted = args[2]
                self.toEncrypt = args[3]
                self.lastSync = args[4]
                self.children = args[5]
        def convert(self):
            return Directory(self.path, self.path, self.lastModified, self.deleted, self.toEncrypt, self.lastSync, self.children)
def retrieve(path):
        session = Session()
        a = session.query(FileObject).filter_by(path=path).all()
        #Options: determine if its looking for a file or directory based on path, create different functions for both, or do nothing
        if (len(a)==1):
                b = a[0]
                session.close()
                obj = b.convert()
                return obj
        else:
                a = session.query(DirectoryObject).filter_by(path=path).all()
                if(len(a)==1):
                        b = a[0]
                        session.close()
                        obj = b.convert()
                        return obj
                else:
                        return None

def delete(obj1):
    if((type(obj1) is File) or (type(obj1) is Directory)):
        session = Session()
        path = obj1.filePath
        if(type(obj1) is Directory):
            session.query(DirectoryObject).filter_by(path=path).delete()
        
        if(type(obj1) is File):
            session.query(FileObject).filter_by(path=path).delete()
        session.commit()
        session.close()
        return True
    else:
        return False


def store(obj1):
        if((type(obj1) is File) or (type(obj1) is Directory)):	
                if(type(obj1) is Directory):
                        obj2 = DirectoryObject(obj1)
                if(type(obj1) is File):	
                        obj2 = FileObject(obj1)
                        session = Session()
                session.merge(obj2)
                session.commit()
                session.close()
                return True
        else:
                return False

