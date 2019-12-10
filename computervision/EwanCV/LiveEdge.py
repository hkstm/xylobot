import numpy as np
import cv2

cap = cv2.VideoCapture(1)
pready = False
bready = False
gready = False
while(True):
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(frame, (9, 9), 0)
    edges = cv2.Canny(blur, 100, 200)
    cv2.imshow('Edges', edges)

# !!!!PURPLE!!!!

    lower_purple = np.array([140, 120, 40])
    upper_purple = np.array([170, 170, 110])

    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    kernel = np.ones((7, 7), np.uint8)
    dilatemask = cv2.dilate(mask, kernel, iterations=1)
    resp = cv2.bitwise_and(frame, frame, mask=dilatemask)

    resp2 = cv2.bitwise_and(edges, edges, mask=dilatemask)

    purpcnts = cv2.findContours(resp2.copy(),
                                 cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(purpcnts) > 0:
        green_area = max(purpcnts, key=cv2.contourArea)
        (xg, yg, wg, hg) = cv2.boundingRect(green_area)
        if hg > 137:
            test12=1
            #print(hg)
            #print(wg)

    if 145 > hg > 137 and 38 > wg > 30:
        pready = True
        purplex = xg
        purpley = yg
        purpleh = hg
        purplew = wg
        purplecx = int(purplex + (purplew/2))
        purplecy = int(purpley + (purpleh/2))
        #print('done')


#!!!!SMALLBLUE!!!!

    lower_blue = np.array([100, 50, 20])
    upper_blue = np.array([130, 255, 100])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = np.ones((7, 7), np.uint8)
    dilatemask = cv2.dilate(mask, kernel, iterations=1)
    resb = cv2.bitwise_and(frame, frame, mask=dilatemask)

    resb2 = cv2.bitwise_and(edges, edges, mask=dilatemask)

    bluecnts = cv2.findContours(resb2.copy(),
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(bluecnts) > 0:
        green_area = max(bluecnts, key=cv2.contourArea)
        (xg, yg, wg, hg) = cv2.boundingRect(green_area)
        #if hg > 137:
        #print(hg)
        #print(wg)

    if 135 > hg > 125 and 40 > wg > 30:
        bready = True
        bluex = xg
        bluey = yg
        blueh = hg
        bluew = wg
        bluecx = int(bluex + (bluew / 2))
        bluecy = int(bluey + (blueh / 2))
        print('done')



#!!!!GREEN!!!!

    lower_green = np.array([0, 0, 0])
    upper_green = np.array([180, 255, 10])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    kernel = np.ones((7, 7), np.uint8)
    dilatemask = cv2.dilate(mask, kernel, iterations=1)
    resg = cv2.bitwise_and(frame, frame, mask=dilatemask)
    cv2.imshow('green', resg)
    resg2 = cv2.bitwise_and(edges, edges, mask=dilatemask)

    greencnts = cv2.findContours(resg2.copy(),
                                 cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(greencnts) > 0:
        green_area = max(greencnts, key=cv2.contourArea)
        (xg, yg, wg, hg) = cv2.boundingRect(green_area)
        if hg > 135:
            print(hg)
            print(wg)

    if 145 > hg > 135 and 30 > wg > 25:
        gready = True
        greenx = xg
        greeny = yg
        greenh = hg
        greenw = wg
        greencx = int(greenx + (greenw / 2))
        greency = int(greeny + (greenh / 2))
        print('done')

    if gready:
        cv2.rectangle(frame, (greenx, greeny), (greenx + greenw, greeny + greenh), (0, 0, 255), 2)
        cv2.circle(frame, (greencx, greency), 1, (0, 0, 255), 3)
    if bready:
        cv2.rectangle(frame, (bluex, bluey), (bluex + bluew, bluey + blueh), (0, 0, 255), 2)
        cv2.circle(frame, (bluecx, bluecy), 1, (0, 0, 255), 3)
    if pready:
        cv2.rectangle(frame, (purplex, purpley), (purplex + purplew, purpley + purpleh), (0, 0, 255), 2)
        cv2.circle(frame, (purplecx, purplecy), 1, (0, 0, 255), 3)


    cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()