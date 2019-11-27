import cv2
import numpy
from collections import deque
import imutils

# Global variables are to display the last known contour if no new contour is detected
((globalx, globaly), globalradius) = ((1, 1), 1)
globalc = None

def run():
    use_color_detection_also = True

    cap = cv2.VideoCapture(1)
    width = int(cap.get(3))
    height = int(cap.get(4))
    print(width)
    print(height)

    writer = cv2.VideoWriter('trackoutput.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))
    firstframe = None

    # _, startingframe = cap.read() # can be used for absolute difference in frames (i.e. a static xylophone without a robot)
    # however it does not work well because of lighting changes causing too big of a difference being identified between
    # the static background frame and the new frame with the robot in sight.

    while (1):
        _, frame = cap.read()

        if use_color_detection_also is True:
            mask, res = colorDetection(frame)
        else:
            mask = frame
            _, frame = cap.read()

        if firstframe is None:
            firstframe = mask

        cdet, firstframe, frameDelta, thresh = circleDetection(mask, frame, firstframe)

        try:
            # cv.imshow('Frame',frame)
            # cv2.imshow('Mask', mask)
            cv2.imshow('frameDelta', frameDelta)
            cv2.imshow('thresh', thresh)
            cv2.imshow('Tracking', cdet)
            writer.write(cdet)
            #cv2.imshow('Pure Color Detection', res)
        except:
            print("Could not print all requested frames")


        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    writer.release()
    cap.release()
    cv2.destroyAllWindows()

def circleDetection(mask, frame, firstframe):
    minarea = 500

    try:
        framecopy = frame.copy()
        frameDelta = cv2.absdiff(firstframe, frame)
    except:
        framecopy = mask.copy()
        frameDelta = cv2.absdiff(firstframe, mask)

    kernel = numpy.ones((20, 20), numpy.uint8)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    #kernel = numpy.ones((3, 3), numpy.uint8)

    #thresh = cv2.dilate(thresh, kernel, iterations=2)
    thresh = cv2.medianBlur(thresh, 31)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    frame, firstframe, frameDelta, thresh = contourimage(frame, firstframe, frameDelta, thresh)

    firstframe = framecopy
    return frame, firstframe, frameDelta, thresh

def contourimage(frame, firstframe, frameDelta, thresh):
    global globalradius, globalx, globaly, globalc

    try:
        hsv = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2HSV)
        lower_black = numpy.array([0, 0, 0])
        upper_black = numpy.array([190, 255, 30])
        mask = cv2.inRange(hsv, lower_black, upper_black)
        mask = cv2.bitwise_not(mask)
    except:
        print("Frame is already HSV")
        mask = frameDelta

    kernel = numpy.ones((3, 3), numpy.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.medianBlur(mask, 5)

    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    thresh = mask

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 1:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)

        ((tempx, tempy), tempradius) = cv2.minEnclosingCircle(c)

        if tempradius > 10:
            ((x, y), radius) = ((tempx, tempy), tempradius)
            globalc = c
            globalradius = radius
            (globalx, globaly) = (x, y)
            #M = cv2.moments(c)
            #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            #cv2.circle(frame, center, 5, (0, 0, 255), -1)
            cv2.circle(frame, (int(globalx), int(globaly)), int(globalradius),
                       (0, 255, 255), 2)
            cv2.drawContours(frame, [globalc], 0, (0, 0, 255), 2)
    else:
        if globalradius > 1:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(globalx), int(globaly)), int(globalradius),
                       (0, 255, 255), 2)
            #cv2.circle(thresh, center, int(radius), (255, 255, 255), -1, 8, 0)
            cv2.drawContours(frame, [globalc], 0, (0, 0, 255), 2)

    return frame, firstframe, frameDelta, thresh

def motionDetection(frame, firstframe):
    minarea = 500

    frameDelta = cv2.absdiff(firstframe, frame)
    cv2.imshow('frameDelta', frameDelta)

    kernel = numpy.ones((10, 10), numpy.uint8)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    return frameDelta, thresh


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

    res[mask == 255] = [0, 0, 255]

    #resblur[mask == 255] = [0, 0, 255]
    #cv2.imshow('resblur', resblur)

    return mask, res

if __name__ == '__main__':
    ff = 0
    buffer = 32
    pts = deque(maxlen=buffer)
    run()