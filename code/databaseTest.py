import database
from FileSystemObject import File, Directory
import datetime
import os

def createFSO(relPath, rootAbsPath):
    absPath = rootAbsPath + "/" + relPath
   # print(absPath)
    f = None
    if(os.path.isfile(absPath)):
        f = File(relPath, datetime.datetime.now(), False, False, datetime.datetime.now(), "")
    if(os.path.isdir(absPath)):
        f = Directory(relPath, datetime.datetime.now(), False, False, datetime.datetime.now(), [])
        for fd in os.listdir(absPath):
            #print(relPath + "/" + fd)
            g = createFSO((relPath + "/" +fd), rootAbsPath)
           # print(g.filePath)
            f.files.append(g)
    return f


path = os.path.dirname(os.getcwd())
root = os.path.dirname(path)
path = os.path.relpath(path, root)
testRoot = createFSO(path, root)
delete = testRoot.files[2]
database.store(testRoot)
d = database.retrieve("SyncOrSwim/.git")
database.delete(d)
d = database.retrieve("SyncOrSwim/code")
database.delete(d)
