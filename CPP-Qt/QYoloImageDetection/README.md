# QYoloImageDetection

<br>

**Select Language:** English | [Simplified Chinese]()

<br>

<div align="center"><img src="https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/raw/main/CPP-Qt/QYoloImageDetection/README.assets/ImageDetectionMainpage.png" alt="ImageDetectionMainpage" width="700px"></div>

<br>

An Image Object Detector based on C++ and Qt 5.15.0. Using OpenCV `dnn` module to read net files from Darknet. 

<br>

**Support:**

- Darknet `.cfg` , `.names` and `.weights` files.
- Confidential and Non-maximum Suppression Threshold Configuration
- Result Display Info Configuration
- Object segment and Save segment result
- Save Detection Result
- Send target object coordinates using Socket Communication at 127.0.0.1, Port 1234

<br>

**Features on the drawing board:**

- Receive Mat data from other application via Socket Communication
- Keep Socket Communication listening at the background using multi-thread method as Socket client

<br>

## Diagram of this Application

<div align="center"><img src="https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/raw/main/CPP-Qt/QYoloImageDetection/README.assets/diagram.png" alt="diagram" width="1200px" /></div>

<br>

## How to Use QYoloImageDetection

- Select `.cfg` , `.names` and `.weights` file using the 3 `Select` buttons on the top-left of the application window.
- Enter Threshold Value and Click `Save Threshold` button.
- Make other proper configurations as you wish. 
- Select Source Image using `Select` button of the `Original Image` part， the original image will pop up in a OpenCV `highgui` window. 
- Simply Click `Go` , the application will read darknet with OpenCV dnn module and the result image will pop up.
- Click `Segment_Save` or `Save Cap` button as you wish. Remember to **Select Result Saving Path** beforehand. 
- Tick "Open Socket" Check box and configure the Address and Port then click "Socket!" if you want to send target object coordinates using Socket Communication.

<br>

<div align="center"><img src="https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/raw/main/CPP-Qt/QYoloImageDetection/README.assets/ImageDetection.png" alt="Object Detection using QYoloImageDetection" width="600px"></div>

<br>

**Use Socket to send target object coordinates**

<div align="center"><img src="https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/raw/main/CPP-Qt/QYoloImageDetection/README.assets/socketSendCoordinates.png" alt="socketSendCoordinates" width="700px" /></div>

<br>

Socket Message Decode:

[index, (Point1.x, Point1.y), (Point2.x, Point2.y), (Point3.x, Point3.y), (Point4.x, Point4.y), (Point5.x, Point5.y)]

**Segment Result**

<div align="center"><img src="https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/raw/main/CPP-Qt/QYoloImageDetection/README.assets/segmentResult.png" alt="segmentResult" width="700px" /></div>

<br>

## How to modify from the source code

- This application is based on **OpenCV 4.5.5 x64 CPU version** and **Qt 5.15.0 x64**. Due to the import of the `winsock.h` lib, this code probably **only** suitable for the Windows PC. You need to find another way to achieve Socket Communication if you are a macOS or Linux user.
- You need to deploy both **OpenCV 4.x.x** and **Qt 5.15.x** to ensure the source code can be successfully complied on your PC.

<br>

