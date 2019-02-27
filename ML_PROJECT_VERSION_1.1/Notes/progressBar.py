# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progressBar.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pickle

class Ui_ProgressBar(object):
    def setupUi(self, ProgressBar):
        ProgressBar.setObjectName("ProgressBar")
        ProgressBar.resize(400, 105)
        self.progressBar = QtWidgets.QProgressBar(ProgressBar)
        self.progressBar.setGeometry(QtCore.QRect(10, 50, 371, 41))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(ProgressBar)
        self.label.setGeometry(QtCore.QRect(130, 20, 141, 21))
        self.label.setObjectName("label")
        self.retranslateUi(ProgressBar)
        QtCore.QMetaObject.connectSlotsByName(ProgressBar)

    def newValue(self,value):
        self.progressBar.setValue(value)
        
    def retranslateUi(self, ProgressBar):
        _translate = QtCore.QCoreApplication.translate
        ProgressBar.setWindowTitle(_translate("ProgressBar", "Progress Bar"))
        self.label.setText(_translate("ProgressBar", "Progress Bar"))

class ProgressBarClass(QtWidgets.QWidget,Ui_ProgressBar):
    def __init__(self,parent = None):
        super(ProgressBarClass,self).__init__(parent)
        self.setupUi(self)
    def updateProgressBar(self,val):
        self.progressBar.setValue(val)
