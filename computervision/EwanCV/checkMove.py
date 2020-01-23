import numpy as np
import cv2
from computervision import Grid
from computervision.CenterPoint import CenterPoint
from computervision import VideoCamera as vc
import PIL


cap = None
DONE = False
finalObj = None
bready = False
b2ready = False
finalObj2 = None
swapped = False
list = []
boundarycenterleft = None
boundarycenterright = None

def run(gui):
    global finalObj, DONE, bready, b2ready, finalObj2, list, swapped, boundarycenterleft, boundarycenterright, cap
    cap = gui.vid_bird.vid
    width, height = cap.getDimensions()
    swapped = False
    while(DONE == False):
        ret, frame = cap.getNextFrame()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([60, 80, 50])
        mask = cv2.inRange(hsv, lower_black, upper_black)
        kernel = np.ones((2, 2), np.uint8)
        erode = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.dilate(erode, kernel, iterations=1)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_CLOSE, kernel)
        mask = dilatemask
        blackcnts = cv2.findContours(mask.copy(),
                                     cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)[-2]
        try:
            if len(blackcnts) > 0:
                black_area = max(blackcnts, key=cv2.contourArea)
                Obj = cv2.fitEllipse(black_area)
                center = Obj[0]
                size = Obj[1]
                if (size[0] > 16 and size[0] < 25 and size[1] > 100 and size[1] < 130):
                    finalObj = Obj
                    bready = True
                elif (size[0] > 14 and size[0] < 25 and size[1] > 150 and size[1] < 200):
                    finalObj2 = Obj
                    b2ready = True
        except Exception as e:
            continue

#SECOND HALF!!!!!!!!!!!!!!!!!!!!!!!!!!

#Crop image
        if bready:
            print("bready x: ", int(finalObj[0][0]))
            if int(finalObj[0][0]) > int(width/2):
                offsetright = int(width/2)
                offset = 0
            else:
                offset = int(finalObj[0][0]) + 370
                offsetright = 640
        elif b2ready:
            print("b2ready x: ", int(finalObj2[0][0]))
            if int(finalObj2[0][0]) > int(width/2):
                offsetright = int(width/2)
                offset = 0
            else:
                offset = int(finalObj2[0][0]) + 370
                offsetright = 640
        else:
            offset = 420
            offsetright = 640
        crop = frame[0:height, offset:offsetright]
#Change to hsv, find black mask, reduce noise using morphology
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_black, upper_black)
        kernel = np.ones((2, 2), np.uint8)
        erode = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.dilate(erode, kernel, iterations=1)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_CLOSE, kernel)
        mask = dilatemask

#Finding Contours and Ellipses
        blackcnts = cv2.findContours(mask.copy(),
                                     cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)[-2]
        try:
            if len(blackcnts) > 0:
                black_area = max(blackcnts, key=cv2.contourArea)
                Obj2 = cv2.fitEllipse(black_area)
                angle = Obj[2]
                center = Obj2[0]
                size = Obj2[1]
                center = (center[0] + offset, center[1])
                Obj2 = (center, size, angle)
                if (size[0] > 16 and size[0] < 25 and size[1] > 100 and size[1] < 130):
                    finalObj = Obj2
                    bready = True
                elif (size[0] > 14 and size[0] < 25 and size[1] > 150 and size[1] < 200):
                    finalObj2 = Obj2
                    b2ready = True
        except Exception as e:
            continue
        
        if bready:
            boundarycenterleft = (int(finalObj[0][0]), int(finalObj[0][1]))
        if b2ready:
            boundarycenterright = (int(finalObj2[0][0]), int(finalObj2[0][1]))
        if b2ready and bready and (abs(int(finalObj2[0][0]) - int(finalObj[0][0])) > 100 or abs(int(finalObj2[0][1]) - int(finalObj[0][1])) > 100):
            swapped = False
            if ((int(finalObj2[0][0]) - int(finalObj[0][0])) < 0):#CHECK WITH RHYS
                boundarycenterleft = (int(finalObj2[0][0]), int(finalObj2[0][1]))
                boundarycenterright = (int(finalObj[0][0]), int(finalObj[0][1]))
                print((int(finalObj2[0][0]) - int(finalObj[0][0])))
                temp = finalObj
                finalObj = finalObj2
                finalObj2 = temp
                swapped = True
            return boundarycenterleft, boundarycenterright

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    #cap.release()
    cv2.destroyAllWindows()
