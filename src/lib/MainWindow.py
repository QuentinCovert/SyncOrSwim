#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QDir, pyqtSlot, pyqtSignal, qDebug, QTimer
from lib.EncryptLocalFile import Ui_EcryptLocalFileDialog as EncryptLocalFileDialog
from lib.SetRemoteFileSystemDialog import Ui_SetRemoteFileSystemDialog as SetRemoteFileSystemDialog
from lib.GenerateAccessKeyDialog import Ui_GenerateAccessKeyDialog as GenerateAccessKeyDialog
from lib.InitSystemDialog import Ui_initSystemDialog as InitSystemDialog
from lib.GetAccessKeyDialog import Ui_GetAccessKeyDialog as GetAccessKeyDialog
import lib.database as database
from lib.Settings import Settings
#import lib.FSOTreeGenerator as FSOTreeObject
import lib.FileSystemObject as FileSystemObject
from lib.Settings import Settings
from lib.Crypto import Crypto
from shutil import copyfile
import socket
import select
from lib.watchman import Watchman
from lib.remote import Remote
import lib.sync
from lib.GUIUtils import getRelPathFromAbs
import datetime

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

#Note: this was auto-generated so it's a little messy. It has been organzied,
# as best I could. -Levi
class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self, currentPath, resourcesPath, localSettingsExist, globalSettingsExist):
        super(Ui_MainWindow, self).__init__()
        self.root = None
        self.currentPath = currentPath
        self.resourcesPath = resourcesPath
        lib.sync.setResourcePath(resourcesPath)
        self.settings = None
        self.clickedPath = None
        self.localSettingsExist = localSettingsExist
        self.globalSettingsExist = globalSettingsExist
        self.initSystem()
        self.setupUi(self)
        self.startBusyLoop()


    def getClickedFilePath(self, index):
        self.clickedPath = self.currFileSysModel.filePath(index)
        qDebug("User clicked: %s" % (self.clickedPath))
        relPath = getRelPathFromAbs(self.currFileSysModel.filePath(index), self.settings.rootPath)
        qDebug("getClickedFilePath: relative path returned is = %s" % relPath)

        #Verify if relPath is an acutal path:
        if relPath is not False:
            self.clickedPath = relPath
            if database.isIgnored(self.clickedPath):
                #Set GUI to display that the obj is ignored.
                self.encryptEnableComboBox.setCurrentIndex(2)   #-
                self.itemIgnoredComboBox.setCurrentIndex(0) #Yes
                self.lastUpdatedOutput.setText(_translate("MainWindow", "---------", None))
                self.lastSyncedOutput.setText(_translate("MainWindow", "---------", None))
            else:
                #Pull the obj's settings and display them.
                obj = self.root.retrieve(self.clickedPath)
                self.itemIgnoredComboBox.setCurrentIndex(1) #No
                if obj.encryptionOn:
                    self.encryptEnableComboBox.setCurrentIndex(0)
                else:
                    self.encryptEnableComboBox.setCurrentIndex(1)
                self.lastUpdatedOutput.setText(obj.lastModified.isoformat(' '))
                self.lastSyncedOutput.setText(obj.lastSyncTime.isoformat(' '))
        else:
            qDebug("ERROR in getting relative path!")

    def encryptEnableComboBoxHandler(self, index):
        if index != self.lastEncryptEnableComboBoxIndex:
            qDebug("Encrypt enable comboBox changed to index: %d" % index)
            relPath = getRelPathFromAbs(self.clickedPath, self.settings.rootPath)

            if relPath is not False:
                if database.isIgnored(relPath):
                    self.encryptEnableComboBox.setCurrentIndex(2)
                else:
                    qDebug("Relative path of file to en/decrypt is: %s" % relPath)
                    tmpObj = self.root.retrieve(relPath)
                    #Verify retrievely succeeded:
                    if tmpObj is not False:
                        #See if it's a file or directory obj:
                        if isinstance(tmpObj, Directory):
                            if index == 0:
                                #Need to set encryption to on:
                                tmpObj.setEncrypt(True)
                            else:
                                #Nee to set encryption to off:
                                tmpObj.setEncrypt(False)
                        else:
                            #It's a file type
                            if index == 0:
                                #Need to set encryption to on:
                                tmpObj.encryptionOn = True
                            else:
                                #Nee to set encryption to off:
                                tmpObj.encryptionOn = False

                            self.root.store(tmpObj)
                            remote = Remote(self.settings.remotePath, self.settings)
                            remote.uploadDatabase(self.resourcesPath)
            else:
                qDebug("ERROR! Could not retrieve obj from relative path in tree!")
            self.lastEncryptEnableComboBoxIndex = index

    def itemIgnoredComboBoxHandler(self, index):
        if index != self.lastItemIgnoredComboBoxIndex:
            qDebug("Item ignored comboBox changed to index: %d" % index)
            if index == 0:
                qDebug("User switched itemIgnoredComboBox to Yes.")
                result = QtGui.QMessageBox.warning(self, 'Warning', "Ignored files/directories will not be synced to remote!", QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                qDebug("User selected: %d" % result)
                if result == QtGui.QMessageBox.Ok:
                    database.deleteAndIgnore(self.clickedPath)
                    remote = Remote(self.settings.remotePath, self.settings)
                    remote.uploadDatabase(self.resourcesPath)
                    self.watchman.unsubscribe(self.root.path,'sub1')
                    self.watchman.subscribe(database.retrieveIgnoredObjects())
                else:
                    self.itemIgnoredComboBox.setCurrentIndex(1)
            self.lastItemIgnoredComboBoxIndex = index

    def setupUi(self, MainWindow):

        #Inital setup:
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1060, 620)
        MainWindow.setMinimumSize(QtCore.QSize(1060, 620))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/syncOrSwimLogo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        #Create the GUI's layout:
        self.createUiLayout(MainWindow)

        #Create the GUI's menu bar:
        self.createMenuBar(MainWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Connect signals and slots:
        self.fileSystemView.clicked.connect(self.getClickedFilePath)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Sync Or Swim", None))
        self.rootLabel.setText(_translate("MainWindow", "Welcome to SyncOrSwim UI!", None))
        self.groupBox.setTitle(_translate("MainWindow", "Selection Info", None))
        self.rootOutputLabel.setText(_translate("MainWindow", "", None))

        '''
        self.ignoredTitleLabel.setText(_translate("MainWindow", "Item Ignored:", None))
        self.itemIgnoredComboBox.setItemText(0, _translate("MainWindow", "Yes", None))
        self.itemIgnoredComboBox.setItemText(1, _translate("MainWindow", "No", None))
        self.itemIgnoredComboBox.setItemText(2, _translate("MainWindow", "-", None))
        self.encryptEnableTitleLabel.setText(_translate("MainWindow", "Auto-Encrypt Enabled:", None))
        self.encryptEnableComboBox.setItemText(0, _translate("MainWindow", "Yes", None))
        self.encryptEnableComboBox.setItemText(1, _translate("MainWindow", "No", None))
        self.encryptEnableComboBox.setItemText(2, _translate("MainWindow", "-", None))
        '''

        self.lastUpatedTitleLabel.setText(_translate("MainWindow", "Last updated:", None))
        self.lastUpdatedOutput.setText(_translate("MainWindow", "", None))
        self.lastSyncedTitleLabel.setText(_translate("MainWindow", "Last Synced:", None))
        self.lastSyncedOutput.setText(_translate("MainWindow", "", None))

        '''
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionEncrypt_Local_File.setText(_translate("MainWindow", "Encrypt Local File", None))
        self.actionManage_Root_Directories.setText(_translate("MainWindow", "Manage Root Directories", None))
        self.actionCreate_New_Encryption_Key.setText(_translate("MainWindow", "Create New Encryption Key", None))
        self.actionSet_Remote_File_System_Target.setText(_translate("MainWindow", "Set Remote File System Target", None))
        self.actionGenerate_New_Access_Key.setText(_translate("MainWindow", "Generate New Access Key", None))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation", None))
        self.actionContact_Us.setText(_translate("MainWindow", "Contact Us", None))
        self.actionManage_Root_Directories.setText(_translate("MainWindow", "Manage Root Directories", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        '''

        self.encryptEnableComboBox.setCurrentIndex(2)
        self.itemIgnoredComboBox.setCurrentIndex(2)
        self.currFileSysModel = QtGui.QFileSystemModel(self)
        self.currFileSysModel.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.AllDirs)
        self.currFileSysModel.setRootPath(self.settings.rootPath)
        self.fileSystemView.setModel(self.currFileSysModel)
        self.fileSystemView.setRootIndex(self.currFileSysModel.index(self.settings.rootPath))

    def createUiLayout(self, MainWindow):
        #Create central 'vertical' GUI layout:
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(20, 20, 20, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        #Create the top horizontal layout. This contains the label, combo box,
        # and a spacer.
        self.topHorizontalLayout = QtGui.QHBoxLayout()
        self.topHorizontalLayout.setObjectName(_fromUtf8("topHorizontalLayout"))
        self.createRootLabel()
        self.createRootOutputLabel()
        self.createSpacer()
        self.verticalLayout.addLayout(self.topHorizontalLayout) #Finish of top layout.


        #Create the bottom layout. This contains the treeView (which will display
        # a tree struct of the current root dir the user is working with) and the
        # options table (which will display the options set on a selected dir or file).
        self.bottomHorizontalLayout = QtGui.QHBoxLayout()
        self.bottomHorizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.bottomHorizontalLayout.setObjectName(_fromUtf8("bottomHorizontalLayout"))
        self.createFileSystemView()
        self.createOptionsLayout()
        self.verticalLayout.addLayout(self.bottomHorizontalLayout)  #Finish the bottom layout.
        MainWindow.setCentralWidget(self.centralwidget) #Finsih layout.


    #Create root label. This is what says 'Choose Root Directory' on the GUI:
    def createRootLabel(self):
        self.rootLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rootLabel.sizePolicy().hasHeightForWidth())
        self.rootLabel.setSizePolicy(sizePolicy)
        self.rootLabel.setTextFormat(QtCore.Qt.AutoText)
        self.rootLabel.setObjectName(_fromUtf8("rootLabel"))
        self.topHorizontalLayout.addWidget(self.rootLabel)


    #Create the combo box which will allow users to specify which root directory
    # they wish to be working with.
    def createRootOutputLabel(self):
        self.rootOutputLabel = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rootOutputLabel.sizePolicy().hasHeightForWidth())
        self.rootOutputLabel.setSizePolicy(sizePolicy)
        self.rootOutputLabel.setTextFormat(QtCore.Qt.AutoText)
        self.rootOutputLabel.setObjectName(_fromUtf8("rootOutputLabel"))
        self.topHorizontalLayout.addWidget(self.rootOutputLabel)

    #This is a simple spacer item which keeps the label and combo box to the left:
    def createSpacer(self):
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.topHorizontalLayout.addItem(spacerItem)

    #Create the fileSystemView:
    def createFileSystemView(self):
        self.fileSystemView = QtGui.QTreeView(self.centralwidget)
        self.fileSystemView.setObjectName(_fromUtf8("fileSystemView"))
        self.bottomHorizontalLayout.addWidget(self.fileSystemView)

    #Create the optionsTableWidget:
    def createOptionsLayout(self):
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.optionsLayout = QtGui.QFormLayout(self.groupBox)
        self.optionsLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.optionsLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.optionsLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.optionsLayout.setMargin(20)
        self.optionsLayout.setHorizontalSpacing(10)
        self.optionsLayout.setVerticalSpacing(70)
        self.optionsLayout.setObjectName(_fromUtf8("optionsLayout"))
        self.ignoredTitleLabel = QtGui.QLabel(self.groupBox)
        '''
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ignoredTitleLabel.setFont(font)
        self.ignoredTitleLabel.setObjectName(_fromUtf8("ignoredTitleLabel"))
        self.optionsLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.ignoredTitleLabel)
        self.itemIgnoredComboBox = QtGui.QComboBox(self.groupBox)
        self.itemIgnoredComboBox.setObjectName(_fromUtf8("itemIgnoredComboBox"))
        self.itemIgnoredComboBox.addItem(_fromUtf8(""))
        self.itemIgnoredComboBox.addItem(_fromUtf8(""))
        self.itemIgnoredComboBox.addItem(_fromUtf8(""))
        self.itemIgnoredComboBox.activated.connect(self.itemIgnoredComboBoxHandler)
        self.lastItemIgnoredComboBoxIndex = 2
        self.optionsLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.itemIgnoredComboBox)
        self.encryptEnableTitleLabel = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.encryptEnableTitleLabel.setFont(font)
        self.encryptEnableTitleLabel.setObjectName(_fromUtf8("encryptEnableTitleLabel"))
        self.optionsLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.encryptEnableTitleLabel)
        self.encryptEnableComboBox = QtGui.QComboBox(self.groupBox)
        self.encryptEnableComboBox.setObjectName(_fromUtf8("encryptEnableComboBox"))
        self.encryptEnableComboBox.addItem(_fromUtf8(""))
        self.encryptEnableComboBox.addItem(_fromUtf8(""))
        self.encryptEnableComboBox.addItem(_fromUtf8(""))
        self.lastEncryptEnableComboBoxIndex = 2
        self.encryptEnableComboBox.activated.connect(self.encryptEnableComboBoxHandler)
        self.optionsLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.encryptEnableComboBox)
        self.lastUpatedTitleLabel = QtGui.QLabel(self.groupBox)
        '''
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lastUpatedTitleLabel.setFont(font)
        self.lastUpatedTitleLabel.setObjectName(_fromUtf8("lastUpatedTitleLabel"))
        self.optionsLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lastUpatedTitleLabel)
        self.lastUpdatedOutput = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lastUpdatedOutput.setFont(font)
        self.lastUpdatedOutput.setText(_fromUtf8(""))
        self.lastUpdatedOutput.setObjectName(_fromUtf8("lastUpdatedOutput"))
        self.optionsLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lastUpdatedOutput)
        self.lastSyncedTitleLabel = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lastSyncedTitleLabel.setFont(font)
        self.lastSyncedTitleLabel.setObjectName(_fromUtf8("lastSyncedTitleLabel"))
        self.optionsLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.lastSyncedTitleLabel)
        self.lastSyncedOutput = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lastSyncedOutput.setFont(font)
        self.lastSyncedOutput.setText(_fromUtf8(""))
        self.lastSyncedOutput.setObjectName(_fromUtf8("lastSyncedOutput"))
        self.optionsLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lastSyncedOutput)
        self.bottomHorizontalLayout.addWidget(self.groupBox)

    #Create the menu bar:
    def createMenuBar(self, MainWindow):
        '''
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1060, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))

        Create the menu bar's tabs:
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)

        #Create status bar
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        #Add actions to the File tab:
        self.actionEncrypt_Local_File = QtGui.QAction(MainWindow)
        self.actionEncrypt_Local_File.setObjectName(_fromUtf8("actionEncrypt_Local_File"))
        self.actionEncrypt_Local_File.triggered.connect(self.encryptLocalFile)
        self.menuFile.addAction(self.actionEncrypt_Local_File)
        self.actionCreate_New_Encryption_Key = QtGui.QAction(MainWindow)
        self.actionCreate_New_Encryption_Key.setObjectName(_fromUtf8("actionCreate_New_Encryption_Key"))
        self.menuFile.addAction(self.actionCreate_New_Encryption_Key)
        self.menuFile.addSeparator()
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.triggered.connect(self.quitApplication)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionExit)

        #Add actions to Settings tab:
        self.actionSet_Remote_File_System_Target = QtGui.QAction(MainWindow)
        self.actionSet_Remote_File_System_Target.setObjectName(_fromUtf8("actionSet_Remote_File_System_Target"))
        self.actionSet_Remote_File_System_Target.triggered.connect(self.setRemoteFileSystemTarget)
        self.menuSettings.addAction(self.actionSet_Remote_File_System_Target)
        self.actionGenerate_New_Access_Key = QtGui.QAction(MainWindow)
        self.actionGenerate_New_Access_Key.setObjectName(_fromUtf8("actionGenerate_New_Access_Key"))
        self.actionGenerate_New_Access_Key.triggered.connect(self.generateNewAccessKey)
        self.menuSettings.addAction(self.actionGenerate_New_Access_Key)
        self.menuSettings.addSeparator()
        self.actionManage_Root_Directories = QtGui.QAction(MainWindow)
        self.actionManage_Root_Directories.setObjectName(_fromUtf8("actionManage_Root_Directories"))
        self.menuSettings.addAction(self.actionManage_Root_Directories)

        #Add actions to Help tab:
        self.actionDocumentation = QtGui.QAction(MainWindow)
        self.actionDocumentation.setObjectName(_fromUtf8("actionDocumentation"))
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addSeparator()
        self.actionContact_Us = QtGui.QAction(MainWindow)
        self.actionContact_Us.setObjectName(_fromUtf8("actionContact_Us"))
        self.menuHelp.addAction(self.actionContact_Us)

        #Add tabs to menu:
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        '''

    #Taken from: http://stackoverflow.com/questions/21079941/how-can-i-kill-a-single-shot-qtcore-qtimer-in-pyqt4
    def startBusyLoop(self):
        self.busyLoopTimer = QTimer(self)
        self.busyLoopTimer.timeout.connect(self.busyLoop)
        self.busyLoopTimer.start(2000)

    def busyLoop(self):
        #Do busy loop work here
        qDebug("Busy loop triggered.")
        self.watchman.parse()

    def initSystem(self):
        self.root = database.pullRoots()
        qDebug("Initalizing system.")
        #if the user does not have local settings file, initialize it
        if self.localSettingsExist == False:
            syncDirPath, remoteDirPath = InitSystemDialog.initSystem(self)
            if syncDirPath is "" and remoteDirPath is "":
                sys.exit()
            encDir = self.currentPath + "enc/"
            Settings.generateLocalSettings(self.resourcesPath, syncDirPath, encDir, remoteDirPath)
            qDebug("Test: syncDirPath = %s, remoteDirPath = %s" % (syncDirPath, remoteDirPath))
        #test if global settings is present
        if self.globalSettingsExist == False:
            userHasAccessKey = QtGui.QMessageBox.question(self, 'Startup Message', "Access Key is not present, do you have an existing Access Key?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            qDebug("accesskey: %d" % userHasAccessKey)
            if userHasAccessKey == QtGui.QMessageBox.Yes:
                accessKeyPath = GetAccessKeyDialog.getAccessKeyPath(self)
                if accessKeyPath is "":
                    sys.exit()
                qDebug("Init: accessKeyPath = %s" % accessKeyPath)
                #copy settings file into system
                dst = self.resourcesPath + "global_settings.p"
                copyfile(accessKeyPath, dst)
                #TODO: get database and shit
                #TODO: dowgetRelPathFromAbs "" and unit is "":
            else:
                size, unit = GenerateAccessKeyDialog.openDialog("", "", self)
                if size is "" and unit is "":
                    sys.exit()
                qDebug("MainWindow: returned from set encryption options: size = %s, unit = %s" % (size, unit))
                #convert size and unit to bytes
                if unit == 'MB':
                    sizeBytes = int(size) * 1000000
                else:
                    sizeBytes = int(size) * 1000000000
                #generate settings file
                key = Crypto.generateKey()
                Settings.generateGlobalSettings(self.resourcesPath, sizeBytes, 10000000, key)
                #this is a new remote, upload the local database to it
                #NOTE: maybe generate new database here?
                self.settings = Settings(self.resourcesPath)
                remote = Remote(self.settings.remotePath, self.settings)
                remote.uploadDatabase(self.resourcesPath)
        #Settings are now created, or proven to exist. Now load them into GUI:
        self.settings = Settings(self.resourcesPath)
        crypto = Crypto(self.settings)
        remote = Remote(self.settings.remotePath, self.settings)
        lib.sync.localSyncFinal(remote, crypto, self.settings.rootPath)
        #init socket
        self.watchman = Watchman(self.settings.rootPath, self.root, crypto, remote, self.settings, self.resourcesPath)
        self.watchman.subscribe()


    def encryptLocalFile(self):
        tmpFilePath = EncryptLocalFileDialog.getEncryptFilePath(self)
        qDebug("MainWindow: returned encrypt file path = %s" % tmpFilePath)
        if len(tmpFilePath) > 0:
            #TODO: encrypt file path points to
            qDebug("Encrypt file....")

    def setRemoteFileSystemTarget(self):
        tmpFilePath = SetRemoteFileSystemDialog.getRemoteFileSystemPath(self)
        qDebug("MainWindow: returned remote file system path = %s" % tmpFilePath)
        if len(tmpFilePath) > 0:
            #TODO: change settings file
            qDebug("Set Remote File System Path....")

    def generateNewAccessKey(self):
        size, unit = SetEncryptionOptions.setOptions("3", "GB", self)
        qDebug("MainWindow: returned from set encryption options: key = %s, size = %s, unit = %s" % (key, size, unit))

    def quitApplication(self):
        result = QtGui.QMessageBox.question(self, 'Exit', "Are you sure you want to exit the application?", QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        if result == QtGui.QMessageBox.Ok:
            sys.exit()
