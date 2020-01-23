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
boundarycenterleft = None
boundarycenterright = None
list = []

def run():
    width = int(cap.get(3))
    height = int(cap.get(4))
    global finalObj, DONE, bready, b2ready, finalObj2, list, boundarycenterleft, boundarycenterright
    while(DONE == False):
       # ret, frame = cap.read()

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fgbg = cv2.createBackgroundSubtractorMOG2()
        while (1):
            ret, frame = cap.read()
            fgmask = fgbg.apply(frame)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
            cv2.imshow('frame', fgmask)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow('hsv', hsv)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([50, 50, 50])
        mask = cv2.inRange(hsv, lower_black, upper_black)
        kernel = np.ones((2, 2), np.uint8)
        erode = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.dilate(erode, kernel, iterations=1)
        kernel = np.ones((4, 4), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_CLOSE, kernel)
        mask = dilatemask
        blackimg = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow('blackmask', mask)
        blackcnts = cv2.findContours(mask.copy(),
                                     cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(blackcnts) > 0:
            black_area = max(blackcnts, key=cv2.contourArea)
            Obj = cv2.fitEllipse(black_area)
            center = Obj[0]
            size = Obj[1]
            if (size[0] > 16 and size[0] < 20 and size[1] > 100 and size[1] < 110):
                finalObj = Obj
            if (finalObj != None):
                cv2.ellipse(frame, finalObj, (0, 255, 255), 2)
                bready = True

#SECOND HALF!!!!!!!!!!!!!!!!!!!!!!!!!!

        if bready:
            offset = int(finalObj[1][0]) + 350
        else:
            offset = 400
        crop = frame[0:height, offset:640]
        cv2.imshow('crop', crop)

        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_black, upper_black)
        kernel = np.ones((2, 2), np.uint8)
        erode = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.dilate(erode, kernel, iterations=1)
        kernel = np.ones((4, 4), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_CLOSE, kernel)
        mask = dilatemask
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
            if (size[0] > 16 and size[0] < 25 and size[1] > 150 and size[1] < 175):
                print(size)
                finalObj2 = Obj2
            if (finalObj2 != None):
                cv2.ellipse(frame, finalObj2, (255,0, 0), 2)
                b2ready = True


        
        if bready:
            cv2.circle(frame, (int(finalObj[0][0]), int(finalObj[0][1])), 1, (0, 0, 255), 3)
            boundarycenterleft = (int(finalObj[0][0]), int(finalObj[0][1]))
        if b2ready:
            cv2.circle(frame, (int(finalObj2[0][0]), int(finalObj2[0][1])), 1, (0, 0, 255), 3)
            boundarycenterright = (int(finalObj2[0][0]), int(finalObj2[0][1]))
        if b2ready and bready and (abs(int(finalObj2[0][0]) - int(finalObj[0][0])) > 40 or abs(int(finalObj2[0][1]) - int(finalObj[0][1])) > 40):

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
            print(" List Found")
            createList(int(finalObj[0][0]), int(finalObj[1][0]), int(finalObj[0][1]), int(finalObj[1][1]))

            cv2.imwrite('Xylobot\centerpoints.jpg', frame)
            print('Printed')
            DONE = True

        cv2.imshow('frame', frame)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


def getList():
    global list
    return list

def createList(blackcx, black2cx, blackcy, black2cy):
    global list
    print(" LIST CERATED")
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
