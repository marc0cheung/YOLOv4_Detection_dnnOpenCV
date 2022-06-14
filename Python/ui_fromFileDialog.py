# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fromFileDialogfTBBLN.ui'
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
        Dialog.resize(1003, 701)
        self.original_image = QLabel(Dialog)
        self.original_image.setObjectName(u"original_image")
        self.original_image.setGeometry(QRect(60, 150, 416, 416))
        font = QFont()
        font.setFamily(u"Agency FB")
        font.setPointSize(24)
        self.original_image.setFont(font)
        self.original_image.setAutoFillBackground(True)
        self.original_image.setAlignment(Qt.AlignCenter)
        self.result_image = QLabel(Dialog)
        self.result_image.setObjectName(u"result_image")
        self.result_image.setGeometry(QRect(540, 150, 416, 416))
        self.result_image.setMinimumSize(QSize(0, 0))
        self.result_image.setFont(font)
        self.result_image.setAutoFillBackground(True)
        self.result_image.setAlignment(Qt.AlignCenter)
        self.file_path_label = QLabel(Dialog)
        self.file_path_label.setObjectName(u"file_path_label")
        self.file_path_label.setGeometry(QRect(20, 600, 381, 20))
        font1 = QFont()
        font1.setPointSize(9)
        self.file_path_label.setFont(font1)
        self.SelcPathBtn = QPushButton(Dialog)
        self.SelcPathBtn.setObjectName(u"SelcPathBtn")
        self.SelcPathBtn.setGeometry(QRect(410, 600, 75, 23))
        self.detect_btn = QPushButton(Dialog)
        self.detect_btn.setObjectName(u"detect_btn")
        self.detect_btn.setGeometry(QRect(480, 330, 51, 81))
        self.savepath_label = QLabel(Dialog)
        self.savepath_label.setObjectName(u"savepath_label")
        self.savepath_label.setGeometry(QRect(580, 600, 281, 20))
        self.savepath_label.setFont(font1)
        self.SavePathBtn = QPushButton(Dialog)
        self.SavePathBtn.setObjectName(u"SavePathBtn")
        self.SavePathBtn.setGeometry(QRect(870, 600, 75, 23))
        self.segment_save = QPushButton(Dialog)
        self.segment_save.setObjectName(u"segment_save")
        self.segment_save.setGeometry(QRect(620, 650, 141, 31))
        self.save_cap = QPushButton(Dialog)
        self.save_cap.setObjectName(u"save_cap")
        self.save_cap.setGeometry(QRect(780, 650, 141, 31))
        self.notification = QLabel(Dialog)
        self.notification.setObjectName(u"notification")
        self.notification.setGeometry(QRect(20, 660, 481, 31))
        self.notification.setAutoFillBackground(True)
        self.notification.setAlignment(Qt.AlignCenter)
        self.cfgFileBtn = QPushButton(Dialog)
        self.cfgFileBtn.setObjectName(u"cfgFileBtn")
        self.cfgFileBtn.setEnabled(False)
        self.cfgFileBtn.setGeometry(QRect(540, 30, 121, 28))
        self.cfgFilePath_Label = QLabel(Dialog)
        self.cfgFilePath_Label.setObjectName(u"cfgFilePath_Label")
        self.cfgFilePath_Label.setGeometry(QRect(70, 30, 301, 20))
        self.cfgFilePath_Label.setFont(font1)
        self.namesFileBtn = QPushButton(Dialog)
        self.namesFileBtn.setObjectName(u"namesFileBtn")
        self.namesFileBtn.setEnabled(False)
        self.namesFileBtn.setGeometry(QRect(540, 70, 121, 28))
        self.namesFilePath_Label = QLabel(Dialog)
        self.namesFilePath_Label.setObjectName(u"namesFilePath_Label")
        self.namesFilePath_Label.setGeometry(QRect(70, 70, 301, 20))
        self.namesFilePath_Label.setFont(font1)
        self.weightsFilePath_Label = QLabel(Dialog)
        self.weightsFilePath_Label.setObjectName(u"weightsFilePath_Label")
        self.weightsFilePath_Label.setGeometry(QRect(70, 110, 301, 20))
        self.weightsFilePath_Label.setFont(font1)
        self.weightsFileBtn = QPushButton(Dialog)
        self.weightsFileBtn.setObjectName(u"weightsFileBtn")
        self.weightsFileBtn.setEnabled(False)
        self.weightsFileBtn.setGeometry(QRect(540, 110, 121, 28))
        self.saveThresholdBtn = QPushButton(Dialog)
        self.saveThresholdBtn.setObjectName(u"saveThresholdBtn")
        self.saveThresholdBtn.setGeometry(QRect(730, 110, 181, 28))
        self.confThreshold_label = QLabel(Dialog)
        self.confThreshold_label.setObjectName(u"confThreshold_label")
        self.confThreshold_label.setGeometry(QRect(730, 10, 181, 16))
        self.NMSInput = QTextEdit(Dialog)
        self.NMSInput.setObjectName(u"NMSInput")
        self.NMSInput.setGeometry(QRect(850, 60, 61, 41))
        self.confThreshold_Input = QTextEdit(Dialog)
        self.confThreshold_Input.setObjectName(u"confThreshold_Input")
        self.confThreshold_Input.setGeometry(QRect(850, 10, 61, 41))
        self.NMSThreshold_label = QLabel(Dialog)
        self.NMSThreshold_label.setObjectName(u"NMSThreshold_label")
        self.NMSThreshold_label.setGeometry(QRect(730, 60, 181, 16))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Detect from file(s)", None))
        self.original_image.setText(QCoreApplication.translate("Dialog", u"Original Image", None))
        self.result_image.setText(QCoreApplication.translate("Dialog", u"Result", None))
        self.file_path_label.setText(QCoreApplication.translate("Dialog", u"Select Image File Path...", None))
        self.SelcPathBtn.setText(QCoreApplication.translate("Dialog", u"Select", None))
        self.detect_btn.setText(QCoreApplication.translate("Dialog", u"Go", None))
        self.savepath_label.setText(QCoreApplication.translate("Dialog", u"Select Result Saving Path...", None))
        self.SavePathBtn.setText(QCoreApplication.translate("Dialog", u"Select", None))
        self.segment_save.setText(QCoreApplication.translate("Dialog", u"Segment_Save", None))
        self.save_cap.setText(QCoreApplication.translate("Dialog", u"Save Cap", None))
        self.notification.setText(QCoreApplication.translate("Dialog", u"Notification", None))
        self.cfgFileBtn.setText(QCoreApplication.translate("Dialog", u"cfgFile", None))
        self.cfgFilePath_Label.setText(QCoreApplication.translate("Dialog", u".cfg File: network/1.cfg", None))
        self.namesFileBtn.setText(QCoreApplication.translate("Dialog", u"namesFile", None))
        self.namesFilePath_Label.setText(QCoreApplication.translate("Dialog", u".names File: network/1.names", None))
        self.weightsFilePath_Label.setText(QCoreApplication.translate("Dialog", u".weights File: network/1.weights", None))
        self.weightsFileBtn.setText(QCoreApplication.translate("Dialog", u"weightsFile", None))
        self.saveThresholdBtn.setText(QCoreApplication.translate("Dialog", u"Save Threshold", None))
        self.confThreshold_label.setText(QCoreApplication.translate("Dialog", u"confThreshold:", None))
        self.NMSInput.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">0.4</span></p></body></html>", None))
        self.confThreshold_Input.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">0.9</span></p></body></html>", None))
        self.NMSThreshold_label.setText(QCoreApplication.translate("Dialog", u"NMS Threshold:", None))
    # retranslateUi

