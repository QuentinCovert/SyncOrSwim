from sqlalchemy import create_engine, Column, Integer, Boolean, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from FileSystemObject import File, Directory
import os.path




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

        def __init__(self, *args):
            if(len(args)==1):
                self.path = args[0].path
                self.lastModified = args[0].lastModified
                self.deleted = args[0].fileDeleted
                self.toEncrypt = args[0].encryptionOn
                self.lastSync = args[0].lastSyncTime
                self.encryptedPath = args[0].encryptedFilePath
                self.parent = os.path.dirname(args[0].path)
            else:
                self.path = args[0]
                self.lastModified = args[1]
                self.deleted = args[2]
                self.toEncrypt = args[3]
                self.lastSync = args[4]
                self.encryptedPath = args[5]
                self.parent = args[6]
      
        def convert(self):
            return File(self.path, self.lastModified, self.deleted, self.toEncrypt, self.lastSync, self.encryptedPath)
class DirectoryObject(Base):
        __tablename__ = 'directories'
        path = Column(String, primary_key=True)
        lastModified = Column(DateTime, default=datetime.datetime.utcnow)
        deleted = Column(Boolean)
        toEncrypt = Column(Boolean)
        lastSync = Column(DateTime, default=datetime.datetime.utcnow)
        parent = Column(String)
        
        def __init__(self, *args):
            if(len(args)==1):
                self.path = args[0].path
                self.lastModified = args[0].lastModified
                self.deleted = args[0].fileDeleted
                self.toEncrypt = args[0].encryptionOn
                self.lastSync = args[0].lastSyncTime
                self.parent = os.path.dirname(args[0].path)
            else:
                self.path = args[0]
                self.lastModified = args[1]
                self.deleted = args[2]
                self.toEncrypt = args[3]
                self.lastSync = args[4]
                self.parent = args[5]
        def convert(self):
            return Directory(self.path, self.lastModified, self.deleted, self.toEncrypt, self.lastSync,[])
        
        
class GlobalSetting(Base):
        __tablename__ = 'global_settings'
        name = Column(String, primary_key=True)
        value = Column(Integer)
        enabled = Column(Boolean)
        
        def __init__(self, name, value, enabled):
            self.name = name
            self.value = value
            self.enabled = enabled
        
class GlobalRoots(Base):
        __tablename__ = 'global_roots'
        name = Column(String, primary_key=True)
        
        def __init__(self, name):
            self.name = name
      
      
#Files and Directories Section

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
                        c = session.query(FileObject).filter_by(parent=obj.path).all()
                        for fd in c:
                            obj.files.append(fd.convert())
                        #find all subdirectories
                        d = session.query(DirectoryObject).filter_by(parent = obj.path).all()
                        #print(d)
                        for fd in d:
                           # print(fd.path)
                            obj.files.append(retrieve(fd.path))
                            
                        session.close()
                        return obj
                else:
                        return None
                
#Retrieve file or directory, but not any subdirectories
def fastRetrieve(path):
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
                        session.close()
                        return obj
                else:
                        return None

#deletes file or directory and all subdirectories from database
def delete(obj1):
    if((type(obj1) is File) or (type(obj1) is Directory)):
        session = Session()
        path1 = obj1.path
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

#stores file or directory and all subdirectories in database, if files are new they are added, otherwise they are just modified
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

#deletes all files and directories that have been deleted from the file system
def cull():
    session = Session()
    session.query(FileObject).filter_by(deleted = True).delete()
    session.query(DirectoryObject).filter_by(deleted = True).delete()
    session.commit()
    session.close()

#pulls roots from database
def pullRoots():
    session = Session()
    roots = session.query(DirectoryObject).filter_by(parent = "").all()
    rootObjects = []
    print(roots)
    for root in roots:
        rootObjects.append(retrieve(root.path))
    return rootObjects

#pulls everything that is out of sync out of the database, starting from the roots
def syncRoots():
    roots = pullRoots()
    outOfSync = []
    for root in roots:
        if(root.lastModified > root.lastSyncTime):
            root.files = checkMod(root.files)
            outOfSync.append(root)
    return outOfSync

#recursive function to check if the subfiles are out of sync
def checkMod(checkList):
	outOfSync = []
	for fd in checkList:
		if (type(fd) is File):
			if(fd.lastModified > fd.lastSyncTime):
				outOfSync.append(fd)
		if(type(fd) is Directory):
			if(fd.lastModified > fd.lastSyncTime):
				fd.files = checkMod(fd.files)
				outOfSync.append(fd)
	return outOfSync


#Settings Section

def retrieve_setting(name):
    session = Session()
    gs = session.query(GlobalSetting).filter_by(name = name).all()
    if(gs != None):
        if(gs[0].value == None):
            return gs[0].enabled
        if(gs[0].enabled == True):
            return gs[0].value
    else:
        return None

def change_setting(name, value, enabled):
    gs = GlobalSetting(name, value, enabled)
    session = Session()
    session.merge(gs)
    session.commit()
    session.close()
    return None

def retrieve_roots():
    session = Session()
    r = []
    roots = session.query(GlobalRoots).all()
    for root in roots:
        r.append(root.name)
    return r

def insert_root(name):
    root = GlobalRoots(name)
    session = Session()
    session.merge(root)
    session.commit()
    session.close()
    return None

def delete_root(name):
    session = Session()
    session.query(GlobalRoots).filter_by(name = name).delete()
    session.commit()
    session.close()
    return None

