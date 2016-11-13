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
        parent = Column(String)
        
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
                self.parent = args[0].parent
            else:
                self.path = args[0]
                self.lastModified = args[1]
                self.deleted = args[2]
                self.toEncrypt = args[3]
                self.lastSync = args[4]
                self.encryptedPath = args[5]
                self.parent = args[6]
      
        def convert(self):
            return File(self.path, self.path, self.lastModified, self.deleted, self.toEncrypt, self.lastSync, self.encryptedPath)
class DirectoryObject(Base):
        __tablename__ = 'directories'
        path = Column(String, primary_key=True)
        lastModified = Column(DateTime, default=datetime.datetime.utcnow)
        deleted = Column(Boolean)
        toEncrypt = Column(Boolean)
        lastSync = Column(DateTime, default=datetime.datetime.utcnow)
        parent = Column(String)
        
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
                self.parent = args[0].parent
            else:
                self.path = args[0]
                self.lastModified = args[1]
                self.deleted = args[2]
                self.toEncrypt = args[3]
                self.lastSync = args[4]
                self.parent = args[5]
        def convert(self):
            return Directory(self.path, self.lastModified, self.deleted, self.toEncrypt, self.lastSync,[], self.parent)

#Retrieve file or directory from database based on relative path
def retrieve(path1):
        session = Session()
        a = session.query(FileObject).filter_by(path=path1).all()
        #If a file with matching path is found
        if (len(a)==1):
                b = a[0]
                session.close()
                obj = b.convert()
                return obj
        else:
                a = session.query(DirectoryObject).filter_by(path=path1).all()
                #If a directory with matching path is found
                if(len(a)==1):
                        b = a[0]
                        #convert to Directory
                        obj = b.convert()
                        #find all files in directory
                        c = session.query(FileObject).filter_by(parent=obj.filePath).all()
                        for fd in c:
                            obj.files.append(fd.convert())
                        #find all subdirectories
                        d = session.query(DirectoryObject).filter_by(parent = obj.filePath).all()
                        #print(d)
                        for fd in d:
                           # print(fd.path)
                            obj.files.append(retrieve(fd.path))
                            
                        session.close()
                        return obj
                else:
                        return None

def delete(obj1):
    if((type(obj1) is File) or (type(obj1) is Directory)):
        session = Session()
        path1 = obj1.filePath
        if(type(obj1) is Directory):
            for fd in obj1.files:
                delete(fd)
            session.query(DirectoryObject).filter_by(path=path1).delete()
        
        if(type(obj1) is File):
            session.query(FileObject).filter_by(path=path1).delete()
        session.commit()
        session.close()
        return True
    else:
        return False


def store(obj1):
        if((type(obj1) is File) or (type(obj1) is Directory)):	
                if(type(obj1) is Directory):
                        obj2 = DirectoryObject(obj1)
                        for fd in obj1.files:
                            #print("executed")
                            store(fd)
                if(type(obj1) is File):	
                        obj2 = FileObject(obj1)
                session = Session()
                session.merge(obj2)
                session.commit()
                session.close()
                return True
        else:
                return False

def cull():
    session = Session()
    session.query(FileObject).filter_by(deleted = True).delete()
    session.query(DirectoryObject).filter_by(deleted = True).delete()
    session.commit()
    session.close()

def pullRoots():
    session = Session()
    roots = session.query(DirectoryObject).filter_by(parent = "").all()
    rootObjects = []
    print(roots)
    for root in roots:
        rootObjects.append(retrieve(root.path))
    return rootObjects

def syncRoots():
    roots = pullRoots
    outOfSync = []
    for root in roots:
        if(root.lastModified > root.lastSyncTime):
            outOfSync.append(root)
    return outOfSync


