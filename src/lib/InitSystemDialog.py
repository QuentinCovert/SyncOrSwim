# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InitSystemDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import qDebug
from lib.GUIUtils import isDirPathValid

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

class Ui_initSystemDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        super(Ui_initSystemDialog, self).__init__(parent)
        self.syncDirPath = ""
        self.remoteDirPath = ""
        self.setupUi(self)

    def setupUi(self, initSystemDialog):
        initSystemDialog.setObjectName(_fromUtf8("initSystemDialog"))
        initSystemDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        initSystemDialog.resize(700, 400)
        initSystemDialog.setMinimumSize(QtCore.QSize(700, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/syncOrSwimLogo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        initSystemDialog.setWindowIcon(icon)
        initSystemDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(initSystemDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.title = QtGui.QLabel(initSystemDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName(_fromUtf8("title"))
        self.verticalLayout.addWidget(self.title)
        self.horizontalLayout1 = QtGui.QHBoxLayout()
        self.horizontalLayout1.setSpacing(10)
        self.horizontalLayout1.setObjectName(_fromUtf8("horizontalLayout1"))
        self.pathSyncLabel = QtGui.QLabel(initSystemDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pathSyncLabel.setFont(font)
        self.pathSyncLabel.setObjectName(_fromUtf8("pathSyncLabel"))
        self.horizontalLayout1.addWidget(self.pathSyncLabel)
        self.pathSyncDirLineEdit = QtGui.QLineEdit(initSystemDialog)
        self.pathSyncDirLineEdit.setObjectName(_fromUtf8("pathSyncDirLineEdit"))
        self.horizontalLayout1.addWidget(self.pathSyncDirLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout1)
        self.horizontalLayout2 = QtGui.QHBoxLayout()
        self.horizontalLayout2.setSpacing(10)
        self.horizontalLayout2.setObjectName(_fromUtf8("horizontalLayout2"))
        self.pathRemoteLabel = QtGui.QLabel(initSystemDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pathRemoteLabel.setFont(font)
        self.pathRemoteLabel.setObjectName(_fromUtf8("pathRemoteLabel"))
        self.horizontalLayout2.addWidget(self.pathRemoteLabel)
        self.pathRemoteDirLineEdit = QtGui.QLineEdit(initSystemDialog)
        self.pathRemoteDirLineEdit.setObjectName(_fromUtf8("pathRemoteDirLineEdit"))
        self.horizontalLayout2.addWidget(self.pathRemoteDirLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout2)
        self.buttonBox = QtGui.QDialogButtonBox(initSystemDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.ok_clicked)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.cancel_clicked)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(initSystemDialog)
        QtCore.QMetaObject.connectSlotsByName(initSystemDialog)

    def retranslateUi(self, initSystemDialog):
        initSystemDialog.setWindowTitle(_translate("initSystemDialog", "Initalization", None))
        self.title.setText(_translate("initSystemDialog", "Please enter the following information to initalize SyncOrSwim:", None))
        self.pathSyncLabel.setText(_translate("initSystemDialog", "Path to Sync Directory:", None))
        self.pathRemoteLabel.setText(_translate("initSystemDialog", "Path to Remote Directory:", None))

    def ok_clicked(self):

        if isDirPathValid(self.pathSyncDirLineEdit.text()) is False:
            QtGui.QMessageBox.warning(self, 'Error', "Sync Directory path does not exist.", QtGui.QMessageBox.Ok)
        elif isDirPathValid(self.pathRemoteDirLineEdit.text()) is False:
            QtGui.QMessageBox.warning(self, 'Error', "Remote Directory path does not exist.", QtGui.QMessageBox.Ok)
        else:
            self.syncDirPath = self.pathSyncDirLineEdit.text()
            self.remoteDirPath = self.pathRemoteDirLineEdit.text()
            self.accept()

    def cancel_clicked(self):
        self.reject()

    def initSystem(parent = None):
        dialog = Ui_initSystemDialog(parent)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            return(dialog.syncDirPath, dialog.remoteDirPath)
        else:
            return("", "")
