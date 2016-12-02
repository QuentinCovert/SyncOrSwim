#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from lib.MainWindow import Ui_MainWindow
from lib.Settings import Settings
import sys
from os import path
from shutil import copyfile
from lib.FileSystemObject import FileSystemObject, File
from lib.Crypto import Crypto
from cryptography.fernet import Fernet
import base64
import lib.database

global localSettingsExist
global globalSettingsExist
global databaseFO
global globalCrypto
global currentPath
global resourcesPath

#intialization code. Start by getting settings
currentPath = path.dirname(path.realpath("__file__")) + "/"
resourcesPath = currentPath + "resources/"

if path.exists(currentPath + "resources/settings.p") == False:
    #the local settings file does not exist
    #pop up windows asking to initialize here
    global localSettingsExist
    localSettingsExist = False
else:
    global localSettingsExist
    localSettingsExist = True

if path.exists(currentPath + "resources/global_settings.p") == False:
    #the global settings file doesn't exist
    global globalSettingsExist
    globalSettingsExist = False
else:
    global globalSettingsExist
    globalSettingsExist = True

if localSettingsExist and globalSettingsExist:
    global globalSettings
    global resourcesPath
    global databaseFO
    globalSettings = Settings(currentPath + "resources/")
    globalCrypto = Crypto(globalSettings)
    #test local database against remote
    localDBTime = path.getmtime(resourcesPath + "SyncOrSwimDB.db")
    remoteDBTime = path.getmtime(globalSettings.remotePath + "SyncOrSwimDB")
    if localDBTime < remoteDBTime:
        #local is older, download remote
        databaseFO = File(resourcesPath + "SyncOrSwimDB.db", 0, 0, True, 0, globalSettings.remotePath + "SyncOrSwimDB")
        copyfile(globalSettings.remotePath + "SyncOrSwimDB", globalSettings.encryptedFolder + "SyncOrSwimDB")
        fernet = Fernet(globalSettings.key)
        inFile = open(globalSettings.encryptedFolder + "SyncOrSwimDB", "rb")
        outFile = open(resourcesPath + "SyncOrSwimDB.db", "wb")
        outDataEnc = base64.urlsafe_b64encode(inFile.read())
        outData = fernet.decrypt(outDataEnc)
        outFile.write(outData)
        inFile.close()
        outFile.close()
        #compare files
        rootDirectory = database.pullRoots()

    else:
        #local is newer, replace remote and upload files
        x = 1
        #rootDirectory = lib.database.pullRoots()
        #print(rootDirectory.files[0].path)

print(globalSettingsExist)
print(localSettingsExist)
#GUI setup code
app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow(currentPath, resourcesPath, localSettingsExist, globalSettingsExist)
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
