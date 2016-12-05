from lib.FileSystemObject import File, Directory
from lib.remote import Remote
from lib.Crypto import Crypto
import lib.database as database
import os
from PyQt4.QtCore import qDebug


def localSync(rem, rootPath, crypto, remote):
#recursively checks every file in a directory, if changes have occurred, the files are pulled from the remote and put on the local system
#checks local files for last modified date, if remote is the last modified, download and decrypt it
#if local is last modified, print something
#delete as well
    if(type(rem) is File):
        local = rootPath + rem.path
        if(os.path.exists(local)): #if the file exists locally
            ltime = os.path.getmtime(local)
            rtime = rem.lastModified.timestamp()
            if(ltime > rtime): #if the file exists locally and the mofified time is newer for the local file
                print("eat shit cameron")
            else:
                if(rem.fileDeleted):
                    os.remove(local)
                else:
                    remote.pull(rem)
                    crypto.decrypt(rem)
        elif(not(rem.fileDeleted)): #if the file doesn't exist locally, and isn't marked deleted
            remote.pull(rem)
            crypto.decrypt(rem)
    else:
        for file in rem.files:
            localSync(file, rootPath, crypto, remote)

def localSyncFinal(remote, crypto, rootPath):
    #remote is a Remote object
    #crypto is a Crypto module
    #rootPath is the absolute path to the root on the local system
    qDebug("localSyncFinal: rootPath is = %s" % rootPath)

    #download remote database
    remote.downloadDatabase(resourcePath)
    #pull root from database
    rem = database.pullRoots()
    if isinstance(rem, Directory):
        rem.printDirectory()
    else:
        qDebug("localSyncFinal: ERROR, rem not a root directory!")
    #execute local sync funtion
    localSync(rem, rootPath, crypto, remote)
    
    #checks and removes deleted objects locally
    d = database.retrieveDeletedObjects()
    for file in d:
        local = rootPath + file
        if(os.path.exists(local)):
            os.remove(local)
        

def setResourcePath(resourceP):
    global resourcePath
    resourcePath = resourceP
