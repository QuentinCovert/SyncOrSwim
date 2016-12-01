# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'encryptLocalFile.ui'
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

class Ui_EcryptLocalFileDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        super(Ui_EcryptLocalFileDialog, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, EcryptLocalFileDialog):
        EcryptLocalFileDialog.setObjectName(_fromUtf8("EcryptLocalFileDialog"))
        EcryptLocalFileDialog.setWindowModality(QtCore.Qt.WindowModal)
        EcryptLocalFileDialog.resize(650, 150)
        EcryptLocalFileDialog.setMinimumSize(QtCore.QSize(650, 150))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/syncOrSwimLogo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EcryptLocalFileDialog.setWindowIcon(icon)
        EcryptLocalFileDialog.setModal(True)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.verticalLayout = QtGui.QVBoxLayout(EcryptLocalFileDialog)
        self.verticalLayout.setMargin(20)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(EcryptLocalFileDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(EcryptLocalFileDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(EcryptLocalFileDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.ok_clicked)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.cancel_clicked)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(EcryptLocalFileDialog)
        #self.buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(foo)

        QtCore.QMetaObject.connectSlotsByName(EcryptLocalFileDialog)

    def retranslateUi(self, EcryptLocalFileDialog):
        EcryptLocalFileDialog.setWindowTitle(_translate("EcryptLocalFileDialog", "Encrypt Local File", None))
        self.label.setText(_translate("EcryptLocalFileDialog", "Local File Path: ", None))

    def ok_clicked(self):
        qDebug("Encrypt Local File Path = %s" % (self.lineEdit.text()))
        if isFilePathValid(self.lineEdit.text()):
            # file exists
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, 'Error', "File path given does not exist.", QtGui.QMessageBox.Ok)

    def cancel_clicked(self):
        qDebug("Cancelled")
        self.reject()

    def getEncryptFilePath(parent = None):
        dialog = Ui_EcryptLocalFileDialog(parent)
        result = dialog.exec_()
        qDebug("Reached after exec_")
        if result == QtGui.QDialog.Accepted:
            return(dialog.lineEdit.text())
        else:
            return("")
