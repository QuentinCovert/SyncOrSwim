#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from lib.MainWindow import Ui_MainWindow
from lib.Settings import Settings
import sys
from os import path

global localSettingsExist
global globalSettingsExist

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
    globalSettings = Settings(currentPath + "resources/")

print(globalSettingsExist)
print(localSettingsExist)
#GUI setup code
app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
