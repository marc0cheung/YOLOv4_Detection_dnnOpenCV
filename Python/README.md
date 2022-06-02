# YOLOv4-Tiny Remote Control Detection (Python Implementation)

**Select Language**: English | [Simplified Chinese](https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/blob/main/Python/README_SimplifiedCN.md)



## Introduction

The YOLO family of deep learning networks has been well received by the community. [AlexeyAB](https://github.com/AlexeyAB/darknet/) uses Darknet to implement YOLOv4, a target detection network with a good balance of speed and recognition rate. The OpenCV support for the DNN module makes it easy to read the neural network weights, `.cfg` files and `.names` files, thus eliminating the slow detection rate of Darknet.

This software is a real-time implementation of YOLOv4-Tiny network detection based on OpenCV-Python, PySide2. The training weights used are for a real-time detection model for remote controls, trained using Google Colab.

<br>

<br>

## Implementation UI and Instruction

### Mainpage

<div align=center> 
<img src="https://github.com/marc0cheung/YOLOv4_RemoteDetection_OpenCVDNN/raw/main/Python/README_SimplifiedCN.assets/image-20220523165423786.png" alt="Mainpage" width="300px" />
</div>

<br>

- `Save Pref.`: Used to save the user's preferences for the pixels of the video stream (not supported at the moment) and the index of the intercepted recognition result image filename after customising them.
- `Segment`: In the detection of a real-time video stream, the target object in the current frame can be targeted for segmentation, the path being the one selected in the `Select Segment Saving Path....` section at the bottom of the program.
- `Cap!` button: In the detection of a real-time video stream, you can capture the entire current frame, if the frame contains a target at this time, the program will keep the prediction box(es), but not the FPS information etc. in the upper left corner.
- `From File`: Opens the picture detection window when pressed.
- `Close`: Close the entire program.
- `About`: Open the introduction of the program.
- When the program starts, a dialog box will pop up with three path selection buttons for the `.names` file, the `.cfg` file and the `.weights` file of the YOLO network.
- At the bottom of the program there are two path selection buttons, one for saving the target segment and one for saving the whole screen.

<br>

### Picture Detection Page

<div align=center><img src="https://github.com/marc0cheung/YOLOv4_RemoteDetection_OpenCVDNN/blob/main/Python/README_SimplifiedCN.assets/image-20220523165747321.png?raw=true" alt="Picture_Detection_Page" width="600px" /></div>

<br>

### Object Segmentation & Extraction

<div align=center><img src="https://github.com/marc0cheung/YOLOv4_RemoteDetection_OpenCVDNN/blob/main/Python/README_SimplifiedCN.assets/image-20220523165857078.png?raw=true" alt="Result_Show" width="600px" /></div>

<br>

<br>

## Features

With this software, you can.

- Detect remote control (or remote control-like) objects in the video stream in real time based on the YOLOv4-Tiny network, if you used my trained weights file.
- Change your own self-training weights and network (only requires OpenCV DNN module support) to detect arbitrary objects.
- Support for selecting images to feed into the neural network for detection.
- Support for target segmentation, extraction and custom path saving of recognition results in both image detection and video stream detection.
- Real-time output of the number of targets in the frame.

<br>

<br>

## Cautions

- This program only supports English paths, please save this program or any output from this program in English paths.
- The custom resolution of the real-time video stream is not available at the moment and will be updated in the next version.

<br>

<br>
