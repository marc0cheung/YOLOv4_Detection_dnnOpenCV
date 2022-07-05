# QYoloImageDetection

<br>

**选择语言:** [English]() | 简体中文

<br>

<div align="center"><img src="https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/raw/main/CPP-Qt/QYoloImageDetection/README.assets/ImageDetectionMainpage.png" alt="ImageDetectionMainpage" width="700px"></div>

<br>

QYoloImageDetection 是一个支持图像输入的目标检测程序，基于 C++ 与 Qt 5.15.0 开发。该程序通过 OpenCV 的 `dnn` 模块读取 Darknet 网络文件。

<br>

**该程序支持:**

- Darknet 的网络文件，如 `.cfg` 文件、`.names` 文件与 `.weights` 文件。
- 支持置信阈值与 NMS 阈值的调整。
- 自定义检测结果图像中需要显示的内容与参数。
- 目标图像区域分割与保存
- 保存全图像检测结果。
- 利用 Socket 通信发送图像中目标物的坐标

<br>

**未来计划加入的功能:**

- 利用 Socket 通信接收外部程序所发送的 Mat 类型文件进行检测（在后台保持监听）

<br>

## 程序流程图

<div align="center"><img src="https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/raw/main/CPP-Qt/QYoloImageDetection/README.assets/diagram_zhCN.png" alt="diagram_zhCN" width="1200px" /></div>

<br>

## 如何使用 QYoloImageDetection

- 在应用程序窗口左上角使用 3 个 Select 按钮以选择 Darknet 的网络文件，如 `.cfg` , `.names` 和 `.weights` 文件。
- 输入自定义的阈值并按下 `Save Threshold` 按钮。
- 如果你需要使用 Socket 通信发送坐标，请勾选 `Open Socket` 复选框，并输入需要链接的服务器地址、端口号，并按下保存。
- 使用在 `Original Image` 部分的 `Select` 按钮选择原始图片，原始图片会通过 OpenCV 自带的 UI 窗口弹出。
- 单击 `Go` 按钮，程序会用 OpenCV dnn 模块读取方才所选择的 Darknet 网络进行目标检测，检测完毕后，检测结果会自动弹出。如下图所示。
- 单击 `Segment_Save` 或者 `Save Cap` 按钮来保存目标分割结果或整体识别结果，记得一定要提前在程序窗口的右侧选择保存路径*。

*请使用英文路径以避免出错。

<br>

<div align="center"><img src="https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/raw/main/CPP-Qt/QYoloImageDetection/README.assets/ImageDetection.png" alt="Object Detection using QYoloImageDetection" width="600px"></div>

<br>

**使用 Socket 发送目标坐标**

<div align="center"><img src="https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/raw/main/CPP-Qt/QYoloImageDetection/README.assets/socketSendCoordinates.png" alt="socketSendCoordinates" width="700px" /></div>

<br>

坐标信息解读：

[index, (Point1.x, Point1.y), (Point2.x, Point2.y), (Point3.x, Point3.y), (Point4.x, Point4.y), (Point5.x, Point5.y)]

<br>

**目标分割结果展示**

<div align="center"><img src="https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/raw/main/CPP-Qt/QYoloImageDetection/README.assets/segmentResult.png" alt="segmentResult" width="700px" /></div>

<br>

## 如果要基于源代码进行二次开发

- 该软件使用 **OpenCV 4.5.5 x64 CPU 版本** 以及 **Qt 5.15.0 x64** 进行开发。由于 Socket 库的引入，本代码可能仅仅适合于 Windows 系统的计算机。
- 你需要同时在电脑上配置 Visual Studio 2019、 **OpenCV 4.x.x** 与 **Qt 5.15.x** 来保证这份源代码可以正确在你的 PC 上编译。

<br>

