import numpy as np
import cv2

from computervision import Grid
from computervision.CenterPoint import CenterPoint

cap = cv2.VideoCapture(1)
bready = False
b2ready = False
DONE = False
list = []
boundarycenterleft = None
boundarycenterright = None

def run():
    print(" RUNNING Getssides")
    global DONE, bready, b2ready, list, boundarycenterleft, boundarycenterright
    while(DONE == False):
        ret, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow('hsv', hsv)
        blur = cv2.GaussianBlur(frame, (23, 23), 0)
        edges = cv2.Canny(blur, 100, 200)
        #cv2.imshow('Edges', edges)

        lower_black = np.array([0, 0, 0])
        upper_black = np.array([50, 50, 50])

        mask = cv2.inRange(hsv, lower_black, upper_black)
        kernel = np.ones((2, 2), np.uint8)
        erode = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.dilate(erode, kernel, iterations=1)
        kernel = np.ones((4, 4), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_CLOSE, kernel)


        resb = cv2.bitwise_and(frame, frame, mask=dilatemask)
        #cv2.imshow('black', resb)
        resb2 = cv2.bitwise_and(edges, edges, mask=dilatemask)

        mask = dilatemask
        cv2.imshow('blackmask', mask)

        blackcnts = cv2.findContours(mask.copy(),
                                     cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(blackcnts) > 0:
            black_area = max(blackcnts, key=cv2.contourArea)
            (xg, yg, wg, hg) = cv2.boundingRect(black_area)
            print("hg: ", hg)
            print("wg: ", wg)
            if  125 > hg > 100 and 25 > wg > 10:
                bready = True
                blackx = xg
                blacky = yg
                blackh = hg
                blackw = wg
                blackcx = int(blackx + (blackw / 2))
                blackcy = int(blacky + (blackh / 2))
                print('done')

    #SECOND HALF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if bready:
            offset = blackx + 390
        else:
            offset = 450
        crop = frame[0:380, offset:640]
        cv2.imshow('crop', crop)

        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(crop, (9, 9), 0)
        edges = cv2.Canny(blur, 100, 200)

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
        cv2.imshow('blackmask2', mask)

        blackcnts = cv2.findContours(mask.copy(),
                                     cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(blackcnts) > 0:
            black_area2 = max(blackcnts, key=cv2.contourArea)
            (xg, yg, wg, hg) = cv2.boundingRect(black_area2)
            #cv2.rectangle(frame, (xg+offset, yg), (xg +offset+ wg, yg + hg), (0, 0, 255), 2)
            print(hg)
            print(wg)
            if 125 > hg > 105 and 20 > wg > 10:
                b2ready = True
                black2x = xg + offset
                black2y = yg
                black2h = hg
                black2w = wg
                black2cx = int(black2x + (black2w / 2))
                black2cy = int(black2y + (black2h / 2))
                print('done2')

        #dimensions = frame.shape
        #print(dimensions)


        if bready:
            cv2.rectangle(frame, (blackx, blacky), (blackx + blackw, blacky + blackh), (0, 0, 255), 2)
            #cv2.drawContours(frame, black_area, -1, (0, 255, 255), 1, 8)
            cv2.circle(frame, (blackcx, blackcy), 1, (0, 0, 255), 3)
            boundarycenterleft = (blackcx, blackcy)
        if b2ready:
            cv2.rectangle(frame, (black2x, black2y), (black2x + black2w, black2y + black2h), (0, 0, 255), 2)
            #cv2.drawContours(frame, black_area2, -1, (0, 255, 255), 1, 8)
            cv2.circle(frame, (black2cx, black2cy), 1, (0, 0, 255), 3)
            boundarycenterright = (black2cx, black2cy)
        if b2ready and bready:
            lineThickness = 2
            cv2.line(frame, (blackcx, blackcy), (black2cx, black2cy), (0, 255, 0), lineThickness)
            cv2.circle(frame, (int(blackcx + (1 / 9) * (black2cx - blackcx)), int((blackcy + (1 / 9) * (black2cy - blackcy)))), 1,(0, 0, 255), 3)
            cv2.circle(frame, (int(blackcx + (2 / 9)*(black2cx-blackcx)), int((blackcy + (2/9)*(black2cy-blackcy)))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(blackcx + (3 / 9)*(black2cx-blackcx)), int((blackcy + (3/9)*(black2cy-blackcy)))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(blackcx + (4 / 9)*(black2cx-blackcx)), int((blackcy + (4/9)*(black2cy-blackcy)))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(blackcx + (5 / 9)*(black2cx-blackcx)), int((blackcy + (5/9)*(black2cy-blackcy)))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(blackcx + (6 / 9)*(black2cx-blackcx)), int((blackcy + (6/9)*(black2cy-blackcy)))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(blackcx + (7 / 9)*(black2cx-blackcx)), int((blackcy + (7/9)*(black2cy-blackcy)))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(blackcx + (8.05 / 9)*(black2cx-blackcx)), int((blackcy + (8/9)*(black2cy-blackcy)))), 1, (0, 0, 255), 3)
            print(" List Found")
            createList(blackcx, black2cx, blackcy, black2cy)

            cv2.imwrite('centerpoints.jpg', frame)
            DONE = True




        cv2.imshow('frame', frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break



    cap.release()
    cv2.destroyAllWindows()


def getList():
     return list

def createList(blackcx, black2cx, blackcy, black2cy):
    print(" LIST CERATED")
    list.append(CenterPoint("c6", int(blackcx + (8.05 / 9) * (black2cx - blackcx)),
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

if __name__ == '__main__':
    run()