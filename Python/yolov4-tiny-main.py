# -*- coding: utf-8 -*-
# yolov4-tiny Object Detection (RealTime)
import cv2
import time

imgNum = 0

camera = cv2.VideoCapture(0)  # active local USB Camera

# （1）导入yolov4-tiny网络模型结构
# 传入模型结构.cfg文件，模型权重参数.weight文件
# net = cv2.dnn.readNet('dnn_model\yolov4-tiny.cfg', 'dnn_model\yolov4-tiny.weights')  # For Yolov4-Tiny
# net = cv2.dnn.readNet('dnn_model\yolov4.cfg', 'dnn_model\yolov4.weights')          # For Standard Yolov4
# net = cv2.dnn.readNet('yolo-fastest\yolo-fastest-1.1-xl.cfg', 'yolo-fastest\yolo-fastest-1.1-xl.weights')  # For Yolo-Fastest
# net = cv2.dnn.readNet('yolo-fastest\\remote.cfg', 'yolo-fastest\\weights\\remote_6000.weights')  # for DIY YOLO Fastest
net = cv2.dnn.readNet('yolo-tiny-random\\remote_tiny.cfg',
                      'yolo-tiny-random\\weights\\remote_tiny_final.weights')  # for DIY YOLO Tiny

# 定义一个目标检测模型，将模型传进去
model = cv2.dnn_DetectionModel(net)

'''
设置模型的输入
size：将输入的图像缩放至指定大小。size越大检测效果越好，但是检测速度越慢
scale：像素值的缩放大小。在opencv中每个像素值的范围在0-255之间，而在神经网络中每个像素值在0-1之间
'''
model.setInputParams(size=(416, 416), scale=1 / 255)

# （2）获取分类文本的信息
classes = []  # 存放每个分类的名称
with open('yolo-tiny\\remote_tiny.names') as file_obj:
    # 获取文本中的每一行
    for class_name in file_obj.readlines():
        # 删除文本中的换行符、空格等
        class_name = class_name.strip()
        # 将每个分类名保存到列表中
        classes.append(class_name)

# （3）视频捕获
# filepath = 'C:\\remote.mp4'
cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)

# （5）创建窗口
cv2.namedWindow('Image')  # 窗口名和显示图像的窗口名相同

# （6）定义检测框绘制函数
colorline = (0, 255, 0)  # 角点线段颜色
angerline = 13  # 角点线段长度


def drawbbx(img, x, y, w, h, predName, score):
    # 检测框
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 1)
    # 角点美化
    cv2.line(img, (x, y), (x + angerline, y), colorline, 2)
    cv2.line(img, (x, y), (x, y + angerline), colorline, 2)
    cv2.line(img, (x + w, y), (x + w, y + angerline), colorline, 2)
    cv2.line(img, (x + w, y), (x + w - angerline, y), colorline, 2)
    cv2.line(img, (x, y + h), (x, y + h - angerline), colorline, 2)
    cv2.line(img, (x, y + h), (x + angerline, y + h), colorline, 2)
    cv2.line(img, (x + w, y + h), (x + w, y + h - angerline), colorline, 2)
    cv2.line(img, (x + w, y + h), (x + w - angerline, y + h), colorline, 2)

    # 显示预测的类别
    cv2.putText(img, predName, (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # 显示预测概率
    cv2.putText(img, str(int(score * 100)) + '%', (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)


# （6）对每一帧视频图像处理
while True:

    # 返回是否读取成功ret和读取的帧图像frame
    ret, frame = cap.read()

    # 图像比较大把它缩小一点
    frame = cv2.resize(frame, (1280, 720))
    # frame = cv2.resize(frame, (416, 416))

    # 视频比较短，循环播放
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # 如果当前帧==总帧数，那就重置当前帧为0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    T1 = time.perf_counter()  # 开始检测时间节点（用于计算检测一次要多久）
    # 目标检测
    '''
    返回值
    classids：检测得到的类别
    score：检测得到的目标的概率
    bbox：检测框的85项信息
    参数
    confThreshold：目标检测最小置信度
    nmsThreshold：非极大值抑制的自定义参数
    '''
    classids, scores, bboxes = model.detect(frame, 0.8, 0.3)

    # （7）显示检测结果
    # 遍历所有的检测框信息，把它们绘制出来
    for class_id, score, bbox in zip(classids, scores, bboxes):
        # 获取检测框的左上角坐标和宽高
        x, y, w, h = bbox

        # 获取检测框对应的分类名
        class_name = classes[class_id]

        drawbbx(frame, x, y, w, h, class_name, score)
        print(str(len(bboxes)) + " Object(s) Detected")
        cv2.imshow('Object', frame[y:y+h, x:x+w])

    T2 = time.perf_counter()  # 检测完毕时间节点

    # 显示图像
    cv2.putText(frame, str("RT: ") + str(int((T2 - T1) * 1000)) + str('ms'), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1,
                (0, 0, 255), 2)
    cv2.putText(frame, str("FPS: ") + str(fps), (10, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, str("YOLO FPS: ") + str(int(1000 / ((T2 - T1) * 1000))), (10, 150), cv2.FONT_HERSHEY_COMPLEX, 1,
                (0, 0, 255), 2)
    cv2.imshow('Image', frame)  # 窗口名，图像变量
    if cv2.waitKey(30) & 0xFF == 27:  # 每帧滞留1毫秒后消失
        break

# 释放视频资源
cap.release()
cv2.destroyAllWindows()
