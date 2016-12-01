# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SetEncryptionOptions.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import qDebug
from lib.GUIUtils import isDirPathValid, isInt

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

class Ui_SetEncryptionOptionsDialog(QtGui.QDialog):
    def __init__(self, defaultEncryptionKey, defaultAutoMaxEncryptSize, defaultSizeUnit, parent = None):
        super(Ui_SetEncryptionOptionsDialog, self).__init__(parent)
        self.encryptionKey = defaultEncryptionKey
        self.maxAutoEncryptSize = defaultAutoMaxEncryptSize
        self.sizeUnit = defaultSizeUnit
        self.setupUi(self)

    def setupUi(self, SetEncryptionOptionsDialog):
        SetEncryptionOptionsDialog.setObjectName(_fromUtf8("SetEncryptionOptionsDialog"))
        SetEncryptionOptionsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        SetEncryptionOptionsDialog.resize(650, 300)
        SetEncryptionOptionsDialog.setMinimumSize(QtCore.QSize(650, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/syncOrSwimLogo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SetEncryptionOptionsDialog.setWindowIcon(icon)
        SetEncryptionOptionsDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(SetEncryptionOptionsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.topHorizontalLayout = QtGui.QHBoxLayout()
        self.topHorizontalLayout.setSpacing(20)
        self.topHorizontalLayout.setObjectName(_fromUtf8("topHorizontalLayout"))
        self.setEncryptionKeyLabel = QtGui.QLabel(SetEncryptionOptionsDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.setEncryptionKeyLabel.setFont(font)
        self.setEncryptionKeyLabel.setObjectName(_fromUtf8("setEncryptionKeyLabel"))
        self.topHorizontalLayout.addWidget(self.setEncryptionKeyLabel)
        self.encryptionKeyLineEdit = QtGui.QLineEdit(SetEncryptionOptionsDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.encryptionKeyLineEdit.setFont(font)
        self.encryptionKeyLineEdit.setObjectName(_fromUtf8("encryptionKeyLineEdit"))
        self.topHorizontalLayout.addWidget(self.encryptionKeyLineEdit)
        self.verticalLayout.addLayout(self.topHorizontalLayout)
        self.bottomHorizontalLayout = QtGui.QHBoxLayout()
        self.bottomHorizontalLayout.setSpacing(20)
        self.bottomHorizontalLayout.setObjectName(_fromUtf8("bottomHorizontalLayout"))
        self.setMaxAutoEncryptSizeLabel = QtGui.QLabel(SetEncryptionOptionsDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.setMaxAutoEncryptSizeLabel.setFont(font)
        self.setMaxAutoEncryptSizeLabel.setObjectName(_fromUtf8("setMaxAutoEncryptSizeLabel"))
        self.bottomHorizontalLayout.addWidget(self.setMaxAutoEncryptSizeLabel)
        self.maxSizeLlineEdit = QtGui.QLineEdit(SetEncryptionOptionsDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.maxSizeLlineEdit.setFont(font)
        self.maxSizeLlineEdit.setObjectName(_fromUtf8("maxSizeLlineEdit"))
        self.bottomHorizontalLayout.addWidget(self.maxSizeLlineEdit)
        self.sizeUnitcomboBox = QtGui.QComboBox(SetEncryptionOptionsDialog)
        self.sizeUnitcomboBox.setObjectName(_fromUtf8("sizeUnitcomboBox"))
        self.sizeUnitcomboBox.addItem(_fromUtf8(""))
        self.sizeUnitcomboBox.addItem(_fromUtf8(""))
        self.sizeUnitcomboBox.addItem(_fromUtf8(""))
        self.bottomHorizontalLayout.addWidget(self.sizeUnitcomboBox)
        self.verticalLayout.addLayout(self.bottomHorizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(SetEncryptionOptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.ok_clicked)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.cancel_clicked)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SetEncryptionOptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(SetEncryptionOptionsDialog)

    def retranslateUi(self, SetEncryptionOptionsDialog):
        SetEncryptionOptionsDialog.setWindowTitle(_translate("SetEncryptionOptionsDialog", "SetEncryptionOptionsDialog", None))
        self.setEncryptionKeyLabel.setText(_translate("SetEncryptionOptionsDialog", "Set Encryption Key:", None))
        self.setMaxAutoEncryptSizeLabel.setText(_translate("SetEncryptionOptionsDialog", "Set Max Auto-Encryption Size:", None))
        self.sizeUnitcomboBox.setItemText(0, _translate("SetEncryptionOptionsDialog", "Select", None))
        self.sizeUnitcomboBox.setItemText(1, _translate("SetEncryptionOptionsDialog", "GB", None))
        self.sizeUnitcomboBox.setItemText(2, _translate("SetEncryptionOptionsDialog", "MB", None))
        self.encryptionKeyLineEdit.setText(self.encryptionKey)
        self.maxSizeLlineEdit.setText(self.maxAutoEncryptSize)
        if self.sizeUnit == "MB":
            self.sizeUnitcomboBox.setCurrentIndex(2)
        elif self.sizeUnit == "GB":
            self.sizeUnitcomboBox.setCurrentIndex(1)
        else:
            self.sizeUnitcomboBox.setCurrentIndex(0)


    def ok_clicked(self):

        if isInt(self.maxSizeLlineEdit.text()) is False:
            QtGui.QMessageBox.warning(self, 'Error', "Max Size must be an integer.", QtGui.QMessageBox.Ok)
        elif self.sizeUnitcomboBox.itemText(self.sizeUnitcomboBox.currentIndex()) == "Select":
            QtGui.QMessageBox.warning(self, 'Error', "Must select size unit.", QtGui.QMessageBox.Ok)
        else:
            self.encryptionKey = self.encryptionKeyLineEdit.text()
            self.maxAutoEncryptSize = self.maxSizeLlineEdit.text()
            self.sizeUnit = self.sizeUnitcomboBox.itemText(self.sizeUnitcomboBox.currentIndex())
            self.accept()

    def cancel_clicked(self):
        self.reject()

    def setOptions(defaultEncryptionKey, defaultAutoMaxEncryptSize, defaultSizeUnit, parent = None):
        dialog = Ui_SetEncryptionOptionsDialog(defaultEncryptionKey, defaultAutoMaxEncryptSize, defaultSizeUnit, parent)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            return(dialog.encryptionKey, dialog.maxAutoEncryptSize, dialog.sizeUnit)
        else:
            return("", "", "")
