# YOLOv4_Detection_dnnOpenCV
YOLOv4-Tiny Remote Control Detection instances using OpenCV DNN module and C++ / PyQt5 (Pyside2) GUI. 

<br>

The YOLO family of deep learning networks has been well received by the community. [AlexeyAB](https://github.com/AlexeyAB/darknet/) uses Darknet to implement YOLOv4, a target detection network with a good balance of speed and recognition rate. The OpenCV support for the DNN module makes it easy to read the neural network weights, `.cfg` files and `.names` files, thus eliminating the slow detection rate of Darknet.

<br>

<br>

## Features

### Python Ver.

- Easy-to-use GUI interface made by PySide2.
- Support single image detection.
- Object Segmentation & Extraction available in both real-time video stream and single image detection.
- Capture & Segment detection results, and can be saved to any path you want (as long as the path is in English).
- FPS and YOLO processing time showed in real-time in the upper left corner in real-time video stream.

<br>

### C++ Ver.

- Based on OpenCV `highgui.h` , and command lines to output.
- Accept any neural network as long as the `dnn` module from OpenCV supported. 
- Support Socket Communication with other applications or machines, use this protocol to send coordinates of objects.
- Support `.json` file output coordinates of objects detected, use [jsoncpp](https://github.com/open-source-parsers/jsoncpp).

<br>

<br>
