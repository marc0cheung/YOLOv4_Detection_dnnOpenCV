# -*- coding: utf-8 -*-
# yolov4-tiny Object Detection (RealTime Video Stream but use Image Detection to segment ROIs from each frame)
import time
import cv2
import sys
from PySide2 import QtCore, QtGui, QtWidgets
import qimage2ndarray

from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QRect, Qt

from ui_StartUpPage import Ui_Dialog as StartUpUi_Dialog
from ui_yolov4 import Ui_MainWindow
from ui_fromFileDialog import Ui_Dialog as fromFileUi_Dialog

imgNum = 0
FileDirectory = ''
cfgDIR = 'networkButton/1.cfg'
namesDIR = 'networkButton/1.names'
weightsDIR = 'networkButton/1.weights'
img_width = 416
img_height = 416


def drawbbx(img, x, y, w, h, predName, score, showNames, showConf):
    colorline = (0, 255, 0)
    angerline = 13
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 1)
    cv2.line(img, (x, y), (x + angerline, y), colorline, 2)
    cv2.line(img, (x, y), (x, y + angerline), colorline, 2)
    cv2.line(img, (x + w, y), (x + w, y + angerline), colorline, 2)
    cv2.line(img, (x + w, y), (x + w - angerline, y), colorline, 2)
    cv2.line(img, (x, y + h), (x, y + h - angerline), colorline, 2)
    cv2.line(img, (x, y + h), (x + angerline, y + h), colorline, 2)
    cv2.line(img, (x + w, y + h), (x + w, y + h - angerline), colorline, 2)
    cv2.line(img, (x + w, y + h), (x + w - angerline, y + h), colorline, 2)

    if showNames:
        cv2.putText(img, predName, (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    if showConf:
        cv2.putText(img, str(int(score * 100)) + '%', (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)


class StartUpPage(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.StartUpUI = StartUpUi_Dialog()
        self.StartUpUI.setupUi(self)

        # Push Button Signals and Slots
        self.StartUpUI.cfgFileBtn.clicked.connect(self.onCfgFileBtn_Clicked)
        self.StartUpUI.namesFileBtn.clicked.connect(self.onNamesFileBtn_Clicked)
        self.StartUpUI.weightsFileBtn.clicked.connect(self.onWeightsFileBtn_Clicked)

    def onCfgFileBtn_Clicked(self):
        cfgDIR = QFileDialog.getOpenFileName(QDialog(), "Open .cfg File")
        if cfgDIR[0] != 'network/1.cfg':
            self.StartUpUI.cfgFilePath_Label.setText("cfg: " + str(cfgDIR[0]))

    def onNamesFileBtn_Clicked(self):
        namesDIR = QFileDialog.getOpenFileName(QDialog(), "Open .names File")
        if namesDIR[0] != 'network/1.names':
            self.StartUpUI.namesFilePath_Label.setText("names: " + str(namesDIR[0]))

    def onWeightsFileBtn_Clicked(self):
        weightsDIR = QFileDialog.getOpenFileName(QDialog(), "Open .weights File")
        if weightsDIR[0] != 'network/1.weights':
            self.StartUpUI.weightsFilePath_Label.setText("weights: " + str(weightsDIR[0]))


class MainWindow(QMainWindow):
    video_flip = False
    video_stream = True
    show_message = False
    show_runtime = True
    showDetectedNames = True
    showDetectedConf = True
    showBBox = True
    confThreshold = 0.9
    NMSThreshold = 0.4
    segment_path = ''

    def __init__(self, width=416, height=416, fps=30):
        super().__init__()

        self.video_size = QtCore.QSize(width, height)
        self.camera_capture = cv2.VideoCapture(cv2.CAP_DSHOW)
        self.video_capture = cv2.VideoCapture()
        self.frame_timer = QtCore.QTimer()

        self.setup_camera(fps)
        self.fps = fps

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.SaveIndexBtn.clicked.connect(self.setImgNum)
        self.ui.CapBtn.clicked.connect(self.capFrame)
        self.ui.CloseBtn.clicked.connect(self.close_win)
        self.ui.GetObjSegmentBtn.clicked.connect(self.segment)
        self.ui.SelcPathBtn.clicked.connect(self.chooseDir)
        self.ui.SelcPathBtn_segment.clicked.connect(self.chooseSegmentDir)
        self.ui.AboutBtn.clicked.connect(self.say_hello)
        self.ui.saveThresholdBtn.clicked.connect(self.onSaveThresholdClicked)

        # CheckBox Signals and Slots
        self.ui.videoFlipCheckBox.stateChanged.connect(self.onVideoFlipCheckBox_Changed)
        self.ui.videoStreamCheckBox.stateChanged.connect(self.onVideoStreamCheckBox_Changed)
        self.ui.MessageCheckBox.stateChanged.connect(self.onMessageCheckBox_Changed)
        self.ui.runtimeCheckBox.stateChanged.connect(self.onRunTimeCheckBox_Changed)
        self.ui.showNames_checkbox.stateChanged.connect(self.onShowNamesCheckBox_Changed)
        self.ui.confValue_checkbox.stateChanged.connect(self.onConfValueCheckBox_Changed)
        self.ui.showBBox_checkbox.stateChanged.connect(self.onShowBBoxCheckBox_Changed)

    def setup_camera(self, fps):
        self.camera_capture.set(3, self.video_size.width())
        self.camera_capture.set(4, self.video_size.height())

        self.frame_timer.timeout.connect(self.display_video_stream)
        self.frame_timer.start(int(1000 // fps))

    def display_video_stream(self):
        ret, frame = self.camera_capture.read()
        if not ret:
            return False

        frame = cv2.resize(frame, (img_width, img_height))

        if self.video_flip:
            frame = cv2.flip(frame, -1, frame)

        # Object Detection Starts
        T1 = time.perf_counter()
        classids, scores, bboxes = model.detect(frame, self.confThreshold, self.NMSThreshold)
        for class_id, score, bbox in zip(classids, scores, bboxes):
            x, y, w, h = bbox

            # get names of classes
            class_name = classes[class_id]

            if self.showBBox:
                drawbbx(frame, x, y, w, h, class_name, score, self.showDetectedNames, self.showDetectedConf)

        T2 = time.perf_counter()

        if self.show_message:
            if self.show_runtime:
                cv2.putText(frame, str("RT: ") + str(round(time.time() - startTime, 0)) + str('s'), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 0, 255), 1)

            cv2.putText(frame, str("FPS: 30"), (10, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
            cv2.putText(frame, str("YOLO FPS: ") + str(int(1000 / ((T2 - T1) * 1000))), (10, 150), cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (0, 0, 255), 1)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = qimage2ndarray.array2qimage(frame)

        if self.video_stream:
            self.ui.label.setPixmap(QtGui.QPixmap.fromImage(image))
        else:
            self.ui.label.setText("Video Stream is OFF.")

        self.ui.detect_status.setText(str(len(bboxes)) + " Obj(s) Detected")

    def setImgNum(self):
        global imgNum
        global img_width, img_height

        imgNum = int(self.ui.index_input.toPlainText())
        img_width = int(self.ui.width_input.toPlainText())
        img_height = int(self.ui.height_input.toPlainText())
        # print("Index Now: " + str(int(self.ui.index_input.toPlainText())))
        self.ui.status_label.setText("Index\nNow\n" + str(int(self.ui.index_input.toPlainText())))
        self.ui.label.setGeometry(QRect(30, 90, img_width, img_height))

    def segment(self):
        if self.segment_path == '':
            QMessageBox.critical(self, 'Error', 'Please select segment save directory first.')
        else:
            success, frame = self.camera_capture.read()
            frame = cv2.resize(frame, (img_width, img_height))

            segment_index = 1
            classids, scores, bboxes = model.detect(frame, 0.8, 0.3)
            for class_id, score, bbox in zip(classids, scores, bboxes):
                x, y, w, h = bbox

                # get names of classes
                class_name = classes[class_id]

                drawbbx(frame, x, y, w, h, class_name, score, self.showDetectedNames, self.showDetectedConf)
                cv2.imwrite(self.segment_path + '/segment_%s.png' % str(segment_index), frame[y: y + h, x: x + w])
                segment_index = segment_index + 1
            # print(str(len(bboxes)) + " Object(s) Detected")
            self.ui.status_label.setText(str(len(bboxes)) + "\nObject(s)\nSaved")

    def capFrame(self):
        global imgNum
        global FileDirectory
        global img_width, img_height

        if FileDirectory == '':
            QMessageBox.critical(self, 'Error', 'Please select save directory first.')
        else:
            success, frame = self.camera_capture.read()
            frame = cv2.resize(frame, (img_width, img_height))  # resolution setting: width x height

            classids, scores, bboxes = model.detect(frame, 0.8, 0.3)
            for class_id, score, bbox in zip(classids, scores, bboxes):
                x, y, w, h = bbox

                # get names of classes
                class_name = classes[class_id]

                drawbbx(frame, x, y, w, h, class_name, score, self.showDetectedNames, self.showDetectedConf)

            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.ui.label.setPixmap(QPixmap.fromImage(showImage))
            self.ui.label.setScaledContents(True)

            imgNum = int(imgNum) + 1
            # Write Images using imwrite
            # cv2.imwrite("D:\YOLOTraining\photos\%s.png" % (str(imgNum)), frame)
            cv2.imwrite(str(FileDirectory) + "/%s.png" % (str(imgNum)), frame)

            # print("Photo " + str(imgNum) + " Saved!")
            self.ui.status_label.setText("Photo\n" + str(imgNum) + "\nSaved!")

    def chooseDir(self):
        global FileDirectory
        FileDirectory = QFileDialog.getExistingDirectory(QMainWindow(), "Choose Save Directory")
        # print("File DIR: " + str(FileDirectory))
        self.ui.path_label.setText("Save to: " + str(FileDirectory))

    def chooseSegmentDir(self):
        self.segment_path = QFileDialog.getExistingDirectory(QMainWindow(), "Choose Segment Save Directory")
        self.ui.segmentPath_label.setText("Segment Save to: " + str(self.segment_path))

    def onVideoFlipCheckBox_Changed(self):
        if self.ui.videoFlipCheckBox.checkState() == Qt.Checked:
            self.video_flip = False
        elif self.ui.videoFlipCheckBox.checkState() == Qt.Unchecked:
            self.video_flip = True

    def onVideoStreamCheckBox_Changed(self):
        if self.ui.videoStreamCheckBox.checkState() == Qt.Checked:
            self.video_stream = True
        elif self.ui.videoStreamCheckBox.checkState() == Qt.Unchecked:
            self.video_stream = False

    def onMessageCheckBox_Changed(self):
        if self.ui.MessageCheckBox.checkState() == Qt.Checked:
            self.show_message = True
            self.ui.runtimeCheckBox.setChecked(True)
        elif self.ui.MessageCheckBox.checkState() == Qt.Unchecked:
            self.show_message = False
            self.ui.runtimeCheckBox.setChecked(False)

    def onSaveThresholdClicked(self):
        self.confThreshold = float(self.ui.confThreshold_Input.toPlainText())
        self.NMSThreshold = float(self.ui.NMSInput.toPlainText())

        msg = "confThreshold: " + self.ui.confThreshold_Input.toPlainText() + "\n" + "NMSThreshold: " + self.ui.NMSInput.toPlainText()
        QMessageBox.information(self, "Threshold Changed", msg)

    def onRunTimeCheckBox_Changed(self):
        if self.ui.runtimeCheckBox.checkState() == Qt.Checked:
            self.show_runtime = True
        elif self.ui.runtimeCheckBox.checkState() == Qt.Unchecked:
            self.show_runtime = False

    def onShowNamesCheckBox_Changed(self):
        if self.ui.showNames_checkbox.checkState() == Qt.Checked:
            self.showDetectedNames = True
        elif self.ui.showNames_checkbox.checkState() == Qt.Unchecked:
            self.showDetectedNames = False

    def onConfValueCheckBox_Changed(self):
        if self.ui.confValue_checkbox.checkState() == Qt.Checked:
            self.showDetectedConf = True
        elif self.ui.confValue_checkbox.checkState() == Qt.Unchecked:
            self.showDetectedConf = False

    def onShowBBoxCheckBox_Changed(self):
        if self.ui.showBBox_checkbox.checkState() == Qt.Checked:
            self.showBBox = True
        elif self.ui.showBBox_checkbox.checkState() == Qt.Unchecked:
            self.showBBox = False

    def say_hello(self):
        QMessageBox.information(self, 'About this software', 'Designed by Marco Cheung')

    def close_win(self):
        self.camera_capture.release()
        self.video_capture.release()
        cv2.destroyAllWindows()
        self.close()


class fromFilePage(QDialog):
    source_path = ''
    save_path = ''
    confThreshold = 0.9
    NMSThreshold = 0.4
    cfgFilePath = 'network/1.cfg'
    namesFilePath = 'network/1.names'
    weightsFilePath = 'network/1.weights'
    detected_frame = None
    showDetectedNames = False
    showDetectedConf = False
    showBBox = True
    fileDetect_net = None

    def __init__(self):
        QDialog.__init__(self)
        self.fromFileUI = fromFileUi_Dialog()
        self.fromFileUI.setupUi(self)

        self.fromFileUI.SelcPathBtn.clicked.connect(self.selectFilePath)
        self.fromFileUI.detect_btn.clicked.connect(self.detectPhoto)
        self.fromFileUI.segment_save.clicked.connect(self.segmentSave)
        self.fromFileUI.SavePathBtn.clicked.connect(self.selectSavingPath)
        self.fromFileUI.save_cap.clicked.connect(self.capSave)

        self.fromFileUI.cfgFileBtn.clicked.connect(self.selectCfgFile)
        self.fromFileUI.namesFileBtn.clicked.connect(self.selectNamesFile)
        self.fromFileUI.weightsFileBtn.clicked.connect(self.selectWeightsFile)
        self.fromFileUI.saveThresholdBtn.clicked.connect(self.setThreshold)

        self.fromFileUI.showNames_checkbox.stateChanged.connect(self.onShowNamesCheckBox_Changed)
        self.fromFileUI.confValue_checkbox.stateChanged.connect(self.onConfValueCheckBox_Changed)
        self.fromFileUI.showBBox_checkbox.stateChanged.connect(self.onShowBBoxCheckBox_Changed)

    def setThreshold(self):
        self.confThreshold = float(self.fromFileUI.confThreshold_Input.toPlainText())
        self.NMSThreshold = float(self.fromFileUI.NMSInput.toPlainText())
        msg = "confThreshold: " + self.fromFileUI.confThreshold_Input.toPlainText() + "\n" + "NMSThreshold: " + self.fromFileUI.NMSInput.toPlainText()
        QMessageBox.information(self, "Threshold Changed", msg)

    def selectCfgFile(self):
        self.cfgFilePath = QFileDialog.getOpenFileName(QDialog(), "Open .cfg File")
        if self.cfgFilePath[0] != 'network/1.cfg':
            self.fromFileUI.cfgFilePath_Label.setText("cfg: " + str(self.cfgFilePath[0]))

    def selectNamesFile(self):
        self.namesFilePath = QFileDialog.getOpenFileName(QDialog(), "Open .names File")
        if self.namesFilePath[0] != 'network/1.names':
            self.fromFileUI.namesFilePath_Label.setText("names: " + str(self.namesFilePath[0]))

    def selectWeightsFile(self):
        self.weightsFilePath = QFileDialog.getOpenFileName(QDialog(), "Open .weights File")
        if self.weightsFilePath[0] != 'network/1.weights':
            self.fromFileUI.weightsFilePath_Label.setText("weights: " + str(self.weightsFilePath[0]))

    def selectFilePath(self):
        self.source_path = QFileDialog.getOpenFileName(QDialog(), "Open Image Source File")
        # print("File DIR: " + str(source_image))
        if self.source_path[0] != '':
            self.fromFileUI.file_path_label.setText("Source: " + str(self.source_path[0]))
            frame = cv2.imread(self.source_path[0])
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.fromFileUI.original_image.setPixmap(QPixmap.fromImage(showImage))

    def selectSavingPath(self):
        self.save_path = QFileDialog.getExistingDirectory(QDialog(), "Choose Save Directory")

        if self.save_path != '':
            self.fromFileUI.savepath_label.setText(str(self.save_path))

    def detectPhoto(self):
        if self.source_path == '':
            QMessageBox.critical(self, 'Error', 'Please select original image first.')
        else:
            frame = cv2.imread(self.source_path[0])
            frame = cv2.resize(frame, (img_width, img_height))  # resolution setting: width x height

            classids, scores, bboxes = model.detect(frame, self.confThreshold, self.NMSThreshold)
            for class_id, score, bbox in zip(classids, scores, bboxes):
                x, y, w, h = bbox

                # get names of classes
                class_name = classes[class_id]

                if self.showBBox:
                    drawbbx(frame, x, y, w, h, class_name, score, self.showDetectedNames, self.showDetectedConf)

            self.detected_frame = frame
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.fromFileUI.result_image.setPixmap(QPixmap.fromImage(showImage))
            self.fromFileUI.result_image.setScaledContents(True)
            self.fromFileUI.notification.setText(str(len(bboxes)) + " Object(s) Detected")

    def segmentSave(self):
        if self.save_path == '':
            QMessageBox.critical(self, 'Error', 'Please select save path first.')
        else:
            frame = cv2.imread(self.source_path[0])
            frame = cv2.resize(frame, (img_width, img_height))

            segment_index = 1
            classids, scores, bboxes = model.detect(frame, self.confThreshold, self.NMSThreshold)
            for class_id, score, bbox in zip(classids, scores, bboxes):
                x, y, w, h = bbox

                # get names of classes
                class_name = classes[class_id]

                drawbbx(frame, x, y, w, h, class_name, score, self.showDetectedNames, self.showDetectedConf)
                cv2.imwrite(self.save_path + '/segment_%s.png' % str(segment_index), frame[y: y + h, x: x + w])
                segment_index = segment_index + 1
            # print(str(len(bboxes)) + " Object(s) Detected")
            self.fromFileUI.notification.setText(str(len(bboxes)) + " Object(s) Segment Saved")

    def capSave(self):
        if self.save_path == '':
            QMessageBox.critical(self, 'Error', 'Please select save path first.')
        else:
            cv2.imwrite(self.save_path + '/cap_%s.png' % str("capIndex"), self.detected_frame)
            self.fromFileUI.notification.setText("Capture Saved!")

    def onShowNamesCheckBox_Changed(self):
        if self.fromFileUI.showNames_checkbox.checkState() == Qt.Checked:
            self.showDetectedNames = True
        elif self.fromFileUI.showNames_checkbox.checkState() == Qt.Unchecked:
            self.showDetectedNames = False

    def onConfValueCheckBox_Changed(self):
        if self.fromFileUI.confValue_checkbox.checkState() == Qt.Checked:
            self.showDetectedConf = True
        elif self.fromFileUI.confValue_checkbox.checkState() == Qt.Unchecked:
            self.showDetectedConf = False

    def onShowBBoxCheckBox_Changed(self):
        if self.fromFileUI.showBBox_checkbox.checkState() == Qt.Checked:
            self.showBBox = True
        elif self.fromFileUI.showBBox_checkbox.checkState() == Qt.Unchecked:
            self.showBBox = False


if __name__ == '__main__':
    startTime = time.time()
    app = QtWidgets.QApplication(sys.argv)

    net = cv2.dnn.readNet(cfgDIR,
                          weightsDIR)  # for DIY YOLO Tiny
    # Define a object detection model and pass the params
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1 / 255)

    # Get lines from .names file
    classes = []  # use a list to store the names
    with open(namesDIR) as file_obj:
        # Get each line from .names file
        for class_name in file_obj.readlines():
            # delete enter and space from .names file
            class_name = class_name.strip()
            # append each name to the list
            classes.append(class_name)

    popup = StartUpPage()
    player = MainWindow()
    child = fromFilePage()

    popup.show()
    popup.StartUpUI.okBtn.clicked.connect(player.show)
    # After Click OK Button in StartUp Page, jump to mainpage and close StartupPage
    popup.StartUpUI.okBtn.clicked.connect(popup.close)
    popup.StartUpUI.exitBtn.clicked.connect(sys.exit)

    player.ui.fromFileBtn.clicked.connect(child.show)
    # player.show()
    sys.exit(app.exec_())
