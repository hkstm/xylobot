import numpy as np
import cv2
from computervision import Grid
from computervision.CenterPoint import CenterPoint


cap = cv2.VideoCapture(1)
DONE = False
finalObj = None
bready = False
b2ready = False
finalObj2 = None
Swapped = False
list = []
boundarycenterleft = None
boundarycenterright = None

def run():
    width = int(cap.get(3))
    height = int(cap.get(4))
    global finalObj, DONE, bready, b2ready, finalObj2, list, Swapped, boundarycenterleft, boundarycenterright
    Swapped = False
    #bready = False
    #b2ready = False
    while(DONE == False):
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow('hsv', hsv)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([60, 80, 50])
        mask = cv2.inRange(hsv, lower_black, upper_black)
        cv2.imshow('original', mask)
        kernel = np.ones((2, 2), np.uint8)
        erode = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.dilate(erode, kernel, iterations=1)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_CLOSE, kernel)
        mask = dilatemask
        cv2.imshow('blackmask', mask)
        blackcnts = cv2.findContours(mask.copy(),
                                     cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(blackcnts) > 0:
            black_area = max(blackcnts, key=cv2.contourArea)
            Obj = cv2.fitEllipse(black_area)
            center = Obj[0]
            size = Obj[1]
            if (size[0] > 16 and size[0] < 25 and size[1] > 100 and size[1] < 130):
                finalObj = Obj
                bready = True
            elif (size[0] > 16 and size[0] < 25 and size[1] > 150 and size[1] < 200):
                finalObj2 = Obj
                b2ready = True

#SECOND HALF!!!!!!!!!!!!!!!!!!!!!!!!!!

#Crop image
        if bready:
            offset = int(finalObj[1][0]) + 370
        elif b2ready:
            offset = int(finalObj2[1][0]) + 370
        else:
            offset = 420
        crop = frame[0:height, offset:640]
        cv2.imshow('crop', crop)
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
            elif (size[0] > 16 and size[0] < 25 and size[1] > 150 and size[1] < 200):
                finalObj2 = Obj2
                b2ready = True
        
        if bready:
            cv2.ellipse(frame, finalObj, (0, 255, 255), 2)
            cv2.circle(frame, (int(finalObj[0][0]), int(finalObj[0][1])), 1, (0, 0, 255), 3)
            boundarycenterleft = (int(finalObj[0][0]), int(finalObj[0][1]))
        if b2ready:
            cv2.ellipse(frame, finalObj2, (255, 0, 0), 2)
            cv2.circle(frame, (int(finalObj2[0][0]), int(finalObj2[0][1])), 1, (0, 0, 255), 3)
            boundarycenterright = (int(finalObj2[0][0]), int(finalObj2[0][1]))
        if b2ready and bready and (abs(int(finalObj2[0][0]) - int(finalObj[0][0])) > 100 or abs(int(finalObj2[0][1]) - int(finalObj[0][1])) > 100):
            Swapped = False
            if ((int(finalObj2[0][0]) - int(finalObj[0][0])) < 0):#CHECK WITH RHYS
                boundarycenterleft = (int(finalObj2[0][0]), int(finalObj2[0][1]))
                boundarycenterright = (int(finalObj[0][0]), int(finalObj[0][1]))
                print((int(finalObj2[0][0]) - int(finalObj[0][0])))
                temp = finalObj
                finalObj = finalObj2
                finalObj2 = temp
                Swapped = True
            lineThickness = 2
            cv2.line(frame, (int(finalObj[0][0]), int(finalObj[0][1])), (int(finalObj2[0][0]), int(finalObj2[0][1])), (0, 255, 0), lineThickness)
            cv2.circle(frame, (int(finalObj[0][0] + (1 / 9) * (finalObj2[0][0] - finalObj[0][0])), int((finalObj[0][1] + (1 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1,(0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (2 / 9)*(finalObj2[0][0]-finalObj[0][0])), int((finalObj[0][1] + (2/9)*(finalObj2[0][1]-finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (3 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (3 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (4 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (4 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (5 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (5 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (6 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (6 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (7 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (7 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (8 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (8 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            #print(" List Found")
            if Swapped: #CHECK WITH RHYS
                createList2(int(finalObj[0][0]), int(finalObj[1][0]), int(finalObj[0][1]), int(finalObj[1][1]))
            else:
                createList1(int(finalObj[0][0]), int(finalObj[1][0]), int(finalObj[0][1]), int(finalObj[1][1]))


            cv2.imwrite('Xylobot\centerpoints.jpg', frame)
            #print('Printed')
            #DONE = True

        cv2.imshow('frame', frame)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


def getList():
    return list

def createList1(blackcx, black2cx, blackcy, black2cy):
    print(" LIST CERATED 1")
    list.append(CenterPoint("c6", int(blackcx + (8 / 9) * (black2cx - blackcx)),
                            int(blackcy + (8 / 9) * (black2cy - blackcy)), 0, 0, 0))
    list.append(
        CenterPoint("d6", int(blackcx + (7 / 9) * (black2cx - blackcx)), int(blackcy + (7 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("e6", int(blackcx + (6 / 9) * (black2cx - blackcx)), int(blackcy + (6 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("f6", int(blackcx + (5 / 9) * (black2cx - blackcx)), int(blackcy + (5 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("g6", int(blackcx + (4 / 9) * (black2cx - blackcx)), int(blackcy + (4 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("a6", int(blackcx + (3 / 9) * (black2cx - blackcx)), int(blackcy + (3 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("b7", int(blackcx + (2 / 9) * (black2cx - blackcx)), int(blackcy + (2 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("c7", int(blackcx + (1 / 9) * (black2cx - blackcx)), int(blackcy + (1 / 9) * (black2cy - blackcy)),
                    0, 0, 0))

def createList2(blackcx, black2cx, blackcy, black2cy):
    print(" LIST CERATED 2")
    list.append(CenterPoint("c7", int(blackcx + (8 / 9) * (black2cx - blackcx)),
                            int(blackcy + (8 / 9) * (black2cy - blackcy)), 0, 0, 0))
    list.append(
        CenterPoint("b6", int(blackcx + (7 / 9) * (black2cx - blackcx)), int(blackcy + (7 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("ba6", int(blackcx + (6 / 9) * (black2cx - blackcx)), int(blackcy + (6 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("g6", int(blackcx + (5 / 9) * (black2cx - blackcx)), int(blackcy + (5 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("e6", int(blackcx + (4 / 9) * (black2cx - blackcx)), int(blackcy + (4 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("f6", int(blackcx + (3 / 9) * (black2cx - blackcx)), int(blackcy + (3 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("d7", int(blackcx + (2 / 9) * (black2cx - blackcx)), int(blackcy + (2 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("c6", int(blackcx + (1 / 9) * (black2cx - blackcx)), int(blackcy + (1 / 9) * (black2cy - blackcy)),
                    0, 0, 0))

def getBoundaryMidpoints():
    global boundarycenterleft, boundarycenterright
    return boundarycenterleft, boundarycenterright

def destroyWindows():
    try:
        cap.release()
        cv2.destroyAllWindows()
    except:
        print("No getSides() windows to destroy")

if __name__ == '__main__':
    run()
