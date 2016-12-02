from lib.FileSystemObject import File, Directory
from lib.remote import Remote
from lib.Crypto import Crypto
import os


def localSync(rem, root, crypto):
#checks local files for last modified date, if remote is the last modified, download and decrypt it
#if local is last modified, print something
#delete as well
    if(type(rem) is File):
        local = root + rem.path
        if(os.path.exists(local)): #if the file exists locally
            ltime = os.path.getmtime(local)
            if(ltime > rem.lastModified): #if the file exists locally and the mofified time is newer for the local file
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
        for file in files:
            localSync(file, root, crypto)
            