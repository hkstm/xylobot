import numpy as np
import cv2

from computervision import Grid
from computervision.CenterPoint import CenterPoint

cap = cv2.VideoCapture(1)
bready = False
b2ready = False
while(True):
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(frame, (9, 9), 0)
    edges = cv2.Canny(blur, 100, 200)
    cv2.imshow('Edges', edges)

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 20])

    mask = cv2.inRange(hsv, lower_black, upper_black)
    cv2.imshow('blackmask', mask)
    kernel = np.ones((7, 7), np.uint8)
    dilatemask = cv2.dilate(mask, kernel, iterations=1)
    resb = cv2.bitwise_and(frame, frame, mask=dilatemask)
    cv2.imshow('black', resb)
    resb2 = cv2.bitwise_and(edges, edges, mask=dilatemask)

    blackcnts = cv2.findContours(mask.copy(),
                                 cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(blackcnts) > 0:
        black_area = max(blackcnts, key=cv2.contourArea)
        (xg, yg, wg, hg) = cv2.boundingRect(black_area)
        #print(hg)
        #print(wg)

    if  145 > hg > 135 and 30 > wg > 20:
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
    upper_black = np.array([180, 255, 35])

    mask = cv2.inRange(hsv, lower_black, upper_black)
    cv2.imshow('blackmask2', mask)
    kernel = np.ones((7, 7), np.uint8)
    dilatemask = cv2.dilate(mask, kernel, iterations=1)
    resb = cv2.bitwise_and(crop, crop, mask=dilatemask)
    cv2.imshow('black2', resb)
    resb2 = cv2.bitwise_and(edges, edges, mask=dilatemask)

    blackcnts = cv2.findContours(mask.copy(),
                                 cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(blackcnts) > 0:
        black_area = max(blackcnts, key=cv2.contourArea)
        (xg, yg, wg, hg) = cv2.boundingRect(black_area)
        #cv2.rectangle(frame, (xg+offset, yg), (xg +offset+ wg, yg + hg), (0, 0, 255), 2)
        print(hg)
        print(wg)

    if 195 > hg > 185 and 35 > wg > 20:
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
        cv2.circle(frame, (blackcx, blackcy), 1, (0, 0, 255), 3)
    if b2ready:
        cv2.rectangle(frame, (black2x, black2y), (black2x + black2w, black2y + black2h), (0, 0, 255), 2)
        cv2.circle(frame, (black2cx, black2cy), 1, (0, 0, 255), 3)
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
        cv2.circle(frame, (int(blackcx + (8.1 / 9)*(black2cx-blackcx)), int((blackcy + (8/9)*(black2cy-blackcy)))), 1, (0, 0, 255), 3)

        list = []
        list.append(CenterPoint("c6",int(blackcx + (1 / 9)*(black2cx-blackcx)),int(blackcy + (1/9)*(black2cy-blackcy)), 0, 0, 0))
        list.append(CenterPoint("d6",int(blackcx + (2 / 9)*(black2cx-blackcx)),int(blackcy + (2/9)*(black2cy-blackcy)), 0, 0, 0))
        list.append(CenterPoint("e6",int(blackcx + (3 / 9)*(black2cx-blackcx)),int(blackcy + (3/9)*(black2cy-blackcy)), 0, 0, 0))
        list.append(CenterPoint("f6",int(blackcx + (4 / 9)*(black2cx-blackcx)),int(blackcy + (4/9)*(black2cy-blackcy)), 0, 0, 0))
        list.append(CenterPoint("g6",int(blackcx + (5 / 9)*(black2cx-blackcx)),int(blackcy + (5/9)*(black2cy-blackcy)), 0, 0, 0))
        list.append(CenterPoint("a6",int(blackcx + (6 / 9)*(black2cx-blackcx)),int(blackcy + (6/9)*(black2cy-blackcy)), 0, 0, 0))
        list.append(CenterPoint("b6",int(blackcx + (7 / 9)*(black2cx-blackcx)),int(blackcy + (7/9)*(black2cy-blackcy)), 0, 0, 0))
        list.append(CenterPoint("c7",int(blackcx + (8.1 / 9)*(black2cx-blackcx)),int(blackcy + (8/9)*(black2cy-blackcy)), 0, 0, 0))
        Grid.list = list

        break

    cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()