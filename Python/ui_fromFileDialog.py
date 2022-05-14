# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fromFileDialoglIflyt.ui'
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
        Dialog.resize(1003, 587)
        self.original_image = QLabel(Dialog)
        self.original_image.setObjectName(u"original_image")
        self.original_image.setGeometry(QRect(60, 20, 416, 416))
        font = QFont()
        font.setFamily(u"Agency FB")
        font.setPointSize(24)
        self.original_image.setFont(font)
        self.original_image.setAutoFillBackground(True)
        self.original_image.setAlignment(Qt.AlignCenter)
        self.result_image = QLabel(Dialog)
        self.result_image.setObjectName(u"result_image")
        self.result_image.setGeometry(QRect(540, 20, 416, 416))
        self.result_image.setMinimumSize(QSize(0, 0))
        self.result_image.setFont(font)
        self.result_image.setAutoFillBackground(True)
        self.result_image.setAlignment(Qt.AlignCenter)
        self.file_path_label = QLabel(Dialog)
        self.file_path_label.setObjectName(u"file_path_label")
        self.file_path_label.setGeometry(QRect(20, 470, 381, 20))
        font1 = QFont()
        font1.setPointSize(9)
        self.file_path_label.setFont(font1)
        self.SelcPathBtn = QPushButton(Dialog)
        self.SelcPathBtn.setObjectName(u"SelcPathBtn")
        self.SelcPathBtn.setGeometry(QRect(410, 470, 75, 23))
        self.detect_btn = QPushButton(Dialog)
        self.detect_btn.setObjectName(u"detect_btn")
        self.detect_btn.setGeometry(QRect(480, 200, 51, 81))
        self.savepath_label = QLabel(Dialog)
        self.savepath_label.setObjectName(u"savepath_label")
        self.savepath_label.setGeometry(QRect(580, 470, 281, 20))
        self.savepath_label.setFont(font1)
        self.SavePathBtn = QPushButton(Dialog)
        self.SavePathBtn.setObjectName(u"SavePathBtn")
        self.SavePathBtn.setGeometry(QRect(870, 470, 75, 23))
        self.segment_save = QPushButton(Dialog)
        self.segment_save.setObjectName(u"segment_save")
        self.segment_save.setGeometry(QRect(620, 520, 141, 31))
        self.save_cap = QPushButton(Dialog)
        self.save_cap.setObjectName(u"save_cap")
        self.save_cap.setGeometry(QRect(780, 520, 141, 31))
        self.notification = QLabel(Dialog)
        self.notification.setObjectName(u"notification")
        self.notification.setGeometry(QRect(20, 530, 481, 31))
        self.notification.setAutoFillBackground(True)
        self.notification.setAlignment(Qt.AlignCenter)

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
    # retranslateUi

