#include "YOLOCPPSOCKETQt.h"
#include "ui_YOLOCPPSOCKETQt.h"
#include <QPushButton>
#include <QFileDialog>

#include <opencv2/core/core_c.h>
#include <opencv2/imgproc/imgproc_c.h>
#include <opencv2/photo/photo.hpp>
#include <opencv2/video/tracking.hpp>
#include <opencv2/objdetect/objdetect.hpp>
#include <highgui/highgui_c.h>
#include <string.h>
#include <string>
#include <json/json.h>
#include <time.h>

#pragma once
#include <fstream>
#include <sstream>
#include <iostream>
#include <opencv2/dnn.hpp>
#include <opencv2/core/cuda.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>

#include<WINSOCK2.H>
#include<STDIO.H>
#include<cstring>
#pragma comment(lib, "ws2_32.lib")

using namespace std;
using namespace cv;
using namespace dnn;

// Function Switch, 1 = on / true, 0 = off / false
// ===============================================
// JSON Configuration
int WriteJSON = 1;
#define JSONOnlyOne         1  // need to keep this open.
int outputJsonWriter = 0;
// Socket Configuration
int OpenSocket = 1;
char SocketServerAddress[255] = "127.0.0.1";  // N/A Currently
int SocketPort = 9999;
int outputSocketMessage = 0;
// Video Stream UI Configuration
int DisplayBoxX = 0;
int DisplayRunTime = 0;
// Video Configuration
int VideoStream = 1;
int VideoFlip = 1;
int VideoSize_width = 960;
int VideoSize_height = 540;
// YOLO network Configuration
int BackendGPU = 1;
float confThreshold = 0.9; // Confidence threshold
float nmsThreshold = 0.4;  // Non-maximum suppression threshold
string cfgFile = "./network/2.cfg";
string weightsFile = "./network/2.weights";
string namesFile = "./network/2.names";


// Initialize Json
Json::Value root;
Json::Value Detected;
Json::Value Objects;

YOLOCPPSOCKETQt::YOLOCPPSOCKETQt(QWidget *parent)
    : QMainWindow(parent)
{
    ui.setupUi(this);

	ui.output->append(" [!!!!!] Config [Open Socket] and [Use GPU + CUDA] and [YOLO Network Files] and [Threshold] First!");
	ui.output->append(" [!!!!!] All Pre-Start Settings Needed to be CONFIRM / set are colored in Red.");
	ui.output->append(" [!!!!!] Please Check Below Startup Configuration Carefully!\n");

	// Show Startup Configuration
	showStartupConfig();

	// Turn Checkboxes in RED Colour, warn the user to do the pre-start settings
	QPalette red;
	red.setColor(QPalette::WindowText, Qt::red);
	ui.openSocketCheckBox->setPalette(red);
	ui.useGPUCheckBox->setPalette(red);
	ui.yoloNetworkLabel->setPalette(red);
	ui.confThreshold_label->setPalette(red);
	ui.NMSThreshold_label->setPalette(red);

	// PushButtons Signal and Slots
    connect(ui.startBtn, SIGNAL(clicked()), this, SLOT(on_StartBtn_Clicked()));
	connect(ui.pauseBtn, SIGNAL(clicked()), this, SLOT(on_pauseBtn_Clicked()));
    connect(ui.exitBtn ,SIGNAL(clicked()), this, SLOT(on_ExitBtn_Clicked()));
	connect(ui.clearBtn, SIGNAL(clicked()), this, SLOT(on_clearBtn_Clicked()));

	connect(ui.saveAddrBtn, SIGNAL(clicked()), this, SLOT(on_saveAddrBtn_Clicked()));
	connect(ui.saveVideoSizeBtn, SIGNAL(clicked()), this, SLOT(on_saveVideoSizeBtn_Clicked()));
	connect(ui.saveThresholdBtn, SIGNAL(clicked()), this, SLOT(on_saveThresholdBtn_Clicked()));

	connect(ui.cfgFileBtn, SIGNAL(clicked()), this, SLOT(on_cfgFileBtn_Clicked()));
	connect(ui.weightsFileBtn, SIGNAL(clicked()), this, SLOT(on_weightsFileBtn_Clicked()));
	connect(ui.namesFileBtn, SIGNAL(clicked()), this, SLOT(on_namesFileBtn_Clicked()));

	
	// Check Box Signal and Slots
	connect(ui.writeJsonCheckBox, SIGNAL(stateChanged(int)), this, SLOT(on_writeJsonCheckBox_Changed(int)));
	connect(ui.logJsonCheckBox, SIGNAL(stateChanged(int)), this, SLOT(on_logJsonCheckBox_Changed(int)));
	
	connect(ui.openSocketCheckBox, SIGNAL(stateChanged(int)), this, SLOT(on_openSocketCheckBox_Changed(int)));
	connect(ui.logSocketCheckBox, SIGNAL(stateChanged(int)), this, SLOT(on_logSocketCheckBox_Changed(int)));

	connect(ui.videoStreamCheckBox, SIGNAL(stateChanged(int)), this, SLOT(on_videoStreamCheckBox_Changed(int)));
	connect(ui.videoFlipCheckBox, SIGNAL(stateChanged(int)), this, SLOT(on_videoFlipCheckBox_Changed(int)));
	connect(ui.boxXCheckBox, SIGNAL(stateChanged(int)), this, SLOT(on_BoxXCheckBox_Changed(int)));
	connect(ui.runtimeCheckBox, SIGNAL(stateChanged(int)), this, SLOT(on_runtimeCheckBox_Changed(int)));

	connect(ui.useGPUCheckBox, SIGNAL(stateChanged(int)), this, SLOT(on_useGPUCheckBox_Changed(int)));
}

void YOLOCPPSOCKETQt::showStartupConfig()
{
	if (WriteJSON == 1)
		ui.output->append("[1] Write Json: OPEN");
	else
		ui.output->append("[1] Write Json: CLOSED");

	if (outputJsonWriter == 1)
		ui.output->append("[2] Log Json: OPEN");
	else
		ui.output->append("[2] Log Json: CLOSED");

	if (OpenSocket == 1)
		ui.output->append("[3] Socket Communication: OPEN");
	else
		ui.output->append("[3] Socket Communication: CLOSED");

	string server_config = "[4] Socket Server Address: 127.0.0.1     Port: " + to_string(SocketPort);
	ui.output->append(QString::fromStdString(server_config));

	if (outputSocketMessage == 1)
		ui.output->append("[5] Log SocketMessage: OPEN");
	else
		ui.output->append("[5] Log SocketMessage: CLOSED");

	if (DisplayBoxX == 1)
		ui.output->append("[6] Display Box.X Coordinates: OPEN");
	else
		ui.output->append("[6] Display Box.X Coordinates: CLOSED");
	
	if (DisplayRunTime == 1)
		ui.output->append("[7] Display RunTime: OPEN");
	else
		ui.output->append("[7] Display RunTime: CLOSED");

	if (VideoStream == 1)
		ui.output->append("[8] OpenCV Video Stream: OPEN");
	else
		ui.output->append("[8] OpenCV Video Stream: CLOSED");

	if (VideoFlip == 1)
		ui.output->append("[9] OpenCV Video Flip: OPEN");
	else
		ui.output->append("[9] OpenCV Video Flip: CLOSED");
	
	if (BackendGPU == 1)
		ui.output->append("[10] Use GPU + CUDA: YES");
	else
		ui.output->append("[10] Use GPU + CUDA: NO");

	string videoSize_msg = "[11] Current Video Size: " + to_string(VideoSize_width) + " X " + to_string(VideoSize_height);
	ui.output->append(QString::fromStdString(videoSize_msg));
	
	string cfg_file_path = "[12] .cfg File in use: ";
	cfg_file_path.append(cfgFile);
	ui.output->append(QString::fromStdString(cfg_file_path));

	string weights_file_path = "[13] .weights_file_path File in use: ";
	weights_file_path.append(weightsFile);
	ui.output->append(QString::fromStdString(weights_file_path));

	string names_file_path = "[14] .names File in use: ";
	names_file_path.append(namesFile);
	ui.output->append(QString::fromStdString(names_file_path));

	string conf_str = "[15] Confident Threshold: ";
	conf_str.append(to_string(confThreshold));
	ui.output->append(QString::fromStdString(conf_str));

	string nms_str = "[16] NMS Threshold: ";
	nms_str.append(to_string(nmsThreshold));
	ui.output->append(QString::fromStdString(nms_str));

	ui.output->append("=============================================");
	ui.output->append("");

}

int YOLOCPPSOCKETQt::on_StartBtn_Clicked()
{
	// Socket Communication
	// Define the length of the message
	int send_len = 0;
	// Defining the send buffer
	char send_buf[100];
	// Define server-side sockets and accept request sockets
	SOCKET s_server;
	// server address
	SOCKADDR_IN server_addr;
	YOLOCPPSOCKETQt::socketInitialization();  // Here are some problems too
	// server-side information
	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.S_un.S_addr = inet_addr(SocketServerAddress);
	server_addr.sin_port = htons(SocketPort);
	// Create sockets
	s_server = socket(AF_INET, SOCK_STREAM, 0);
	if (::connect(s_server, (SOCKADDR*)&server_addr, sizeof(SOCKADDR)) == SOCKET_ERROR) {
		//cout << "Fail to establish connection to receiver." << endl;
		ui.output->append("Fail to establish connection to receiver.");
		WSACleanup();
	}
	else {
		//cout << "Successfully connect to receiver." << endl;
		ui.output->append("Successfully connect to receiver.");
	}

	if (OpenSocket == 0)
	{
		//cout << "\n[!!!] Socket initialized but Socket is set to CLOSED status.\n" << endl;
		ui.output->append("\n[!!!] Socket initialized but Socket is set to CLOSED status.\n");
	}
	else
		//cout << "Socket initialized and Socket Communication is OPEN." << endl;
		ui.output->append("Socket initialized and Socket Communication is OPEN.\n");

	
	// Get Object Name(s)
	vector<string> classes;  //for Object Name(s)
	String classesFile = namesFile;

	ifstream ifs(classesFile.c_str());
	string line;
	while (getline(ifs, line))
		classes.push_back(line);

	// Set net argvs
	//float confThreshold = 0.9; // Confidence threshold
	//float nmsThreshold = 0.4;  // Non-maximum suppression threshold
	int inpWidth = 416;        // Width of network's input image
	int inpHeight = 416;       // Height of network's input image

	// Define a YOLO net
	Net yolo_net;
	yolo_net = readNetFromDarknet(cfgFile, weightsFile);

	// Set OpenCV dnn Backend and Target
	if (BackendGPU == 0)
	{
		yolo_net.setPreferableBackend(DNN_BACKEND_OPENCV);
		yolo_net.setPreferableTarget(DNN_TARGET_CPU);
	}
	else if (BackendGPU == 1)
	{
		yolo_net.setPreferableBackend(DNN_BACKEND_CUDA);
		yolo_net.setPreferableTarget(DNN_TARGET_CUDA);
	}
	
	//Open USB Camera
	VideoCapture cap(0);
	if (!cap.isOpened())
	{
		cerr << "Couldn't open Camera." << endl;
		cap.release();
		return false;
	}
	Mat frame;

	clock_t start, finish; // Use these vars to record the YOLO processing time
	double tick_ori = static_cast<double>(getTickCount());  // Get Original Tick Count 
	int loopCount = 0;

	while (1)
	{
		// Calculate Programme Running Time
		double timex = static_cast<double>(getTickCount());
		timex = (timex - tick_ori) / getTickFrequency();  // now_tickCount - Original_Tick_Count = Program running time

		cap >> frame;
		if (frame.empty()) break;
		Size dsize = Size(VideoSize_width, VideoSize_height);  //Set Video Stream Resolution
		cv::resize(frame, frame, dsize, 0, 0, INTER_AREA);
		if (VideoFlip == 1)
		{
			flip(frame, frame, -1);
		}

		//Start timer, use to calculate how long does YOLOv4-Tiny process a frame
		start = clock();

		// Use YOLOv4-Tiny Net to Detect Object
		Mat blob;
		blobFromImage(frame, blob, 1 / 255.0, Size(inpWidth, inpHeight), Scalar(0, 0, 0), true, false);
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

		// Perform non maximum suppression to eliminate redundant overlapping boxes with
		// lower confidences
		vector<int> indices;
		NMSBoxes(boxes, confidences, confThreshold, nmsThreshold, indices);

		// End Timer
		finish = clock();
		double  duration;
		duration = (double)(finish - start);

		//Draw Predict Boxes
		if (indices.size() > 0)
		{
			// Object_Count * 2 value per Coord * 5_Coordinates
			//int* pRect = new int[indices.size() * 2 * 5];
			for (size_t i = 0; i < indices.size(); ++i)
			{
				int idx = indices[i];
				Rect box = boxes[idx];
				rectangle(frame, Point(box.x, box.y), Point(box.x + box.width, box.y + box.height), Scalar(0, 0, 255), 1);
				string label = format("%.2f", confidences[idx]);
				if (!classes.empty())
				{
					CV_Assert(classIds[idx] < (int)classes.size());
					label = classes[classIds[idx]] + ":" + label;
				}
				int baseLine;
				Size labelSize = getTextSize(label, FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);
				box.y = max(box.y, labelSize.height);
				putText(frame, label, Point(box.x, box.y), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(0, 255, 0), 1);
				std::string i_str = std::to_string(i + 1);
				putText(frame, i_str, Point(box.x + box.width, box.y), FONT_HERSHEY_SIMPLEX, 0.75, Scalar(0, 0, 255), 1);

				if (DisplayBoxX == 1)
				{
					// Output box.x coordinates on the frame
					putText(frame, "box.x: " + to_string(boxes[0].x), Point(20, 160), FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 0, 255), 2, 4);
				}

				if (WriteJSON == 1)
				{
					// Write Coordinates to coordinates.json using JSONCPP Library
					//writeFileJson(g_Obj, indices.size(), duration, pRect);

					int coordinatesArray[10] = { box.x, box.y , (box.x + box.width) , box.y , box.x , (box.y + box.height) ,
					(box.x + box.width) , (box.y + box.height) , (box.x + (box.width / 2)) , (box.y + (box.height / 2)) };

					for (int arrayIndx = 0; arrayIndx < 10; arrayIndx++)
					{
						Objects.append(coordinatesArray[arrayIndx]);
					}

					string detected_dst = "Object_" + to_string(i + 1);
					Detected[detected_dst] = Json::Value(Objects);
					Objects.clear();
				}

				if (OpenSocket == 1)
				{
					// Use String to send coordinates to receiver, but needs decoding process.
					String sendData;
					sendData += "Object_" + to_string(i + 1) + "\n[(";                                              // Object Count
					sendData += to_string(box.x) + "," + to_string(box.y) + ")-(";                                 // Point 1
					sendData += to_string(box.x + box.width) + "," + to_string(box.y) + ")-(";                    // Point 2
					sendData += to_string(box.x) + ", " + to_string(box.y + box.height) + ")-(";                 // Point 3
					sendData += to_string(box.x + box.width) + "," + to_string(box.y + box.height) + ")-(";      // Point 4
					sendData += to_string(box.x + (box.width / 2)) + "," + to_string(box.y + (box.height / 2)) + ")-";  // Point 5
					sendData += to_string((int)duration) + "]";      // Processing Time

					sendData += "\n";

					if (outputSocketMessage == 1)
						//cout << sendData << endl;
						ui.output->append(QString::fromStdString(sendData));
					strcpy(send_buf, sendData.c_str());
					send_len = send(s_server, send_buf, 100, 0);
				}

			}

			if (WriteJSON == 1) {
				string root_dst = "Detected_at_" + to_string(loopCount + 1);
				root[root_dst] = Detected;

				// JSON Styled Writer output
				if (outputJsonWriter == 1)
				{
					Json::StyledWriter sw;
					//cout << "StyledWriter:" << endl;
					//cout << sw.write(root) << endl << endl;
					ui.output->append("Styled Json Writer:\n");
					ui.output->append(QString::fromStdString(sw.write(root)));
					ui.output->append("\n\n");
				}
			}

		}

		// Put YOLO Processing Time and YOLO FPS to the frame
		putText(frame, "Delay: " + to_string((int)duration) + " ms", Point(20, 40), FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 0, 255), 2, 4);
		putText(frame, "FPS: " + to_string((int)(1000 / (int)duration)), Point(20, 80), FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 0, 255), 2, 4);
		loopCount++;

		if (DisplayRunTime == 1)
		{
			putText(frame, "RunTime: " + to_string((int)timex) + " s", Point(20, 120), FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 0, 255), 2, 4);
		}

		if (VideoStream == 1)
		{
			// Display Video Stream
			imshow("OpenCV DNN", frame);

			if (getWindowProperty("OpenCV DNN", WND_PROP_VISIBLE) < 1)
			{
				cap.release();
				break;
			}
		}

		if (WriteJSON == 1)
		{
			ofstream os;
			Json::StyledWriter sw;

			if (JSONOnlyOne == 1)
			{
				os.open("coordinates.json");  // Output coordinates of the last frame to json file only
			}
			else
			{
				os.open("coordinates.json", std::ios::out | std::ios::app);  // Output all coordinates in one .json file
			}
			if (!os.is_open())
				cout << "error: can not find or create the file which named \" coordinates.json\"." << endl;
			os << sw.write(root);
			os.close();

			//cout << "JSON DONE!" << endl;
		}

		if (waitKey(33) >= 0) break;
	}

	closesocket(s_server);
	WSACleanup();
	return 0;
}

void YOLOCPPSOCKETQt::socketInitialization() {
	// Initialize Socket Library 
	WORD w_req = MAKEWORD(2, 2);  // Version No.
	WSADATA wsadata;
	int err;
	err = WSAStartup(w_req, &wsadata);
	if (err != 0) {
		//cout << "Failed to initialize the socket library!" << endl;
		ui.output->append("Failed to initialize the socket library!");
	}
	else {
		//cout << "Initialization of socket library successful!" << endl;
		ui.output->append("Initialization of socket library successful!");
	}
	// check version
	if (LOBYTE(wsadata.wVersion) != 2 || HIBYTE(wsadata.wHighVersion) != 2) {
		//cout << "The socket library version number does not match!" << endl;
		ui.output->append("The socket library version number does not match!");
		WSACleanup();
	}
	else {
		//cout << "The socket library version is correct! " << endl;
		ui.output->append("The socket library version is correct!");
	}

}

void YOLOCPPSOCKETQt::on_pauseBtn_Clicked()
{
	system("pause");
}

void YOLOCPPSOCKETQt::on_ExitBtn_Clicked()
{
    exit(0);
}

void YOLOCPPSOCKETQt::on_clearBtn_Clicked()
{
	ui.output->clear();
}

void YOLOCPPSOCKETQt::on_saveAddrBtn_Clicked()
{
	string addr = (ui.socketAddrInput->toPlainText()).toStdString();
	// Write addr(string) to SocketServerAddress(char)
	memset(SocketServerAddress, '\0', sizeof(SocketServerAddress));
	strcpy(SocketServerAddress, addr.c_str());
	
	SocketPort = stoi((ui.socketPortInput->toPlainText()).toStdString());

	string msg = "Socket Address:Port is set to: ";
	msg.append(addr); msg.append(":");
	msg.append(to_string(SocketPort));
	ui.output->append(QString::fromStdString(msg));
}

void YOLOCPPSOCKETQt::on_saveVideoSizeBtn_Clicked()
{
	VideoSize_width = stoi((ui.widthInput->toPlainText()).toStdString());
	VideoSize_height = stoi((ui.heightInput->toPlainText()).toStdString());

	string msg = "VideoSize is set to: " + to_string(VideoSize_width) + " x " + to_string(VideoSize_height);
	ui.output->append(QString::fromStdString(msg));
}

void YOLOCPPSOCKETQt::on_saveThresholdBtn_Clicked()
{
	confThreshold = stof((ui.confThreshold_Input->toPlainText()).toStdString());
	nmsThreshold = stof((ui.NMSInput->toPlainText()).toStdString());

	string msg_conf = "confThreshold is set to: " + to_string(confThreshold);
	string msg_nms = "NMSThreshold is set to: " + to_string(nmsThreshold);
	ui.output->append(QString::fromStdString(msg_conf));
	ui.output->append(QString::fromStdString(msg_nms));
}

void YOLOCPPSOCKETQt::on_cfgFileBtn_Clicked()
{
	QString QcfgFilePath = QFileDialog::getOpenFileName(this, "Select .cfg File", "./");
	
	if (QcfgFilePath != "")
	{
		cfgFile = QcfgFilePath.toStdString();
		string msg = ".cfg File Selected at: " + cfgFile;
		ui.output->append(QString::fromStdString(msg));
	}

}

void YOLOCPPSOCKETQt::on_weightsFileBtn_Clicked()
{
	QString QweightsFilePath = QFileDialog::getOpenFileName(this, "Select .weights File", "./");

	if (QweightsFilePath != "")
	{
		weightsFile = QweightsFilePath.toStdString();
		string msg = ".weights File Selected at: " + weightsFile;
		ui.output->append(QString::fromStdString(msg));
	}
}

void YOLOCPPSOCKETQt::on_namesFileBtn_Clicked()
{
	QString QnamesFilePath = QFileDialog::getOpenFileName(this, "Select .names File", "./");
	
	if (QnamesFilePath != "")
	{
		namesFile = QnamesFilePath.toStdString();
		string msg = ".names File Selected at: " + namesFile;
		ui.output->append(QString::fromStdString(msg));
	}
}

void YOLOCPPSOCKETQt::on_writeJsonCheckBox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		WriteJSON = 1;
		ui.output->append("Write Json: set to OPEN");
	}
	else if (state == Qt::Unchecked)
	{
		WriteJSON = 0;
		ui.output->append("Write Json: set to CLOSED");
	}
}

void YOLOCPPSOCKETQt::on_logJsonCheckBox_Changed(int state)
{
	if (state == Qt::Checked) {
		outputJsonWriter = 1;
		ui.output->append("Log Json: set to OPEN");
	}
	else if (state == Qt::Unchecked)
	{
		outputJsonWriter = 0;
		ui.output->append("Log Json: set to CLOSED");
	}
}

void YOLOCPPSOCKETQt::on_openSocketCheckBox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		OpenSocket = 1;
		ui.output->append("Socket Communication: set to OPEN");
	}
	else if (state == Qt::Unchecked) {
		OpenSocket = 0;
		ui.output->append("Socket Communication: set to CLOSED");
	}
}

void YOLOCPPSOCKETQt::on_logSocketCheckBox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		outputSocketMessage = 1;
		ui.output->append("Log Socket: set to OPEN");
	}
	else if (state == Qt::Unchecked)
	{
		outputSocketMessage = 0;
		ui.output->append("Log Socket: set to CLOSED");
	}
}

void YOLOCPPSOCKETQt::on_videoStreamCheckBox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		VideoStream = 1;
		ui.output->append("OpenCV Video Stream: set to OPEN");
	}
	else if (state == Qt::Unchecked)
	{
		VideoStream = 0;
		ui.output->append("OpenCV Video Stream: set to CLOSED");
	}
}

void YOLOCPPSOCKETQt::on_videoFlipCheckBox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		VideoFlip = 1;
		ui.output->append("OpenCV Video Flip: set to OPEN");
	}
	else if (state == Qt::Unchecked)
	{
		VideoFlip = 0;
		ui.output->append("OpenCV Video Flip: set to CLOSED");
	}
}

void YOLOCPPSOCKETQt::on_BoxXCheckBox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		DisplayBoxX = 1;
		ui.output->append("Display Box.X Coordinates: set to OPEN");
	}
	else if (state == Qt::Unchecked)
	{
		DisplayBoxX = 0;
		ui.output->append("Display Box.X Coordinates: set to CLOSED");
	}
}

void YOLOCPPSOCKETQt::on_runtimeCheckBox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		DisplayRunTime = 1;
		ui.output->append("Display RunTime: set to OPEN");
	}
	else if (state == Qt::Unchecked)
	{
		DisplayRunTime = 0;
		ui.output->append("Display RunTime: set to CLOSED");
	}
}

void YOLOCPPSOCKETQt::on_useGPUCheckBox_Changed(int state)
{
	if (state == Qt::Checked)
	{
		BackendGPU = 1;
		ui.output->append("Use GPU + CUDA: set to YES");
	}
	else if (state == Qt::Unchecked)
	{
		BackendGPU = 0;
		ui.output->append("Use GPU + CUDA: set to NO");
	}
}
