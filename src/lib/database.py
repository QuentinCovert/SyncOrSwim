from sqlalchemy import create_engine, Column, Integer, Boolean, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from lib.FileSystemObject import File, Directory
import os.path




engine = create_engine('sqlite:///resources/SyncOrSwimDB.db')
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
                            if(fd.path != fd.parent):
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
        storeDeletedObj(obj1.path)
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

#deletes file or directory and all subdirectories from database and marks them as ignored.
def deleteAndIgnore(obj1):
    if(isinstance(obj1, File) or isinstance(obj1, Directory)):
        storeIgnoredObj(obj1.path)
        session = Session()
        path1 = obj1.path
        if(type(obj1) is Directory):
            for fd in obj1.files:
                #should you just delete them, or add them to the ignored list as well?
                delete(fd)
            session.query(DirectoryObject).filter_by(path=path1).delete()
        if(type(obj1) is File):
            session.query(FileObject).filter_by(path=path1).delete()
        session.commit()
        session.close()
        return True
    else:
        if (obj1[0] != '/'):
            obj1 = '/' + obj1
        obj = retrieve(obj1)
        if(obj != None):
            return deleteAndIgnore(obj)
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
    roots = session.query(DirectoryObject).filter_by(path = "/").all()
    if (len(roots)==1):
        rootObjects = (retrieve(roots[0].path))
        return rootObjects
    else:
        root = Directory("/", datetime.datetime.now(), False, False, None, [])
        rootObject = DirectoryObject(root)
        session.merge(rootObject)
        session.commit()
        session.close()
        return root

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


class IgnoredObject(Base):
    __tablename__ = 'ignored_objects'
    ignoredObjPath = Column(String, primary_key=True)

    def __init__(self, arg):
        self.ignoredObjPath = arg

class DeletedObject(Base):
    __tablename__ = 'deleted_objects'
    deletedObjPath = Column(String, primary_key=True)

    def __init__(self, arg):
        self.deletedObjPath = arg

#Checks to see if given path is in the ignored list:
def isIgnored(path):
    list = retrieveIgnoredObjects()
    if path in list:
        return True
    else:
        return False

#Get a list of relative paths of all files to be ignored by the system.
def retrieveIgnoredObjects():
    session = Session()
    ignoredList = session.query(IgnoredObject).all()
    session.close()
    retList = []
    for ignoredObj in ignoredList:
        reList.append(ignoredObj.ignoredObjPath)
    return retList

#Removes an ignored path from the database. This would be used when the user chooses to no longer ignore a file.
def deleteIgnoredObject(objPath):
    if isinstance(objPath, str):
        session = Session()
        session.query(IgnoredObject).filter_by(ignoredObjPath=objPath).delete()
        session.commit()
        session.close()
        return True
    else:
        return False

#This adds an ignored path to the db. This would be used when the user chooses to ignore a file.
def storeIgnoredObj(objPath):
    if isinstance(objPath, str):
        session = Session()
        obj = IgnoredObject(objPath)
        session.merge(obj)
        session.commit()
        session.close()
        return True
    else:
        return False

#Get a list of relative paths of all files to be deleted by the system, if they exist.
def retrieveDeletedObjects():
    session = Session()
    deletedObjList = session.query(DeletedObject).all()
    session.close()
    retList = []
    for deletedObj in deletedObjList:
        reList.append(deletedObj.deletedObjPath)
    return retList

#Removes an deleted filePath from the database. This would be used when the user chooses to add a file which was deleted.
def deleteDeletedObj(filePath):
    if isinstance(filePath, str):
        session = Session()
        session.query(DeletedObject).filter_by(deletedObjPath=filePath).delete()
        session.commit()
        session.close()
        return True
    else:
        return False

#This adds an deleted filePath to the db. This would be used when the user chooses to delete a file that's in the root.
def storeDeletedObj(filePath):
    if isinstance(filePath, str):
        session = Session()
        obj = DeletedObject(filePath)
        session.merge(obj)
        session.commit()
        session.close()
        return True
    else:
        return False
