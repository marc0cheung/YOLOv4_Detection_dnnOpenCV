# -*- coding: utf-8 -*-
# yolov4-tiny Object Detection (RealTime Video Stream but use Image Detection to segment ROIs from each frame)
import time
import cv2
import sys
from PySide2 import QtCore, QtGui, QtWidgets
import qimage2ndarray

from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QRect

from ui_yolov4 import Ui_MainWindow
from ui_fromFileDialog import Ui_Dialog

imgNum = 0
FileDirectory = ''
img_width = 416
img_height = 416


def drawbbx(img, x, y, w, h, predName, score):
    colorline = (0, 255, 0)  # angerline colour
    angerline = 13  # angerline length
    # Draw Detection Boxes
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 1)
    # angerline beautify
    cv2.line(img, (x, y), (x + angerline, y), colorline, 2)
    cv2.line(img, (x, y), (x, y + angerline), colorline, 2)
    cv2.line(img, (x + w, y), (x + w, y + angerline), colorline, 2)
    cv2.line(img, (x + w, y), (x + w - angerline, y), colorline, 2)
    cv2.line(img, (x, y + h), (x, y + h - angerline), colorline, 2)
    cv2.line(img, (x, y + h), (x + angerline, y + h), colorline, 2)
    cv2.line(img, (x + w, y + h), (x + w, y + h - angerline), colorline, 2)
    cv2.line(img, (x + w, y + h), (x + w - angerline, y + h), colorline, 2)

    # Show predict category 显示预测的类别
    cv2.putText(img, predName, (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # Show Predict percentage 显示预测概率
    cv2.putText(img, str(int(score * 100)) + '%', (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)


class MainWindow(QMainWindow):
    pause = False
    video = False
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

        # Object Detection Starts
        T1 = time.perf_counter()
        classids, scores, bboxes = model.detect(frame, 0.8, 0.3)
        for class_id, score, bbox in zip(classids, scores, bboxes):
            # 获取检测框的左上角坐标和宽高
            # Get the coordinates of the top left corner of the detection box and the width and height
            x, y, w, h = bbox

            # 获取检测框对应的分类名
            # Get the name of the category corresponding to the detection box
            class_name = classes[class_id]

            drawbbx(frame, x, y, w, h, class_name, score)

        T2 = time.perf_counter()  # Detection Complete Time 检测完毕时间节点
        cv2.putText(frame, str("RT: ") + str(int((T2 - T1) * 1000)) + str('ms'), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (0, 0, 255), 2)
        cv2.putText(frame, str("FPS: 30"), (10, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, str("YOLO FPS: ") + str(int(1000 / ((T2 - T1) * 1000))), (10, 150), cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (0, 0, 255), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = qimage2ndarray.array2qimage(frame)
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(image))
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

                class_name = classes[class_id]

                drawbbx(frame, x, y, w, h, class_name, score)
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

                class_name = classes[class_id]

                drawbbx(frame, x, y, w, h, class_name, score)

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
    detected_frame = None

    def __init__(self):
        QDialog.__init__(self)
        self.fromFileUI = Ui_Dialog()
        self.fromFileUI.setupUi(self)

        self.fromFileUI.SelcPathBtn.clicked.connect(self.selectFilePath)
        self.fromFileUI.detect_btn.clicked.connect(self.detectPhoto)
        self.fromFileUI.segment_save.clicked.connect(self.segmentSave)
        self.fromFileUI.SavePathBtn.clicked.connect(self.selectSavingPath)
        self.fromFileUI.save_cap.clicked.connect(self.capSave)

    def selectFilePath(self):
        self.source_path = QFileDialog.getOpenFileName(QDialog(), "Open Image Source File")
        # print("File DIR: " + str(source_image))
        self.fromFileUI.file_path_label.setText("Source: " + str(self.source_path[0]))
        frame = cv2.imread(self.source_path[0])
        show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        self.fromFileUI.original_image.setPixmap(QPixmap.fromImage(showImage))

    def selectSavingPath(self):
        self.save_path = QFileDialog.getExistingDirectory(QDialog(), "Choose Save Directory")
        self.fromFileUI.savepath_label.setText(str(self.save_path))

    def detectPhoto(self):
        if self.source_path == '':
            QMessageBox.critical(self, 'Error', 'Please select original image first.')
        else:
            frame = cv2.imread(self.source_path[0])
            frame = cv2.resize(frame, (img_width, img_height))  # resolution setting: width x height

            classids, scores, bboxes = model.detect(frame, 0.8, 0.3)
            for class_id, score, bbox in zip(classids, scores, bboxes):
                x, y, w, h = bbox

                class_name = classes[class_id]

                drawbbx(frame, x, y, w, h, class_name, score)

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
            classids, scores, bboxes = model.detect(frame, 0.8, 0.3)
            for class_id, score, bbox in zip(classids, scores, bboxes):
                x, y, w, h = bbox

                class_name = classes[class_id]

                drawbbx(frame, x, y, w, h, class_name, score)
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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    net = cv2.dnn.readNet('yolo-tiny-random\\remote_tiny.cfg',
                          'yolo-tiny-random\\weights\\remote_tiny_final.weights')  # for Self-trained YOLO Tiny
    # 定义一个目标检测模型，将模型传进去
    # Define a object detection model and pass in the net config
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1 / 255)

    # （2）获取分类文本的信息
    #  (2) Get lines(category names) on .names file
    classes = []  # list use to save category names
    with open('yolo-tiny\\remote_tiny.names') as file_obj:
        for class_name in file_obj.readlines():
            # Remove line breaks, spaces, etc. from text
            class_name = class_name.strip()
            # append each category name to a list 将每个分类名保存到列表中
            classes.append(class_name)

    player = MainWindow()
    child = fromFilePage()
    player.ui.fromFileBtn.clicked.connect(child.show)
    player.show()
    sys.exit(app.exec_())
