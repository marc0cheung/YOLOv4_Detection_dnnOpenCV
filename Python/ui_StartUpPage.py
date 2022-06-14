# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StartUpPageIsoWQD.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(475, 292)
        self.cfgFilePath_Label = QLabel(Dialog)
        self.cfgFilePath_Label.setObjectName(u"cfgFilePath_Label")
        self.cfgFilePath_Label.setGeometry(QRect(30, 90, 301, 20))
        font = QFont()
        font.setPointSize(9)
        self.cfgFilePath_Label.setFont(font)
        self.weightsFilePath_Label = QLabel(Dialog)
        self.weightsFilePath_Label.setObjectName(u"weightsFilePath_Label")
        self.weightsFilePath_Label.setGeometry(QRect(30, 170, 301, 20))
        self.weightsFilePath_Label.setFont(font)
        self.cfgFileBtn = QPushButton(Dialog)
        self.cfgFileBtn.setObjectName(u"cfgFileBtn")
        self.cfgFileBtn.setEnabled(False)
        self.cfgFileBtn.setGeometry(QRect(340, 90, 121, 28))
        self.namesFilePath_Label = QLabel(Dialog)
        self.namesFilePath_Label.setObjectName(u"namesFilePath_Label")
        self.namesFilePath_Label.setGeometry(QRect(30, 130, 301, 20))
        self.namesFilePath_Label.setFont(font)
        self.namesFileBtn = QPushButton(Dialog)
        self.namesFileBtn.setObjectName(u"namesFileBtn")
        self.namesFileBtn.setEnabled(False)
        self.namesFileBtn.setGeometry(QRect(340, 130, 121, 28))
        self.weightsFileBtn = QPushButton(Dialog)
        self.weightsFileBtn.setObjectName(u"weightsFileBtn")
        self.weightsFileBtn.setEnabled(False)
        self.weightsFileBtn.setGeometry(QRect(340, 170, 121, 28))
        self.okBtn = QPushButton(Dialog)
        self.okBtn.setObjectName(u"okBtn")
        self.okBtn.setGeometry(QRect(250, 230, 93, 28))
        self.exitBtn = QPushButton(Dialog)
        self.exitBtn.setObjectName(u"exitBtn")
        self.exitBtn.setGeometry(QRect(350, 230, 93, 28))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.cfgFilePath_Label.setText(QCoreApplication.translate("Dialog", u".cfg File: network/1.cfg", None))
        self.weightsFilePath_Label.setText(QCoreApplication.translate("Dialog", u".weights File: network/1.weights", None))
        self.cfgFileBtn.setText(QCoreApplication.translate("Dialog", u"cfgFile", None))
        self.namesFilePath_Label.setText(QCoreApplication.translate("Dialog", u".names File: network/1.names", None))
        self.namesFileBtn.setText(QCoreApplication.translate("Dialog", u"namesFile", None))
        self.weightsFileBtn.setText(QCoreApplication.translate("Dialog", u"weightsFile", None))
        self.okBtn.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.exitBtn.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi

