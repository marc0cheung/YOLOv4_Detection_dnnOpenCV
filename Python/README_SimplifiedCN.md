# 基于 YOLOv4-Tiny 的遥控器实时检测软件（Python 实现）

选择语言：[英文](https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/blob/main/Python/README.md) | 简体中文

## 简介

YOLO 系列深度学习网络深受各界的欢迎。 [AlexeyAB](https://github.com/AlexeyAB/darknet/) 利用 Darknet 实现了 YOLOv4 这一速度与识别率有着较好平衡的目标检测网络。OpenCV 支持 DNN 模块后，可以方便的读取神经网络的权重、架构等文件，进而可以摆脱 Darknet 较慢的检测速率。

本软件是一个基于 OpenCV-Python 、PySide2 的 YOLOv4-Tiny 网络实时检测实现。所使用的训练权重是针对遥控器的实时检测模型，使用 Google Colab 训练得到。

<br>

## 软件界面及按键介绍

### 软件主页面

<img src="https://github.com/marc0cheung/YOLOv4_RemoteDetection_OpenCVDNN/raw/main/Python/README_SimplifiedCN.assets/image-20220523165423786.png" alt="image-20220523165423786" style="zoom: 50%;" />

<br>

- `Save Pref.` 按钮：该按钮用于用户对视频流的像素（暂不支持）以及所截取的识别结果图像的序号进行自定义后，其偏好设置的保存。
- `Segment` 按钮：视频流实时检测中，可以对当前画面中的目标物进行目标分割，路径即为程序下方 `Select Segment Saving Path....` 部分所选择的路径。
- `Cap!` 按钮：视频流实时检测中，可以对当前的整个画面进行截取，如果此时画面中包含目标物，程序会保留识别框，但不会保留左上角的 FPS 等信息。
- `From File` 按钮：该按钮按下后打开图片检测功能页。
- `Close` 按钮：关闭本程序。
- `About` 按钮：关于本程序的介绍。
- 程序启动时会弹出一个对话框，其中有三个路径选择按钮，分别选择 YOLO 网络的 `.names` 文件、 `.cfg` 文件以及 `.weights` 文件。
- 程序下方有两个路径选择按钮，分别选择目标分割的保存路径以及截取整体画面的保存路径。

<br>

### 图片检测功能页

<img src="https://github.com/marc0cheung/YOLOv4_RemoteDetection_OpenCVDNN/blob/main/Python/README_SimplifiedCN.assets/image-20220523165747321.png?raw=true" alt="image-20220523165747321" style="zoom: 50%;" />

<br>

### 目标分割提取效果

<img src="https://github.com/marc0cheung/YOLOv4_RemoteDetection_OpenCVDNN/blob/main/Python/README_SimplifiedCN.assets/image-20220523165857078.png?raw=true" style="zoom: 50%;" />

<br>

## 软件功能

通过该软件，你可以：

- 基于 YOLOv4-Tiny 网络实时检测视频流中的遥控器（或者类似遥控器的）物体。
- 自行更换自训练的权重和网络（唯需要 OpenCV DNN 模块支持），实现任意物体的检测。
- 支持选择图片，输入神经网络进行检测。
- 图片检测与视频流检测中，均支持目标分割、识别结果的自定义路径保存。
- 实时输出画面中目标的个数。

<br>

<br>

## 注意事项

- 本程序只支持英文路径，请在英文路径下保存本程序或者任何本程序所输出的内容。
- 自定义分辨率功能暂不可用，待下一版更新。

<br>

<br>
