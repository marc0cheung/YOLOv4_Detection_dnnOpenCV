# YOLOv4-Tiny Real-Time Detection (C++ Implementation)

**Select Language**: English | [Simplified Chinese](https://github.com/marc0cheung/YOLOv4_Detection_dnnOpenCV/blob/main/CPP-Qt/README_SimplifiedCN.md)

<br>

<br>

## Introduction

The `dnn` module in OpenCV is used to read neural networks under each deep learning technique and provides an implementation of target detection. In the description on the darknet GitHub page, OpenCV is "the fastest YOLOv4 implementation". In order to implement target detection on CPUs, OpenCV was chosen as the basis and the corresponding implementations were written using C++ and Python respectively. The C++ version of the implementation also provides a GPU version code to use Nvidia CUDA as the `dnn` target backend. 

The versions of CUDA and cuDNN used on the IPC are:

CUDA: `cuda_10.1.243_426.00_win10.exe`

cuDNN: `cudnn-10.1-windows10-x64-v8.0.5.39.zip`

**This version of the code, based on Qt 5.15.0, OpenCV 4.5.5, provides a convenient, easy-to-use GUI that is close to the Python version (and even has more features in that version, which was a surprise to me) than the C++-only version.**

<br>

<br>

## On whether you need to configure your environment from scratch

- If you want to use the CPU for computing, you don't need to configure any environment, just run this programme out of the box.
- If you wish to use the GPU for acceleration of the OpenCV dnn module.
  - If you are using my pre-compiled program, you do not need to configure any environment other than the **exact same** NVIDIA CUDA + cuDNN environment that I mentioned above. But even so, I can't guarantee that this program will run properly in the same CUDA and cuDNN environment. If necessary, please configure the Nvidia and OpenCV environments from scratch and recompile the program to ensure that it runs on the GPU. Otherwise, the program will automatically switch to CPU mode.
  - If you are not using my pre-compiled program, then you will need to configure the Nvidia and OpenCV environment from scratch and recompile the program to ensure that it runs on the GPU.

<br>

<br>

## Quick guide to configuring CUDA Environment

Use my compiled `OpenCV with CUDA` dynamic runtime library for a quick configuration.
Note: This configuration method only works if you are using the same CUDA and cuDNN version as me.

<br>

- Download my compiled `x64_dnn.zip` zip file
- Extract it to your `opencv\build\` path
- Add `D:\opencv\build\x64_dnn\vc16\bin` to your system environment variables as described in __Step 4__ of **[Configuring the Environment from Scratch (GPU) ]**
- Refer to __Step 4__ of **[Configuring the Environment from Scratch (GPU) ]** to configure the VS2019 development environment.

<br>

<br>

## Configuring the Environment from Scratch (GPU)

### Step 1: Install CUDA

 - Make sure you have a CUDA-enabled Nvidia graphics card installed on your computer
 - Right click on the desktop, select `NVIDIA Control Panel`, and look for `NVCUDA.DLL` in the menu bar under `Help` > `System Information` > `Components` to see which CUDA version is supported.
 - Download the CUDA Toolkit from [Archive of Previous CUDA Releases](https://developer.nvidia.com/cuda-toolkit-archive). Be careful **NOT** to download a version higher than the `NVCUDA.DLL` shown in the system information.
 - Download the `local` version of the installation package, double click on it after downloading and follow the on-screen instructions to install it, usually we choose  `lite` mode to install.
 - After installation, check for `C:\Program Files/NVIDIA GPU Computing Toolkit\CUDA\v10.1\bin` and `CUDA_PATH` and `CUDA_PATH_V10_1` environment variables in the system `Path` environment variable configuration. Generally, CUDA installed in `lite` mode will automatically add the corresponding system environment variables, no additional configuration is required.
 - Add the `C:\Program Files\NVIDIA Corporation\NVSMI` folder to the system `Path` environment variables.
 - Run `cmd` and check by entering the commands `nvcc -V` and `nvidia-smi`. If both respond, the installation was successful.

<br>

<br>

### Step 2: Install cuDNN

- Make sure CUDA is properly installed on the computer.
 - Go to [cuDNN Archive](https://developer.nvidia.com/rdp/cudnn-archive) and download the corresponding cuDNN library according to your CUDA version.
 - Unzip the cuDNN archive, you can see the `bin` , `include` , `lib` directories.
 - Find the CUDA installation directory you installed, open the `V1x.x` directory, find the `bin`, `include`, `lib` directories, and copy the corresponding **files** in the cuDNN compressed package to the corresponding `bin`, `include`, ` lib` CUDA directory.
   <br>
   **Note: It is to copy files to bin, include, lib directories, not to copy directories. **
   <br><br>
 - In system `Path` variables, add the following two paths: 
   `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2 `
   `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\lib\x64`
   At this point, cuDNN has been successfully installed.
- How to check if cuDNN is successfully installed: 
  Open `Windows Powershell` under the path `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\extras\demo_suite`, execute the command: `.\bandwidthTest .exe` . If a response corresponding to CUDA Bandwidth Test appears, the configuration is successful.

<br>

<br>

### Step 3: Compile OpenCV with CUDA

 - Reminder: The version of OpenCV available on the official website is the `64-bit CPU version`. If you need either the `32-bit CPU version` or the `64-bit GPU version`, you will need to compile it yourself. Note that when compiling the `32-bit GPU version` with cMake and VS2019, there is an error that says it cannot be compiled for unknown reasons. The reason for this is unknown. I guess it is because CUDA no longer supports 32-bit applications. Plenty of `.dll` files are missing in the Win32 folder of CUDA directory.
 - Go to [cMake Download](https://cmake.org/download/) to download the latest version of cMake.
 - Go to [OpenCV Releases](https://opencv.org/releases/) to download the OpenCV 4.5.5 source package (Source). Alternatively, download the Windows version as an `.exe` file, which will also have the source code stored in the `source` folder after the program has been extracted.
 - Go to [OpenCV Contrib Release Tags](https://github.com/opencv/opencv_contrib/tags) to download the corresponding version of the OpenCV Contrib library source code. Because of newer features such as CUDA acceleration, OpenCV has placed them in the opencv_contrib library. Unzip the downloaded files and place them in the OpenCV sources folder.
 - Create a new `x64_cuda_build` folder under the OpenCV build folder, open cMake, select the corresponding location for source and build, click the Configure button, select VS2019 and x64, and confirm.
 - In cMake GUI, adjust these options as follows: 

```bash
ENABLE: WITH_CUDA
ENABLE: OPENCV_DNN_CUDA
ENABLE: OPENCV_ENABLE_NONFREE
ENABLE: CUDA_FAST_MATH
ENABLE: BUILD_opencv_world

DISABLED: ENABLE_FAST_MATH
DISABLED: BUILD_CUDA_STUBS
DISABLED: All options after searching "python"
DISABLED: All options after searching "java"
DISABLED: All options after searching "test"

OPENCV_EXTRA_MODULES_PATH: choose modules folder under opencv_contrib directory
CUDA_ARCH_BIN: choose arithmetic version of the graphics card. (e.g. for Pascal GPUs this version number should be `6.1; ` )

```

- Once you've configured it as described above, click the configure button again. If some of the above options don't appear at first, click the configure button for the first time and then search for them.
- **For users in China**, cMake will automatically download some content from GitHub during the build process, but this may not be possible due to the GFW issues in China. If cMake prompts you to check cMakeDownloadLog.txt during the build process, you should follow [this article](https://blog.csdn.net/painice/article/details/123347824) to resolve the problem.
- When cMake does not show any errors in red fonts, check the cMake output for the corresponding version number at CUDA, the cuDNN for `CUDNN: YES (Ver X.X.X)`, and CUDA_ARCH_BIN for the graphics card's arithmetic version. (e.g. for Pascal GPUs this version number should be `6.1; ` )
- When everything is OK with cMake, you can press the `Open Project` button, open the project with VS2019 and select `Generate` > `Batch Generate` > tick the Debug and Release versions of INSTALL and select Generate.
- After a long wait, we will see the `install` folder under the `x64_cuda_build` folder, containing the `x64` folder, which is the `.dll` file we need to use.

<br>

<br>

### Step 4: Configure OpenCV with CUDA in VS 2019

- In the system `Path` environment variables, add `D:\opencv\x64_cuda_build\install\x64\vc16\bin`.
- After opening the VS project, `Debug` > `Properties` select the corresponding platform and bit number you need to configure, e.g. `Release X64`. If the platform changes later on, the environment will need to be reconfigured.
- In `C++` > `General` > `Additional include directories`, add the `D:\opencv\build\include` and `D:\opencv\build\include\opencv2` directories.
- In `Linker` > `General` > `Additional libraries directory`, add `D:\opencv\x64_cuda_build\install\x64\vc16\lib`, and in `Linker` > `Input` > `Additional dependencies`, add `opencv_world455.lib` (for `release` , the number in the file name is the (the number in the file name is the OpenCV version number), or `opencv_world455d.lib` if it is a `debug` platform.
- Run the project and make sure that the model run used in `main.cpp` sets the target device and compute backend to CUDA. The following code is shown.

```c++
yolo_net.setPreferableBackend(cv::dnn::DNN_BACKEND_CUDA);
yolo_net.setPreferableTarget(cv::dnn::DNN_TARGET_CUDA);
```

- As this project is also configured for JSON writing, you will also need to configure [jsoncpp](https://github.com/open-source-parsers/jsoncpp) to run. The configuration is as follows.
  - Download the source package from [jsoncpp](https://github.com/open-source-parsers/jsoncpp), unzip it and copy the `include` folder to the project directory.
  - Copy the `src` folder from the jsoncpp source code folder to the project directory.
  - Open this project in VS2019 and in the project properties, under `C++` > `General` > `Additional Inclusion Directories`, add the `D:\{Project_Folder}\include` directory.
  - In the Sources section of the project's Solution Explorer, use `Right-click` > `Add` > `Existing Items` to add the three `.cpp` files from `{Project_Folder}\src\lib_json\` (three in total, `json_reader.cpp`, `json_value. cpp` and `json_writer.cpp`) to the source file.

- Try to run the project, if it is allowed successfully then the configuration is successful.
- Open `Windows Task Manager` and check the CPU and GPU usage while the project is running. In general, on an IPC with an `i7-4790` CPU and `GT 1030` GPU, the CPU usage is basically below 10%.

<br><br>

## How To Switch to CPU Computing Mode

- Run the program and set the "Use GPU + CUDA" checkbox in the bottom right corner to "Not-Selected" status.

<br>

<br>

## Features

- An easy-to-use GUI is provided to allow users to adjust the various settings of the program.
- Reads the neural network profiles of the YOLO family of networks and indeed all OpenCV DNN modules that support intervention and invokes the neural network for target detection or segmentation.
- Support for socket protocol communication to pass coordinate information between different platforms and applications.
- Support for target coordinates output in `.json` format
- Coordinate information contains the coordinates of the four points of the rectangular box, as well as the coordinates of the centre point.

<br>

<br>

## Current Issues (June 5, 2022)

1. This program was developed and compiled on a computer without an `OpenCV with CUDA` environment. If ported directly to a computer with an `OpenCV with CUDA` environment for application, OpenCV may not be able to call the CUDA environment for detection acceleration.
2. During the writing of the `.json` file, it seems that the object coordinates are not written in the order according to the  `loopCount` values defined in the code, and the JSON file always ends up with the object coordinates corresponding to `Detected_at_99`. However, the JSON file does grow in size as the detection time continues.
3. The `.json` file can become very large if the program is running for a long time because the program is constantly writing coordinates to the `.json` file. It is therefore recommended to turn **OFF** the __[Write JSON]__ function if this is not needed very much.

<br>
