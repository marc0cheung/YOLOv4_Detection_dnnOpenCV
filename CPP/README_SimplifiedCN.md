# 基于 YOLOv4-Tiny 的实时检测软件（C++ 实现）
**Select Language**:  [English](https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/blob/main/CPP/README.md) | Simplified Chinese

<br>

<br>

## 简介

OpenCV 中的 dnn 模块用于读取各深度学习技术下的神经网络，并提供了目标检测的实现。在 darknet 主页的介绍中，OpenCV 是 “速度最快的 YOLOv4 目标检测实现”。为了实现 CPU 上的目标检测，选用了 OpenCV 作为基础，利用 C++ 和 Python 分别写了对应的实现。同时，在 C++ 版本的实现中，还提供了 CPU 运算版本与 GPU 运算版本的切换。<br>
测试中所采用的工控机 CUDA 与 cuDNN 的版本为：<br>
CUDA: `cuda_10.1.243_426.00_win10.exe`

cuDNN: `cudnn-10.1-windows10-x64-v8.0.5.39.zip`
<br><br>

## 快速配置环境指南（GPU）
利用本人编译好的 `OpenCV with CUDA` 动态运行库，进行快速配置。
注意：该配置方法仅适用于与本人使用同一 CUDA 和 cuDNN 版本的情况。
<br>

- 下载本人编译好的 `x64_dnn.zip` 压缩包
- 解压到你的 `opencv\build\` 下。
- 参考 【从零开始配置环境（GPU）】的 Step 4，在系统环境变量中添加 `D:\opencv\build\x64_dnn\vc16\bin` 
- 在 VS2019 中参考 【从零开始配置环境（GPU）】的 Step 4，配置 VS2019 开发环境。
<br><br>
## 从零开始配置环境（GPU）
### Step 1: 安装 CUDA
 - 确定本机安装了一张支持 CUDA 的 nVIDIA 显卡
 - 桌面上单击右键，选择 `NVIDIA控制面板` ，在菜单栏的 `帮助` > `系统信息` > `组件` 中找到 `NVCUDA.DLL`，即可看到支持的CUDA版本。
 - 前往 CUDA 官网 下载 CUDA Toolkit，可以在 [Archive of Previous CUDA Releases](https://developer.nvidia.com/cuda-toolkit-archive) 找到自己对应的版本。注意下载的版本不要超过 系统信息 中所显示的 `NVCUDA.DLL` 对应的版本。
 - 下载 `local` 版本的安装包，下载完毕后双击启动，按照屏幕上的提示进行安装，一般选择 `精简` 模式进行安装即可。
 - 安装完毕后，在系统环境变量配置中检查，是否有 `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\bin` 以及 `CUDA_PATH` 、 `CUDA_PATH_V10_1` 环境变量。一般而言，通过精简模式安装的 CUDA 均会自动添加对应的系统环境变量，无需额外配置。
 - 将 `C:\Program Files\NVIDIA Corporation\NVSMI` 文件夹添加到系统环境变量中。
 - 打开 `cmd` ，输入指令 `nvcc -V` 以及 `nvidia-smi` 进行检查。如果均有回应，则说明安装成功。
<br><br>
### Step 2: 安装 cuDNN
 - 确定 CUDA 正确的安装在电脑上。
 - 前往 [cuDNN Archive](https://developer.nvidia.com/rdp/cudnn-archive) ，按照 CUDA 版本号，下载对应的 cuDNN 库。
 - 解压 cuDNN 压缩包，可以看到 `bin` 、 `include` 、 `lib` 目录。
 - 找到你安装的版本目录，打开，找到 `bin` 、 `include` 、 `lib` 目录，将 cuDNN 压缩包内对应的 **文件** 复制到 CUDA 对应的 `bin` 、 `include` 、 `lib` 目录。
<br>
**注意：是复制文件到bin、include、lib目录，不是复制目录。**
<br><br>
 - 在系统变量中，添加下方两个路径：<br>
`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2`<br>`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\lib\x64`<br>
到此， cuDNN 安装成功。
- 检测 cuDNN 是否安装成功的方法：<br>在路径 `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\extras\demo_suite` 下打开 `Windows Powershell` ，执行命令：`.\bandwidthTest.exe` 。如果出现 CUDA Bandwidth Test 对应的响应，则说明配置成功。
<br><br>
### Step 3: 编译 OpenCV with CUDA
 - 提醒：OpenCV在官网上下载到的版本是 `64位CPU版` 。如果需要 `32位CPU版` 或 `64位GPU版` 则均需要自行编译。注意，用 cMake 与 VS2019 编译 `32位GPU版` 时，会出现报错无法编译的情况，原因未知。猜测可能是 CUDA 不再支持 32位 的应用程序了。
 - 前往 [cMake Download](https://cmake.org/download/) 下载 cMake 最新版本。
 - 前往 [OpenCV Releases](https://opencv.org/releases/) 下载 OpenCV 4.5.5 源码包（Source）。或者直接下载 Windows 版本的 `.exe` 文件，程序自解压后亦会有源码保存在 `source` 文件夹中。
 - 前往 [OpenCV Contrib Release Tags](https://github.com/opencv/opencv_contrib/tags) 下载对应版本的 OpenCV Contrib 库源代码。因为 CUDA 加速等比较新的特性，OpenCV 将其放置在 opencv_contrib 库中。将下载到的文件解压，放置到 OpenCV 的 sources 文件夹下。
 - 在 OpenCV 的 build 文件夹下新建一个 `x64_cuda_build` 文件夹，打开 cMake ，选择 source 和 build 对应的存放位置，点击 Configure 按钮，选择 VS2019 和 x64 ，确认。
 - 在 cMake 界面中，按照下列描述，调整各选项：

```
启用：WITH_CUDA
启用：OPENCV_DNN_CUDA
启用：OPENCV_ENABLE_NONFREE
启用：CUDA_FAST_MATH
启用：BUILD_opencv_world

禁用：ENABLE_FAST_MATH
禁用：BUILD_CUDA_STUBS
禁用：搜索 python 后的所有内容
禁用：搜索 java 后的所有内容
禁用：搜索 test 后的所有内容

OPENCV_EXTRA_MODULES_PATH 选择 opencv_contrib 目录下的 modules 文件夹
CUDA_ARCH_BIN：选择自己显卡的算力版本，例如 Pascal 架构显卡为 6.1; 剩下的全部去掉。

```

- 按照上述内容配置完毕后，再次点击 configure 按钮，如果刚开始上述的某些选项没有出现，请点第一次 configure 按钮后再搜索。
- 对于身处中国的用户，cMake 在编译过程中会自动从 GitHub 上下载一些内容，此时可能由于网络原因无法下载。如果 cMake 在编译过程出现查看 cMakeDownloadLog.txt 的提示，用户应当按照 [这篇文章](https://blog.csdn.net/painice/article/details/123347824) 来解决问题。
- 当 cMake 没有任何红色错误出现后，查看 cMake 输出信息中，是否在 CUDA 处有对应的版本号，cuDNN 处是否显示 `CUDNN: YES (Ver X.X.X)` ，以及 CUDA_ARCH_BIN 处是否显示显卡的算力版本。
- 当 cMake 的一切都没有问题，即可选择 `Open Project` 按钮，用 VS2019 打开项目，选择 `生成` > `批生成` > 勾选 INSTALL 的 Debug 和 Release 版本，选择生成。
- 经过漫长的等待，我们即可在 `x64_cuda_build` 文件夹下看到 `install` 文件夹，内有 `x64` 文件夹，即我们需要用到的 `.dll` 文件。
<br><br>
### Step 4: VS2019 上配置 OpenCV
- 系统环境变量中，添加 `D:\opencv\x64_cuda_build\install\x64\vc16\bin`
- 打开 VS 项目后，`调试` > `属性` 选择所需要配置的对应的平台和位数，例如 `Release X64` 。如果后期发生平台的变更，则需要重新配置环境。
- 在 `C++` > `常规` > `附加包含目录` 中，添加 `D:\opencv\build\include` 以及 `D:\opencv\build\include\opencv2` 目录。
- `链接器` > `常规` > `附加库目录` 中，添加 `D:\opencv\x64_cuda_build\install\x64\vc16\lib` ，同时在 `链接器` > `输入` > `附加依赖项` 中，添加 `opencv_world455.lib` （文件名中的数字为 OpenCV 版本号），如果是 `debug` 平台，则添加 `opencv_world455d.lib` 。
- 运行项目，确定 `main.cpp` 中，所使用的模型运行设置目标设备与计算后台为 CUDA 。如下代码所示：
```c++
yolo_net.setPreferableBackend(cv::dnn::DNN_BACKEND_CUDA);
yolo_net.setPreferableTarget(cv::dnn::DNN_TARGET_CUDA);
```
- 由于本项目还配置有 JSON 写入功能，所以还需要配置 [jsoncpp](https://github.com/open-source-parsers/jsoncpp) 方可运行。配置方法如下：
  - 前往 [jsoncpp](https://github.com/open-source-parsers/jsoncpp) 下载源码包，解压后，将文件夹内的 `include` 文件夹复制到本项目目录下。
  - 将 `jsoncpp-master\src\lib_json` 下的所有 `.cpp` 文件（共三个，分别为 `json_reader.cpp` 、`json_value.cpp` 以及 `json_writer.cpp` ）拷贝到本项目目录下。
  - 用 VS2019 打开本项目，在项目属性中，在 `C++` > `常规` > `附加包含目录` 中，添加 `D:\YOLO-CPP-CUDA-Socket\include` 目录。
  - 在本项目的 解决方案资源管理器 中的 源文件 部分，使用 `右键` > `添加` > `现有项` ，将上述的三个来自 jsoncpp 的 `.cpp` 文件添加到 源文件 中。

- 尝试运行项目，若能成功允许则配置成功。
- 打开 `Windows任务管理器` ，查看项目运行时， CPU 与 GPU 的占用率，一般而言，在 CPU 为 `i7-4790` ， GPU 为 `GT 1030` 的工控电脑上， CPU 占用率基本上维持在 10% 以下。
  <br><br>

## 如何切换到 CPU 模式

- 在 `main.cpp` 中，注释掉第 `81` 、 `82` 行两行包含 `CUDA` 的代码。
- 取消第 `79` 、 `80` 行两行包含 `CPU` 的代码的注释。
- 在 VS2019 项目属性中，将对应的 OpenCV with CPU 版本上。

## 程序功能
- 读取 YOLO 系列网络乃至所有 OpenCV DNN 模块支持介入的神经网络配置文件，并调用神经网络进行目标检测或分割。
- 支持 Socket 协议通信，在不同平台、不同应用程序之间传递坐标信息。
- 支持目标物坐标以 `.json` 格式输出
- 坐标信息包含矩形框的四个点坐标，以及中心点坐标。

<br>

<br>