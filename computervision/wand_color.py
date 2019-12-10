import cv2
import numpy
from collections import deque
import imutils

def run():
    cap = cv2.VideoCapture(1)

    width = int(cap.get(3))
    height = int(cap.get(4))
    print(width)
    print(height)


    writer = cv2.VideoWriter('color-vide.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))

    y1 = 50
    y2 = 400
    x1 = 120
    x2 = 480

    while (1):
        _, frame = cap.read()
        frame = frame[y1:y2, x1:x2]  # crop frame

        mask, res = colorDetection(frame)

        try:
            #cv2.imshow('Frame',frame)
            cv2.imshow('Mask', mask)
            cv2.imshow('Res', res)
            writer.write(res)
            #cv2.imshow('Pure Color Detection', res)
        except:
            print("Could not print all requested frames")


        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    writer.release()
    cap.release()
    cv2.destroyAllWindows()



def colorDetection(frame):
    frameoriginal = frame
    framecopy = cv2.medianBlur(frame, 15)

    hsv = cv2.cvtColor(framecopy, cv2.COLOR_BGR2HSV)
    lower_black = numpy.array([0, 0, 0])
    upper_black = numpy.array([190, 255, 30])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    mask = cv2.bitwise_not(mask)
    res= cv2.bitwise_and(frameoriginal, frameoriginal, mask=mask)
    #resblur = cv2.bitwise_and(frame, frame, mask=mask)
    mask = cv2.bitwise_not(mask)


    kernel = numpy.ones((10, 10), numpy.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    kernel = numpy.ones((3, 3), numpy.uint8)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)


    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    #removeSmallAreas(mask, cnts)
    res[mask == 255] = [255, 255, 255]


    #resblur[mask == 255] = [0, 0, 255]
    #cv2.imshow('resblur', resblur)

    res = drawCircle(cnts, res)

    return mask, res

def drawCircle(cnts, frame):
    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        # print("area: ", cv2.contourArea(c))
        # cv2.waitKey(0)

        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            print(radius)
            print((x,y))

        pts.appendleft(center)
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        thickness = int(numpy.sqrt(buffer / float(i + 1)) * 1.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    return frame

def removeSmallAreas(mask, cnts):
    if len(cnts) > 0:
        index = 0
        while index < len(cnts):
            c = cv2.contourArea(cnts[index])
            index += index
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius < 10:
                cv2.drawContours(mask, c, "black")
    return mask

if __name__ == '__main__':
    ff = 0
    buffer = 32
    pts = deque(maxlen=buffer)
    run()