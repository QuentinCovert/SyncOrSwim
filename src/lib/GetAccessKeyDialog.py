# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GetAccessKeyDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import qDebug
from lib.GUIUtils import isFilePathValid

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

class Ui_GetAccessKeyDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        super(Ui_GetAccessKeyDialog, self).__init__(parent)
        self.accessKey = ""
        self.setupUi(self)

    def setupUi(self, GetAccessKeyDialog):
        GetAccessKeyDialog.setObjectName(_fromUtf8("Dialog"))
        GetAccessKeyDialog.resize(650, 150)
        GetAccessKeyDialog.setMinimumSize(QtCore.QSize(650, 150))
        self.verticalLayout = QtGui.QVBoxLayout(GetAccessKeyDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(GetAccessKeyDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.accessKeyLineEdit = QtGui.QLineEdit(GetAccessKeyDialog)
        self.accessKeyLineEdit.setObjectName(_fromUtf8("accessKeyLineEdit"))
        self.horizontalLayout.addWidget(self.accessKeyLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(GetAccessKeyDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.ok_clicked)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.cancel_clicked)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GetAccessKeyDialog)
        QtCore.QMetaObject.connectSlotsByName(GetAccessKeyDialog)

    def retranslateUi(self, GetAccessKeyDialog):
        GetAccessKeyDialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Existing Access Key:", None))

    def ok_clicked(self):
        qDebug("Access key file path = %s" % (self.accessKeyLineEdit.text()))
        if isFilePathValid(self.accessKeyLineEdit.text()):
            # file exists
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, 'Error', "Path to Access Key does not exist.", QtGui.QMessageBox.Ok)

    def cancel_clicked(self):
        qDebug("Cancelled")
        self.reject()

    def getAccessKeyPath(parent = None):
        dialog = Ui_GetAccessKeyDialog(parent)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            return(dialog.accessKeyLineEdit.text())
        else:
            return("")
