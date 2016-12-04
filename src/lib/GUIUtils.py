#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4.QtCore import QFileInfo
from PyQt4.QtCore import qDebug
import os

def isFilePathValid(path):
    fileInfo = QFileInfo(path)

    if fileInfo.exists() and fileInfo.isFile():
        qDebug("isFilePathValid: True")
        return (True)
    else:
        qDebug("isFilePathValid: False")
        return (False)

def isDirPathValid(path):
    fileInfo = QFileInfo(path)

    if fileInfo.exists() and fileInfo.isDir():
        qDebug("isDirPathValid: True")
        return (True)
    else:
        qDebug("isDirPathValid: False")
        return (False)

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def getRelPathFromAbs(filePath, rootPath):
    qDebug('Root path: ' + rootPath + '\nfilePath: ' + filePath)
    return os.path.relpath(filePath, rootPath)