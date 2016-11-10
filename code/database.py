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
	
	def __init__(self, path, lastModified, deleted, toEncrypt, lastSync, encryptedPath):
		self.path = path
		self.lastModified = lastModified
		self.deleted = deleted
		self.toEncrypt = toEncrypt
		self.lastSync = lastSync
		self.encryptedPath = encryptedPath

class DirectoryObject(Base):
	__tablename__ = 'directories'
	path = Column(String, primary_key=True)
	lastModified = Column(DateTime, default=datetime.datetime.utcnow)
	deleted = Column(Boolean)
	toEncrypt = Column(Boolean)
	lastSync = Column(DateTime, default=datetime.datetime.utcnow)
	children = Column(Integer)
	
	def __init__(self, path, lastModified, deleted, toEncrypt, lastSync, children):
		self.path = path
		self.lastModified = lastModified
		self.deleted = deleted
		self.toEncrypt = toEncrypt
		self.lastSync = lastSync
		self.children = children


def retrieve(path):
	session = Session()
	a = session.query(FileObject).filter_by(path=path).all()
	#TODO: check if both a file and directory exist
	#Options: determine if its looking for a file or directory based on path, create different functions for both, or do nothing
	if (len(a)==1):
		b = a[0]
		session.close()
		obj = File(b.path, b.path, b.lastModified, b.deleted, b.toEncrypt, b.lastSync, b.encryptedPath, hash)
		return obj
	else:
		a = session.query(DirectoryObject).filter_by(path=path).all()
		if(len(a)==1):
			b = a[0]
			session.close()
			#return b
			obj = Directory(b.path, b.path, b.lastModified, b.deleted, b.toEncrypt, b.lastSync, b.children)
			return obj
		else:
			return None




def store(obj1):
	if((type(obj1) is File) or (type(obj1) is Directory)):	
		if(type(obj1) is Directory):
			obj2 = DirectoryObject(obj1.filePath, obj1.lastModified, obj1.fileDeleted, obj1.encryptedFilePath, obj1.lastSyncTime, obj1.files)
		if(type(obj1) is File):	
			obj2 = FileObject(obj1.filePath, obj1.lastModified, obj1.fileDeleted, obj1.encryptionOn, obj1.lastSyncTime, obj1.encryptedFilePath)
		session = Session()
		session.merge(obj2)
		session.commit()
		session.close()
		return True
	else:
		return False

