# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GenerateAccessKeyDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import qDebug
from lib.GUIUtils import isInt

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

class Ui_GenerateAccessKeyDialog(QtGui.QDialog):
    def __init__(self, defaultAutoMaxEncryptSize, defaultSizeUnit, parent = None):
        super(Ui_GenerateAccessKeyDialog, self).__init__(parent)
        self.maxAutoEncryptSize = defaultAutoMaxEncryptSize
        self.sizeUnit = defaultSizeUnit
        self.setupUi(self)

    def setupUi(self, GenerateAccessKeyDialog):
        GenerateAccessKeyDialog.setObjectName(_fromUtf8("GenerateAccessKeyDialog"))
        GenerateAccessKeyDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        GenerateAccessKeyDialog.resize(650, 170)
        GenerateAccessKeyDialog.setMinimumSize(QtCore.QSize(650, 170))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/syncOrSwimLogo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        GenerateAccessKeyDialog.setWindowIcon(icon)
        GenerateAccessKeyDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(GenerateAccessKeyDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.infoLabel = QtGui.QLabel(GenerateAccessKeyDialog)
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setIndent(-1)
        self.infoLabel.setObjectName(_fromUtf8("infoLabel"))
        self.verticalLayout.addWidget(self.infoLabel)
        self.bottomHorizontalLayout = QtGui.QHBoxLayout()
        self.bottomHorizontalLayout.setSpacing(20)
        self.bottomHorizontalLayout.setObjectName(_fromUtf8("bottomHorizontalLayout"))
        self.setMaxAutoEncryptSizeLabel = QtGui.QLabel(GenerateAccessKeyDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.setMaxAutoEncryptSizeLabel.setFont(font)
        self.setMaxAutoEncryptSizeLabel.setObjectName(_fromUtf8("setMaxAutoEncryptSizeLabel"))
        self.bottomHorizontalLayout.addWidget(self.setMaxAutoEncryptSizeLabel)
        self.maxSizeLlineEdit = QtGui.QLineEdit(GenerateAccessKeyDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.maxSizeLlineEdit.setFont(font)
        self.maxSizeLlineEdit.setObjectName(_fromUtf8("maxSizeLlineEdit"))
        self.bottomHorizontalLayout.addWidget(self.maxSizeLlineEdit)
        self.sizeUnitcomboBox = QtGui.QComboBox(GenerateAccessKeyDialog)
        self.sizeUnitcomboBox.setObjectName(_fromUtf8("sizeUnitcomboBox"))
        self.sizeUnitcomboBox.addItem(_fromUtf8(""))
        self.sizeUnitcomboBox.addItem(_fromUtf8(""))
        self.sizeUnitcomboBox.addItem(_fromUtf8(""))
        self.bottomHorizontalLayout.addWidget(self.sizeUnitcomboBox)
        self.verticalLayout.addLayout(self.bottomHorizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(GenerateAccessKeyDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.ok_clicked)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.cancel_clicked)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GenerateAccessKeyDialog)
        QtCore.QMetaObject.connectSlotsByName(GenerateAccessKeyDialog)

    def retranslateUi(self, GenerateAccessKeyDialog):
        GenerateAccessKeyDialog.setWindowTitle(_translate("GenerateAccessKeyDialog", "Dialog", None))
        self.infoLabel.setText(_translate("GenerateAccessKeyDialog", "Due to system restrictions, SyncOrSwim can not encrypt files larger than available RAM on a system in one chunk. To address this issue, SyncOrSwim will break files that exceed this limit into smaller chunks. Thus, it is suggested to set the maximum file size to one fourth of your system\'s RAM.", None))
        self.setMaxAutoEncryptSizeLabel.setText(_translate("GenerateAccessKeyDialog", "Set Max File Size to Load into RAM:", None))
        self.sizeUnitcomboBox.setItemText(0, _translate("SetEncryptionOptionsDialog", "Select", None))
        self.sizeUnitcomboBox.setItemText(1, _translate("SetEncryptionOptionsDialog", "GB", None))
        self.sizeUnitcomboBox.setItemText(2, _translate("SetEncryptionOptionsDialog", "MB", None))
        if self.maxAutoEncryptSize is not "" and self.maxAutoEncryptSize is not None:
            self.maxSizeLlineEdit.setText(self.maxAutoEncryptSize)
        else:
            self.maxSizeLlineEdit.setText("")
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
            self.maxAutoEncryptSize = self.maxSizeLlineEdit.text()
            self.sizeUnit = self.sizeUnitcomboBox.itemText(self.sizeUnitcomboBox.currentIndex())
            self.accept()

    def cancel_clicked(self):
        self.reject()

    def openDialog(defaultAutoMaxEncryptSize, defaultSizeUnit, parent = None):
        dialog = Ui_GenerateAccessKeyDialog(defaultAutoMaxEncryptSize, defaultSizeUnit, parent)
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            return(dialog.maxAutoEncryptSize, dialog.sizeUnit)
        else:
            return("", "", "")
