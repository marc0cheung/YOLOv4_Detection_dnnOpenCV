# -*- coding: utf-8 -*-
# yolov4-tiny Object Detection (RealTime)
import cv2
import time

imgNum = 0

camera = cv2.VideoCapture(0)  # active local USB Camera

# (1) import yolov4-tiny net config
# import .cfg file and .weight file
# net = cv2.dnn.readNet('dnn_model\yolov4-tiny.cfg', 'dnn_model\yolov4-tiny.weights')  # For Yolov4-Tiny
# net = cv2.dnn.readNet('dnn_model\yolov4.cfg', 'dnn_model\yolov4.weights')            # For Standard Yolov4
# net = cv2.dnn.readNet('yolo-fastest\yolo-fastest-1.1-xl.cfg', 'yolo-fastest\yolo-fastest-1.1-xl.weights')  # For Yolo-Fastest
# net = cv2.dnn.readNet('yolo-fastest\\remote.cfg', 'yolo-fastest\\weights\\remote_6000.weights')            # for Self-trained YOLO Fastest
net = cv2.dnn.readNet('yolo-tiny-random\\remote_tiny.cfg',
                      'yolo-tiny-random\\weights\\remote_tiny_final.weights')  # for Self-trained YOLO Tiny

# define a object detection model and pass the net config
model = cv2.dnn_DetectionModel(net)

'''
Set Model Input
size: Scale the input image to the specified size. 
      the larger the size, the better the detection effect, 
      but the slower the detection speed.
scale: The scaling size of the pixel values. 
       In opencv each pixel value ranges from 0-255, 
       while in neural networks each pixel value ranges from 0-1
'''
model.setInputParams(size=(416, 416), scale=1 / 255)

# (2) Obtain information of classified text
classes = []  # Store the name of each category
with open('yolo-tiny\\remote_tiny.names') as file_obj:
    # Get each line in the text
    for class_name in file_obj.readlines():
        # Remove line breaks, spaces, etc. from text
        class_name = class_name.strip()
        # Save each category name to the list
        classes.append(class_name)

# (3) Video Capture
# filepath = 'C:\\remote.mp4'
cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)

# (5) Create Window
cv2.namedWindow('Image')

# (6) define the detection box drawing function
colorline = (0, 255, 0)  # Angle point line segment color
angerline = 13  # Length of angle point line segment


def drawbbx(img, x, y, w, h, predName, score):
    # draw rectangle object detection box
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 1)
    # beautify the angle point
    cv2.line(img, (x, y), (x + angerline, y), colorline, 2)
    cv2.line(img, (x, y), (x, y + angerline), colorline, 2)
    cv2.line(img, (x + w, y), (x + w, y + angerline), colorline, 2)
    cv2.line(img, (x + w, y), (x + w - angerline, y), colorline, 2)
    cv2.line(img, (x, y + h), (x, y + h - angerline), colorline, 2)
    cv2.line(img, (x, y + h), (x + angerline, y + h), colorline, 2)
    cv2.line(img, (x + w, y + h), (x + w, y + h - angerline), colorline, 2)
    cv2.line(img, (x + w, y + h), (x + w - angerline, y + h), colorline, 2)

    # show object category name
    cv2.putText(img, predName, (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # show prediction percentage
    cv2.putText(img, str(int(score * 100)) + '%', (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)


# (6) Process every frame of the video stream
while True:

    # return [if success flag] and each frame
    ret, frame = cap.read()

    # resize the image
    frame = cv2.resize(frame, (1280, 720))
    # frame = cv2.resize(frame, (416, 416))

    # if the video is short, loop it
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # If the current frame == total frames, then reset the current frame to 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    T1 = time.perf_counter()  # Start detection time node (used to calculate how long a detection will take)
    # Object Detection
    '''
    Return values:
    classids: Detection of the obtained category
    score: Probability of detection of the obtained target
    bbox: 85 items of information in the test box
    argvs: 
    confThreshold: Minimum confidence level for target detection
    nmsThreshold: Custom parameters for non-extreme value suppression
    '''
    classids, scores, bboxes = model.detect(frame, 0.8, 0.3)

    # (7) Show detection result
    # Iterate through all the detection box information and draw them out
    for class_id, score, bbox in zip(classids, scores, bboxes):
        # Get the coordinates and width of the upper left corner of the detection box
        x, y, w, h = bbox

        # Get the name of the category corresponding to the detection box
        class_name = classes[class_id]

        drawbbx(frame, x, y, w, h, class_name, score)
        print(str(len(bboxes)) + " Object(s) Detected")
        cv2.imshow('Object', frame[y:y+h, x:x+w])

    T2 = time.perf_counter()  # Detection Complete time point

    # Put fps and d on the video stream and 
    cv2.putText(frame, str("RT: ") + str(int((T2 - T1) * 1000)) + str('ms'), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1,
                (0, 0, 255), 2)
    cv2.putText(frame, str("FPS: ") + str(fps), (10, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, str("YOLO FPS: ") + str(int(1000 / ((T2 - T1) * 1000))), (10, 150), cv2.FONT_HERSHEY_COMPLEX, 1,
                (0, 0, 255), 2)
    cv2.imshow('Image', frame)        # Display each frame
    if cv2.waitKey(30) & 0xFF == 27:  # Each frame lingers for 1 ms and then disappears
        break

# release capture
cap.release()
cv2.destroyAllWindows()
