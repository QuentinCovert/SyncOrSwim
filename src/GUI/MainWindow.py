#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

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
class Ui_MainWindow(object):
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

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Sync Or Swim", None))
        self.rootLabel.setText(_translate("MainWindow", "Choose Root Directory:", None))
        self.rootDirComboBox.setItemText(0, _translate("MainWindow", "Homework", None)) #TODO: remove line. Placeholder for phase III.
        self.ignoredTitleLabel.setText(_translate("MainWindow", "Item Ignored:", None))
        self.ingoreOutput.setText(_translate("MainWindow", "No", None))
        self.encryptEnableTitleLabel.setText(_translate("MainWindow", "Auto-Encrypt Enabled:", None))
        self.encryptOutput.setText(_translate("MainWindow", "Yes", None))
        self.lastUpatedTitleLabel.setText(_translate("MainWindow", "Last updated:", None))
        self.lastUpdatedOutput.setText(_translate("MainWindow", "11/11/2016", None))
        self.lastSyncedTitleLabel.setText(_translate("MainWindow", "Last Synced:", None))
        self.lastSyncedOutput.setText(_translate("MainWindow", "11/11/2016", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionEncrypt_Local_File.setText(_translate("MainWindow", "Encrypt Local File", None))
        self.actionManage_Root_Directories.setText(_translate("MainWindow", "Manage Root Directories", None))
        self.actionCreate_New_Encryption_Key.setText(_translate("MainWindow", "Create New Encryption Key", None))
        self.actionSet_Remote_File_System_Target.setText(_translate("MainWindow", "Set Remote File System Target", None))
        self.actionSet_Encryption_Options.setText(_translate("MainWindow", "Set Encryption Options", None))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation", None))
        self.actionContact_Us.setText(_translate("MainWindow", "Contact Us", None))
        self.actionManage_Root_Directories.setText(_translate("MainWindow", "Manage Root Directories", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

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
        self.createLabel()
        self.createComboBox()
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
    def createLabel(self):
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
    def createComboBox(self):
        self.rootDirComboBox = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rootDirComboBox.sizePolicy().hasHeightForWidth())
        self.rootDirComboBox.setSizePolicy(sizePolicy)
        self.rootDirComboBox.setObjectName(_fromUtf8("rootDirComboBox"))
        self.rootDirComboBox.addItem(_fromUtf8("")) #TODO: remove line. Placeholder for phase III.
        self.topHorizontalLayout.addWidget(self.rootDirComboBox)

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
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setContentsMargins(5, -1, 5, -1)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(60)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))

        #Create the "Item Ignored" GUI label:
        self.ignoredTitleLabel = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ignoredTitleLabel.setFont(font)
        self.ignoredTitleLabel.setObjectName(_fromUtf8("ignoredTitleLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.ignoredTitleLabel)

        #Create a label which will output the parameter indicating if the file is ignored
        # by the filesystem.
        self.ingoreOutput = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ingoreOutput.setFont(font)
        self.ingoreOutput.setObjectName(_fromUtf8("ingoreOutput"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.ingoreOutput)

        #Create the "Auto Encrypt Enabled" GUI label:
        self.encryptEnableTitleLabel = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.encryptEnableTitleLabel.setFont(font)
        self.encryptEnableTitleLabel.setObjectName(_fromUtf8("encryptEnableTitleLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.encryptEnableTitleLabel)

        #Create a label which will output the parameter indicating if the file will be
        # encrypted by the encryption module.
        self.encryptOutput = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.encryptOutput.setFont(font)
        self.encryptOutput.setObjectName(_fromUtf8("encryptOutput"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.encryptOutput)

        #Create the "Last Updated" GUI label:
        self.lastUpatedTitleLabel = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lastUpatedTitleLabel.setFont(font)
        self.lastUpatedTitleLabel.setObjectName(_fromUtf8("lastUpatedTitleLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lastUpatedTitleLabel)

        #Create a label which will output the parameter indicating the last time a selected
        # file/dir was changed.
        self.lastUpdatedOutput = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lastUpdatedOutput.setFont(font)
        self.lastUpdatedOutput.setObjectName(_fromUtf8("lastUpdatedOutput"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lastUpdatedOutput)

        #Create the "Last Synced" GUI label:
        self.lastSyncedTitleLabel = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lastSyncedTitleLabel.setFont(font)
        self.lastSyncedTitleLabel.setObjectName(_fromUtf8("lastSyncedTitleLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.lastSyncedTitleLabel)

        #Create a label which will output the parameter indicating the last time a selected
        # file/dir was synced by the database module.
        self.lastSyncedOutput = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lastSyncedOutput.setFont(font)
        self.lastSyncedOutput.setObjectName(_fromUtf8("lastSyncedOutput"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lastSyncedOutput)
        self.bottomHorizontalLayout.addLayout(self.formLayout)

    #Create the menu bar:
    def createMenuBar(self, MainWindow):
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1060, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))

        #Create the menu bar's tabs:
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)

        #Honestly, not %100 sure what the statusbar is... It's something that was auto-generated.
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        #Add actions to the File tab:
        self.actionEncrypt_Local_File = QtGui.QAction(MainWindow)
        self.actionEncrypt_Local_File.setObjectName(_fromUtf8("actionEncrypt_Local_File"))
        self.menuFile.addAction(self.actionEncrypt_Local_File)
        self.actionCreate_New_Encryption_Key = QtGui.QAction(MainWindow)
        self.actionCreate_New_Encryption_Key.setObjectName(_fromUtf8("actionCreate_New_Encryption_Key"))
        self.menuFile.addAction(self.actionCreate_New_Encryption_Key)
        self.menuFile.addSeparator()
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionExit)

        #Add actions to Settings tab:
        self.actionSet_Remote_File_System_Target = QtGui.QAction(MainWindow)
        self.actionSet_Remote_File_System_Target.setObjectName(_fromUtf8("actionSet_Remote_File_System_Target"))
        self.menuSettings.addAction(self.actionSet_Remote_File_System_Target)
        self.actionSet_Encryption_Options = QtGui.QAction(MainWindow)
        self.actionSet_Encryption_Options.setObjectName(_fromUtf8("actionSet_Encryption_Options"))
        self.menuSettings.addAction(self.actionSet_Encryption_Options)
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
