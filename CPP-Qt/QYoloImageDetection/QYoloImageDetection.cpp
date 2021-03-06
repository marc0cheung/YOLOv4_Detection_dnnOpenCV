#include "QYoloImageDetection.h"
#include <QPushButton>
#include <QFileDialog>
#include <QMessageBox>

#include <opencv2/core/core_c.h>
#include <opencv2/imgproc/imgproc_c.h>
#include <opencv2/photo/photo.hpp>
#include <opencv2/video/tracking.hpp>
#include <opencv2/objdetect/objdetect.hpp>
#include <highgui/highgui_c.h>

#include <string.h>
#include <time.h>
#include <string>

#pragma once
#include <fstream>
#include <sstream>
#include <iostream>
#include <opencv2/dnn.hpp>
#include <opencv2/core/cuda.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>

#include <winsock.h>
#pragma comment(lib,"ws2_32.lib")
#pragma warning(disable:4996)
#include <thread>

using namespace std;
using namespace cv;
using namespace dnn;

Mat SourceImg;
string SourceImgPath = "";
string ResultSavePath = "";

// Function Switch
int ShowObjNames_Conf = 0;
int ShowBBox = 1;
int ShowObjectIndex = 0;
int openSocket = 0;
float confThreshold = 0.7;
float nmsThreshold = 0.4;
int test = 0;

String cfgFile = "./network/button_v2.cfg";
String weightsFile = "./network/button_v2.weights";
String namesFile = "./network/button_v2.names";

// YOLO Detection Function
Mat Detection(Mat frame);
void sendCoords(int nNum, int* pRectPoints);

QYoloImageDetection::QYoloImageDetection(QWidget *parent)
    : QMainWindow(parent)
{
    ui.setupUi(this);

    // CheckBox Signals and Slots
	connect(ui.showNames_checkbox, SIGNAL(stateChanged(int)), this, SLOT(on_showNames_checkbox_Changed(int)));
	connect(ui.objIndex_checkbox, SIGNAL(stateChanged(int)), this, SLOT(on_objIndex_checkbox_Changed(int)));
	connect(ui.showBBox_checkbox, SIGNAL(stateChanged(int)), this, SLOT(on_showBBox_checkbox_Changed(int)));
	connect(ui.openSocketCheckbox, SIGNAL(stateChanged(int)), this, SLOT(on_openSocketCheckbox_Changed(int)));

    // Push Button Signals and Slots
    connect(ui.SelcPathBtn, SIGNAL(clicked()), this, SLOT(on_SelcPathBtn_Selected()));
	connect(ui.detect_btn, SIGNAL(clicked()), this, SLOT(on_detect_btn_Selected()));
	connect(ui.saveThresholdBtn, SIGNAL(clicked()), this, SLOT(on_saveThresholdBtn_Selected()));
	connect(ui.SavePathBtn, SIGNAL(clicked()), this, SLOT(on_SavePathBtn_Selected()));

	connect(ui.save_cap, SIGNAL(clicked()), this, SLOT(on_save_cap_Selected()));
	connect(ui.segment_save, SIGNAL(clicked()), this, SLOT(on_segment_save_Selected()));

	// Select Yolo Network Files
	connect(ui.cfgFileBtn, SIGNAL(clicked()), this, SLOT(on_cfgFileBtn_Selected()));
	connect(ui.namesFileBtn, SIGNAL(clicked()), this, SLOT(on_namesFileBtn_Selected()));
	connect(ui.weightsFileBtn, SIGNAL(clicked()), this, SLOT(on_weightsFileBtn_Selected()));

	connect(ui.loopBtn, SIGNAL(clicked()), this, SLOT(on_loopBtn_Selected()));

}

// Select Source Image Path Manually
void QYoloImageDetection::on_SelcPathBtn_Selected()
{
	QString QSourceImagePath = QFileDialog::getOpenFileName(this, "Select Source Image", "./");

	if (QSourceImagePath != "")
	{
		SourceImgPath = QSourceImagePath.toStdString();
		ui.file_path_label->setText(QString::fromStdString(SourceImgPath));

		SourceImg = imread(QSourceImagePath.toStdString());
		imshow("Source Image", SourceImg);
	}
}

// Click "Go" Button to run YOLO Image Detection
void QYoloImageDetection::on_detect_btn_Selected()
{
	if (SourceImgPath == "")
	{
		QMessageBox::critical(NULL, "Detector Error", "Cannot Load Source Image", QMessageBox::Yes | QMessageBox::No, QMessageBox::Yes);
	}
	else
	{
		if ((cfgFile == "./network/button_v2.cfg") & (weightsFile == "./network/button_v2.weights") & (namesFile == "./network/button_v2.names"))
		{
			QMessageBox::information(NULL, "Haven't Set Darknet File", "Use Default Network Configuration: Button_v2", QMessageBox::Yes | QMessageBox::No, QMessageBox::Yes);
		}
		
		Mat frame = imread(SourceImgPath);

		frame = Detection(frame);

		// SHOW DETECTION RESULT
		imshow("Detection Result", frame);
	}
}

// Open Socket to receive and send coordinates in real-time
void QYoloImageDetection::on_openSocketCheckbox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		// If get frame input from socket -> start object dectection -> send object coordinates
		openSocket = 1;
		ui.notification->setText("Socket: OPEN");
	}
	else if (state == Qt::Unchecked)
	{
		openSocket = 0;
		ui.notification->setText("Socket: CLOSED");
	}
}

// Choose whether to display Object Names on the result image
void QYoloImageDetection::on_showNames_checkbox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		ShowObjNames_Conf = 1;
		ui.notification->setText("Show Label: OPEN");
	}
	else if (state == Qt::Unchecked)
	{
		ShowObjNames_Conf = 0;
		ui.notification->setText("Show Label: CLOSED");
	}
}

// Choose whether to display object index on the result image
void QYoloImageDetection::on_objIndex_checkbox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		ShowObjectIndex = 1;
		ui.notification->setText("Show Index: OPEN");
	}
	else if (state == Qt::Unchecked)
	{
		ShowObjectIndex = 0;
		ui.notification->setText("Show Index: CLOSED");
	}
}

// Choose whether to display bounding box on the result image
void QYoloImageDetection::on_showBBox_checkbox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		ShowBBox = 1;
		ui.notification->setText("Show BBox: OPEN");
	}
	else if (state == Qt::Unchecked)
	{
		ShowBBox = 0;
		ui.notification->setText("Show BBox: CLOSED");
	}
}

// Save the 2 threshold values from the InputBoxes
void QYoloImageDetection::on_saveThresholdBtn_Selected()
{
	confThreshold = stof((ui.confThreshold_Input->toPlainText()).toStdString());
	nmsThreshold = stof((ui.NMSInput->toPlainText()).toStdString());
	
	string threshold_msg = "Conf: " + to_string(confThreshold) + ", NMS: " + to_string(nmsThreshold);
	ui.notification->setText(QString::fromStdString(threshold_msg));
}

// Select saving path of the Result Image
void QYoloImageDetection::on_SavePathBtn_Selected()
{
	QString QSavePath = QFileDialog::getExistingDirectory();
	if (QSavePath != "")
	{
		ui.savepath_label->setText(QSavePath);
		ResultSavePath = QSavePath.toStdString();
	}
}

// Click "SaveCap" Button to save the whole result image
void QYoloImageDetection::on_save_cap_Selected()
{
	if (SourceImgPath == "")
	{
		QMessageBox::critical(NULL, "Detector Error", "Cannot Load Source Image", QMessageBox::Yes | QMessageBox::No, QMessageBox::Yes);
	}
	else
	{
		// get detection result
		Mat frame = imread(SourceImgPath);

		vector<string> classes;
		String classesFile = namesFile;

		ifstream ifs(classesFile.c_str());
		string line;
		while (getline(ifs, line))
			classes.push_back(line);

		Net yolo_net;
		// yolo_net = readNetFromDarknet("./network/button_v2.cfg", "./network/button_v2.weights");
		yolo_net = readNetFromDarknet(cfgFile, weightsFile);
		yolo_net.setPreferableBackend(DNN_BACKEND_OPENCV);
		yolo_net.setPreferableTarget(DNN_TARGET_CPU);

		// Use YOLOv4-Tiny Net to Detect Object
		Mat blob;
		blobFromImage(frame, blob, 1 / 255.0, Size(416, 416), Scalar(0, 0, 0), true, false);
		yolo_net.setInput(blob);

		vector<Mat> outs;
		yolo_net.forward(outs, yolo_net.getUnconnectedOutLayersNames());

		// Postprocess(frame, outs)
		vector<int> classIds;
		vector<float> confidences;
		vector<Rect> boxes;

		for (size_t i = 0; i < outs.size(); ++i)
		{
			// Scan through all the bounding boxes output from the network and keep only the
			// ones with high confidence scores. Assign the box's class label as the class
			// with the highest score for the box.
			float* data = (float*)outs[i].data;
			for (int j = 0; j < outs[i].rows; ++j, data += outs[i].cols)
			{
				Mat scores = outs[i].row(j).colRange(5, outs[i].cols);
				Point classIdPoint;
				double confidence;
				// Get the value and location of the maximum score
				minMaxLoc(scores, 0, &confidence, 0, &classIdPoint);
				if (confidence > confThreshold)
				{
					int centerX = (int)(data[0] * frame.cols);
					int centerY = (int)(data[1] * frame.rows);
					int width = (int)(data[2] * frame.cols);
					int height = (int)(data[3] * frame.rows);
					int left = centerX - width / 2;
					int top = centerY - height / 2;

					classIds.push_back(classIdPoint.x);
					confidences.push_back((float)confidence);
					boxes.push_back(Rect(left, top, width, height));
				}
			}
		}

		vector<int> indices;
		NMSBoxes(boxes, confidences, confThreshold, nmsThreshold, indices);

		// Draw Predict Boxes
		if (indices.size() > 0)
		{
			string notify_msg = to_string(indices.size()) + " Object Detected.";
			ui.notification->setText(QString::fromStdString(notify_msg));

			// Object_Count * 2 value per Coord * 5_Coordinates
			int* pRect = new int[indices.size() * 2 * 5];
			for (size_t i = 0; i < indices.size(); ++i)
			{
				int idx = indices[i];
				Rect box = boxes[idx];

				if (ShowBBox == 1)
				{
					rectangle(frame, Point(box.x, box.y), Point(box.x + box.width, box.y + box.height), Scalar(0, 0, 255), 1);
				}

				string label = format("%.2f", confidences[idx]);
				if (!classes.empty())
				{
					CV_Assert(classIds[idx] < (int)classes.size());
					label = classes[classIds[idx]] + ":" + label;
				}
				int baseLine;
				Size labelSize = getTextSize(label, FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);
				box.y = max(box.y, labelSize.height);

				if (ShowObjNames_Conf == 1)
				{
					putText(frame, label, Point(box.x, box.y), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(0, 255, 0), 1);
				}

				std::string i_str = std::to_string(i + 1);

				if (ShowObjectIndex == 1)
				{
					putText(frame, i_str, Point(box.x + box.width, box.y), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(0, 0, 255), 1);
				}

				// save each target's coordinates to pRect
				// Point 1
				pRect[i * 10 + 0] = box.x;
				pRect[i * 10 + 1] = box.y;
				// Point 2
				pRect[i * 10 + 2] = box.x + box.width;
				pRect[i * 10 + 3] = box.y;
				// Point 3
				pRect[i * 10 + 4] = box.x;
				pRect[i * 10 + 5] = box.y + box.height;
				// Point 4
				pRect[i * 10 + 6] = box.x + box.width;
				pRect[i * 10 + 7] = box.y + box.height;
				// Center Point
				pRect[i * 10 + 8] = (int)((box.x + box.width) / 2);
				pRect[i * 10 + 9] = (int)((box.y + box.height) / 2);

			}
			if (openSocket == 1)
				sendCoords(indices.size(), pRect);

			delete[]pRect;
		}
		// imshow and imwrite
		imshow("Detection Result", frame);

		if (ResultSavePath != "")
		{
			imwrite(ResultSavePath + "/Result.png", frame);
			ui.notification->setText("Detection Result Saved.");
		}
		else
		{
			QMessageBox::critical(NULL, "Save Result Error", "Haven't Select Save Path", QMessageBox::Yes | QMessageBox::No, QMessageBox::Yes);
		}
	}
}

// Click "Segment_Save" Button to save each segment(s) of the target object(s)
void QYoloImageDetection::on_segment_save_Selected()
{
	// get object segment
	if (SourceImgPath == "")
	{
		QMessageBox::critical(NULL, "Detector Error", "Cannot Load Source Image", QMessageBox::Yes | QMessageBox::No, QMessageBox::Yes);
	}
	else
	{
		if ((cfgFile == "./network/button_v2.cfg") & (weightsFile == "./network/button_v2.weights") & (namesFile == "./network/button_v2.names"))
		{
			QMessageBox::information(NULL, "Haven't Set Darknet File", "Use Default Network Configuration: Button_v2", QMessageBox::Yes | QMessageBox::No, QMessageBox::Yes);
		}

		Mat frame = imread(SourceImgPath);

		vector<string> classes;
		String classesFile = namesFile;

		ifstream ifs(classesFile.c_str());
		string line;
		while (getline(ifs, line))
			classes.push_back(line);

		Net yolo_net;
		// yolo_net = readNetFromDarknet("./network/button_v2.cfg", "./network/button_v2.weights");
		yolo_net = readNetFromDarknet(cfgFile, weightsFile);
		yolo_net.setPreferableBackend(DNN_BACKEND_OPENCV);
		yolo_net.setPreferableTarget(DNN_TARGET_CPU);

		// Use YOLOv4-Tiny Net to Detect Object
		Mat blob;
		blobFromImage(frame, blob, 1 / 255.0, Size(416, 416), Scalar(0, 0, 0), true, false);
		yolo_net.setInput(blob);

		vector<Mat> outs;
		yolo_net.forward(outs, yolo_net.getUnconnectedOutLayersNames());

		// Postprocess(frame, outs)
		vector<int> classIds;
		vector<float> confidences;
		vector<Rect> boxes;

		for (size_t i = 0; i < outs.size(); ++i)
		{
			// Scan through all the bounding boxes output from the network and keep only the
			// ones with high confidence scores. Assign the box's class label as the class
			// with the highest score for the box.
			float* data = (float*)outs[i].data;
			for (int j = 0; j < outs[i].rows; ++j, data += outs[i].cols)
			{
				Mat scores = outs[i].row(j).colRange(5, outs[i].cols);
				Point classIdPoint;
				double confidence;
				// Get the value and location of the maximum score
				minMaxLoc(scores, 0, &confidence, 0, &classIdPoint);
				if (confidence > confThreshold)
				{
					int centerX = (int)(data[0] * frame.cols);
					int centerY = (int)(data[1] * frame.rows);
					int width = (int)(data[2] * frame.cols);
					int height = (int)(data[3] * frame.rows);
					int left = centerX - width / 2;
					int top = centerY - height / 2;

					classIds.push_back(classIdPoint.x);
					confidences.push_back((float)confidence);
					boxes.push_back(Rect(left, top, width, height));
				}
			}
		}

		vector<int> indices;
		NMSBoxes(boxes, confidences, confThreshold, nmsThreshold, indices);


		// Draw Predict Boxes
		if (indices.size() > 0)
		{
			string notify_msg = to_string(indices.size()) + " Object Detected.";
			ui.notification->setText(QString::fromStdString(notify_msg));

			// Object_Count * 2 value per Coord * 5_Coordinates
			int* pRect = new int[indices.size() * 2 * 5];
			for (size_t i = 0; i < indices.size(); ++i)
			{
				int idx = indices[i];
				Rect box = boxes[idx];

				if (ShowBBox == 1)
				{
					rectangle(frame, Point(box.x, box.y), Point(box.x + box.width, box.y + box.height), Scalar(0, 0, 255), 1);
				}

				string label = format("%.2f", confidences[idx]);
				if (!classes.empty())
				{
					CV_Assert(classIds[idx] < (int)classes.size());
					label = classes[classIds[idx]] + ":" + label;
				}
				int baseLine;
				Size labelSize = getTextSize(label, FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);
				box.y = max(box.y, labelSize.height);

				if (ShowObjNames_Conf == 1)
				{
					putText(frame, label, Point(box.x, box.y), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(0, 255, 0), 1);
				}

				std::string i_str = std::to_string(i + 1);

				if (ShowObjectIndex == 1)
				{
					putText(frame, i_str, Point(box.x + box.width, box.y), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(0, 0, 255), 1);
				}

				Rect roi_selector = Rect(box.x, box.y, box.width, box.height);
				//imshow("Segment_" + to_string(i), frame(roi_selector));
				
				// Pop up Error while no Save Path Selected
				if (ResultSavePath == "")
				{
					QMessageBox::critical(NULL, "Segment Save Error", "No Save Path Selected!", QMessageBox::Yes | QMessageBox::No, QMessageBox::Yes);
					ui.notification->setText("Segment Save Error!");
					break;
				}
				else
				{
					imwrite(ResultSavePath + "/Segment_" + to_string(i) + ".png", frame(roi_selector));
					ui.notification->setText("Segment Saved!");
				}

				// save each target's coordinates to pRect
				// Point 1
				pRect[i * 10 + 0] = box.x;
				pRect[i * 10 + 1] = box.y;
				// Point 2
				pRect[i * 10 + 2] = box.x + box.width;
				pRect[i * 10 + 3] = box.y;
				// Point 3
				pRect[i * 10 + 4] = box.x;
				pRect[i * 10 + 5] = box.y + box.height;
				// Point 4
				pRect[i * 10 + 6] = box.x + box.width;
				pRect[i * 10 + 7] = box.y + box.height;
				// Center Point
				pRect[i * 10 + 8] = (int)((box.x + box.width) / 2);
				pRect[i * 10 + 9] = (int)((box.y + box.height) / 2);

			}
			if (openSocket == 1)
				sendCoords(indices.size(), pRect);

			delete[]pRect;
		}

		imshow("Detected Result", frame);
	}
}

// Select .cfg file of darknet
void QYoloImageDetection::on_cfgFileBtn_Selected()
{
	QString QcfgPath = QFileDialog::getOpenFileName();
	if (QcfgPath != "")
	{
		ui.cfgFilePath_Label->setText(QcfgPath);
		// set global cfg file path
		cfgFile = QcfgPath.toStdString();
	}
}

// Select .names file of darknet
void QYoloImageDetection::on_namesFileBtn_Selected()
{
	QString QnamesPath = QFileDialog::getOpenFileName();
	if (QnamesPath != "")
	{
		ui.namesFilePath_Label->setText(QnamesPath);
		// set global .names file path
		namesFile = QnamesPath.toStdString();
	}
}

// Select .weights file of darknet
void QYoloImageDetection::on_weightsFileBtn_Selected()
{
	QString QweightsPath = QFileDialog::getOpenFileName();
	if (QweightsPath != "")
	{
		ui.weightsFilePath_Label->setText(QweightsPath);
		// set global .weights file path
		weightsFile = QweightsPath.toStdString();
	}
}

void QYoloImageDetection::Socket_SendCoord(string sendData)
{
	int send_len = 0;
	int recv_len = 0;

	char send_buf[1024];
	strcpy(send_buf, sendData.c_str());
	//char recv_len[100];

	SOCKET s_server;
	SOCKADDR_IN server_addr;

	WORD wVersion = MAKEWORD(2, 2);
	WSADATA wsadata;
	if (WSAStartup(wVersion, &wsadata) != 0)
	{
		ui.notification->setText("WSA StartUp Error");
	}

	SOCKET s = socket(AF_INET, SOCK_STREAM, 0);
	if (s == INVALID_SOCKET)
	{
		ui.notification->setText("Invalid Socket.");
	}

	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	server_addr.sin_port = htons(1234);

	s_server = socket(AF_INET, SOCK_STREAM, 0);

	if (::connect(s_server, (SOCKADDR*)&server_addr, sizeof(SOCKADDR)) == SOCKET_ERROR) {
		ui.notification->setText("Connect Error");
		WSACleanup();
	}

	send_len = send(s_server, send_buf, 100, 0);
	if (send_len < 0)
	{
		ui.notification->setText("send error");
	}

	closesocket(s_server);
	WSACleanup();
}

void QYoloImageDetection::on_loopBtn_Selected()
{
	// Initialize Socket Connection
	int recv_len = 0;
	char recv_buf[2048];

	SOCKET s_server;
	SOCKADDR_IN server_addr;

	WORD wVersion = MAKEWORD(2, 2);
	WSADATA wsadata;
	if (WSAStartup(wVersion, &wsadata) != 0)
	{
		cout << "WSA StartUp Error" << endl;
	}

	SOCKET s = socket(AF_INET, SOCK_STREAM, 0);
	if (s == INVALID_SOCKET)
	{
		cout << "Invalid Socket." << endl;
	}

	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	server_addr.sin_port = htons(1234);

	s_server = socket(AF_INET, SOCK_STREAM, 0);

	if (::connect(s_server, (SOCKADDR*)&server_addr, sizeof(SOCKADDR)) == SOCKET_ERROR) {
		cout << "Connect Error" << endl;
		WSACleanup();
	}
	
	while (true)
	{
		memset(recv_buf, '\0', sizeof(recv_buf));
		//test = test + 1;
		recv(s_server, recv_buf, sizeof(recv_buf) + 1, 0);  // BUG Here: Blocked if did not receive path_message
		string recv_string = recv_buf;
		string headerMessage = recv_string.substr(0, 5);    // Should be "path:"
		string pathFromSocket = recv_string.substr(5, recv_string.length());  // Get rid of the socket message header "path:"

		if (headerMessage == "path:")
		{
			// if receive source image path -> detection start -> send coordinates via socket
			if ((cfgFile == "./network/button_v2.cfg") & (weightsFile == "./network/button_v2.weights") & (namesFile == "./network/button_v2.names"))
			{
				QMessageBox::information(NULL, "Haven't Set Darknet File", "Use Default Network Configuration: Button_v2", QMessageBox::Yes | QMessageBox::No, QMessageBox::Yes);
			}

			Mat frame = imread(pathFromSocket);

			frame = Detection(frame);

			// SHOW DETECTION RESULT
			imshow("Detection Result", frame);

			ui.notification->setText(QString::fromStdString(pathFromSocket));
		}

		QApplication::processEvents(QEventLoop::AllEvents, 500);  // Keep Qt Window Alive
	}
}

QYoloImageDetection::~QYoloImageDetection()
{}

// Use Yolo Network for object detection
Mat Detection(Mat frame)
{
	vector<string> classes;
	String classesFile = namesFile;

	ifstream ifs(classesFile.c_str());
	string line;
	while (getline(ifs, line))
		classes.push_back(line);

	// Load Yolo network
	Net yolo_net;
	yolo_net = readNetFromDarknet(cfgFile, weightsFile);
	yolo_net.setPreferableBackend(DNN_BACKEND_OPENCV);
	yolo_net.setPreferableTarget(DNN_TARGET_CPU);

	// Use YOLOv4-Tiny Net to Detect Object
	Mat blob;
	blobFromImage(frame, blob, 1 / 255.0, Size(416, 416), Scalar(0, 0, 0), true, false);
	yolo_net.setInput(blob);

	vector<Mat> outs;
	yolo_net.forward(outs, yolo_net.getUnconnectedOutLayersNames());

	// Postprocess(frame, outs)
	vector<int> classIds;
	vector<float> confidences;
	vector<Rect> boxes;

	for (size_t i = 0; i < outs.size(); ++i)
	{
		// Scan through all the bounding boxes output from the network and keep only the
		// ones with high confidence scores. Assign the box's class label as the class
		// with the highest score for the box.
		float* data = (float*)outs[i].data;
		for (int j = 0; j < outs[i].rows; ++j, data += outs[i].cols)
		{
			Mat scores = outs[i].row(j).colRange(5, outs[i].cols);
			Point classIdPoint;
			double confidence;
			// Get the value and location of the maximum score
			minMaxLoc(scores, 0, &confidence, 0, &classIdPoint);
			if (confidence > confThreshold)
			{
				int centerX = (int)(data[0] * frame.cols);
				int centerY = (int)(data[1] * frame.rows);
				int width = (int)(data[2] * frame.cols);
				int height = (int)(data[3] * frame.rows);
				int left = centerX - width / 2;
				int top = centerY - height / 2;

				classIds.push_back(classIdPoint.x);
				confidences.push_back((float)confidence);
				boxes.push_back(Rect(left, top, width, height));
			}
		}
	}

	vector<int> indices;
	NMSBoxes(boxes, confidences, confThreshold, nmsThreshold, indices);


	// Draw Predict Boxes
	if (indices.size() > 0)
	{
		// string notify_msg = to_string(indices.size()) + " Object Detected.";
		// ui.notification->setText(QString::fromStdString(notify_msg));

		// Object_Count * 2 value per Coord * 5_Coordinates per Obj
		int* pRect = new int[indices.size() * 2 * 5];
		
		for (size_t i = 0; i < indices.size(); ++i)
		{
			int idx = indices[i];
			Rect box = boxes[idx];

			if (ShowBBox == 1)
			{
				rectangle(frame, Point(box.x, box.y), Point(box.x + box.width, box.y + box.height), Scalar(0, 0, 255), 1);
			}

			string label = format("%.2f", confidences[idx]);
			if (!classes.empty())
			{
				CV_Assert(classIds[idx] < (int)classes.size());
				label = classes[classIds[idx]] + ":" + label;
			}
			int baseLine;
			Size labelSize = getTextSize(label, FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);
			box.y = max(box.y, labelSize.height);

			if (ShowObjNames_Conf == 1)
			{
				putText(frame, label, Point(box.x, box.y), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(0, 255, 0), 1);
			}

			std::string i_str = std::to_string(i + 1);

			if (ShowObjectIndex == 1)
			{
				putText(frame, i_str, Point(box.x + box.width, box.y), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(0, 0, 255), 1);
			}

			// save each target's coordinates to pRect
			// Point 1
			pRect[i * 10 + 0] = box.x;
			pRect[i * 10 + 1] = box.y;
			// Point 2
			pRect[i * 10 + 2] = box.x + box.width;
			pRect[i * 10 + 3] = box.y;
			// Point 3
			pRect[i * 10 + 4] = box.x;
			pRect[i * 10 + 5] = box.y + box.height;
			// Point 4
			pRect[i * 10 + 6] = box.x + box.width;
			pRect[i * 10 + 7] = box.y + box.height;
			// Center Point
			pRect[i * 10 + 8] = (int)((box.x + box.width) / 2);
			pRect[i * 10 + 9] = (int)((box.y + box.height) / 2);


			// strcpy(send_buf, sendData.c_str());
			// send_len = send(s_server, send_buf, 100, 0);

		}
		if (openSocket == 1)
			sendCoords(indices.size(), pRect);
		
		delete[]pRect;
	}
	return frame;
}

void sendCoords(int nNum, int* pRectPoints)
{
	int send_len = 0;
	char send_buf[2048];

	SOCKET s_server;
	SOCKADDR_IN server_addr;

	WORD wVersion = MAKEWORD(2, 2);
	WSADATA wsadata;
	if (WSAStartup(wVersion, &wsadata) != 0)
	{
		cout << "WSA StartUp Error" << endl;
	}

	SOCKET s = socket(AF_INET, SOCK_STREAM, 0);
	if (s == INVALID_SOCKET)
	{
		cout << "Invalid Socket." << endl;
	}

	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	server_addr.sin_port = htons(1234);

	s_server = socket(AF_INET, SOCK_STREAM, 0);

	if (::connect(s_server, (SOCKADDR*)&server_addr, sizeof(SOCKADDR)) == SOCKET_ERROR) {
		cout << "Connect Error" << endl;
		WSACleanup();
	}

	for (int i = 0; i < nNum; i++)
	{
		string targetMsg = "[" + to_string(i+1) + ",(" + to_string(pRectPoints[i * 10 + 0]) + "," + to_string(pRectPoints[i * 10 + 1]) + "),(" +
			to_string(pRectPoints[i * 10 + 2]) + "," + to_string(pRectPoints[i * 10 + 3]) + "),(" +
			to_string(pRectPoints[i * 10 + 4]) + "," + to_string(pRectPoints[i * 10 + 5]) + "),(" +
			to_string(pRectPoints[i * 10 + 6]) + "," + to_string(pRectPoints[i * 10 + 7]) + "),(" +
			to_string(pRectPoints[i * 10 + 8]) + "," + to_string(pRectPoints[i * 10 + 9]) + ")]\n";
		
		strcpy(send_buf, strdup(targetMsg.c_str()));
		send_len = send(s_server, send_buf, strlen(send_buf) + 1, 0);
	}

	
	if (send_len < 0)
	{
		cout << "send error" << endl;
	}

	closesocket(s_server);
	WSACleanup();

}
