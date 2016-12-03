from sqlalchemy import create_engine, Column, Integer, Boolean, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class IgnoredFileObject(Base):
    __tablename__ = 'ignored_files'
    ignoredFilePath = Column(String, primary_key=True)

    def __init__(self, arg):
        self.ignoredFilePath = arg

    def convert(self):
        return self.ignoredFilePath

class DeletedFileObject(Base):
    __tablename__ = 'deleted_files'
    deletedFilePath = Column(String, primary_key=True)

    def __init__(self, arg):
        self.deletedFilePath = arg

    def convert(self):
        return self.deletedFilePath

#Get a list of relative paths of all files to be ignored by the system.
def retrieveIgnoredFiles():
    session = Session()
    ignoredFileList = session.query(IgnoredFilesObject).all()
    session.close()
    retList = []
    for ignoredFileObj in ignoredFileList:
        reList.append(ignoredFileObj.convert())
    return retList

#Removes an ignored filePath from the database. This would be used when the user chooses to no longer ignore a file.
def deleteIgnoredFile(filePath):
    if isinstance(filePath, str):
        session = Session()
        session.query(IgnoredFilesObject).filter_by(ignoredFilePath=filePath).delete()
        session.commit()
        session.close()
        return True
    else:
        return False

#This adds an ignored filePath to the db. This would be used when the user chooses to ignore a file.
def storeIgnoredFile(filePath):
    if isinstance(filePath, str):
        session = Session()
        obj = IgnoredFileObject(filePath)
        session.merge(obj)
        session.commit()
        session.close()
        return True
    else:
        return False

#Get a list of relative paths of all files to be deleted by the system, if they exist.
def retrieveDeletedFiles():
    session = Session()
    deletedFileList = session.query(DeletedFileObject).all()
    session.close()
    retList = []
    for deletedFileObj in deletedFileList:
        reList.append(deletedFileObj.convert())
    return retList

#Removes an deleted filePath from the database. This would be used when the user chooses to add a file which was deleted.
def deleteDeletedFile(filePath):
    if isinstance(filePath, str):
        session = Session()
        session.query(DeletedFileObject).filter_by(deletedFilePath=filePath).delete()
        session.commit()
        session.close()
        return True
    else:
        return False

#This adds an deleted filePath to the db. This would be used when the user chooses to delete a file that's in the root.
def storeDeletedFile(filePath):
    if isinstance(filePath, str):
        session = Session()
        obj = DeletedFileObject(filePath)
        session.merge(obj)
        session.commit()
        session.close()
        return True
    else:
        return False
