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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1060, 620)
        MainWindow.setMinimumSize(QtCore.QSize(1060, 620))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/syncOrSwimLogo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setContentsMargins(20, 10, 20, 0)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.fileSystemView = QtGui.QTreeView(self.centralwidget)
        self.fileSystemView.setObjectName(_fromUtf8("fileSystemView"))
        self.horizontalLayout_2.addWidget(self.fileSystemView)
        self.optionsView = QtGui.QTableView(self.centralwidget)
        self.optionsView.setObjectName(_fromUtf8("optionsView"))
        self.horizontalLayout_2.addWidget(self.optionsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1060, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionEncrypt_Local_File = QtGui.QAction(MainWindow)
        self.actionEncrypt_Local_File.setObjectName(_fromUtf8("actionEncrypt_Local_File"))
        self.actionManage_Root_Directories = QtGui.QAction(MainWindow)
        self.actionManage_Root_Directories.setObjectName(_fromUtf8("actionManage_Root_Directories"))
        self.actionCreate_New_Encryption_Key = QtGui.QAction(MainWindow)
        self.actionCreate_New_Encryption_Key.setObjectName(_fromUtf8("actionCreate_New_Encryption_Key"))
        self.actionSet_Remote_File_System_Target = QtGui.QAction(MainWindow)
        self.actionSet_Remote_File_System_Target.setObjectName(_fromUtf8("actionSet_Remote_File_System_Target"))
        self.actionSet_Encryption_Options = QtGui.QAction(MainWindow)
        self.actionSet_Encryption_Options.setObjectName(_fromUtf8("actionSet_Encryption_Options"))
        self.actionDocumentation = QtGui.QAction(MainWindow)
        self.actionDocumentation.setObjectName(_fromUtf8("actionDocumentation"))
        self.actionContact_Us = QtGui.QAction(MainWindow)
        self.actionContact_Us.setObjectName(_fromUtf8("actionContact_Us"))
        self.actionManage_Root_Directories_2 = QtGui.QAction(MainWindow)
        self.actionManage_Root_Directories_2.setObjectName(_fromUtf8("actionManage_Root_Directories_2"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionEncrypt_Local_File)
        self.menuFile.addAction(self.actionCreate_New_Encryption_Key)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuSettings.addAction(self.actionSet_Remote_File_System_Target)
        self.menuSettings.addAction(self.actionSet_Encryption_Options)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionManage_Root_Directories_2)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionContact_Us)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Sync Or Swim", None))
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
        self.actionManage_Root_Directories_2.setText(_translate("MainWindow", "Manage Root Directories", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
