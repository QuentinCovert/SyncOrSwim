from lib.FileSystemObject import File, Directory
from lib.remote import Remote
from lib.Crypto import Crypto
import lib.database as database
import os


def localSync(rem, root, crypto):
#recursively checks every file in a directory, if changes have occurred, the files are pulled from the remote and put on the local system
#checks local files for last modified date, if remote is the last modified, download and decrypt it
#if local is last modified, print something
#delete as well
    if(type(rem) is File):
        local = root + rem.path
        if(os.path.exists(local)): #if the file exists locally
            ltime = os.path.getmtime(local)
            rtime = rem.lastModified.timestamp()
            if(ltime > rtime): #if the file exists locally and the mofified time is newer for the local file
                print("eat shit cameron")
            else:
                if(rem.deleted):
                    os.remove(local)
                else:
                    remote.pull(rem)
                    crypto.decrypt(rem)
        elif(not(rem.deleted)): #if the file doesn't exist locally, and isn't marked deleted
            remote.pull(rem)
            crypto.decrypt(rem)
    else:
        for file in rem.files:
            localSync(file, root, crypto)

def localSyncFinal(remote, crypto, root):
    #remote is a Remote object
    #crypto is a Crypto module
    #roo is the absolute path to the root on the local system

    #download remote database
    remote.downloadDatabase(resourcePath)
    #pull root from database
    rem = database.pullRoots()
    #execute local sync funtion
    localSync(rem, root, crypto)

def setResourcePath(resourceP):
    global resourcePath
    resourcePath = resourceP