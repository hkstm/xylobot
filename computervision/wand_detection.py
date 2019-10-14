import cv2
import numpy
from collections import deque
import imutils

def run():
    cap = cv2.VideoCapture(1)
    while (1):
        _, frame = cap.read()
        mask, res = colorDetection(frame)
        cdet = circleDetection(mask, frame)

        # cv.imshow('Frame',frame)
        cv2.imshow('Mask', mask)
        # cv2.imshow('Result', res)
        cv2.imshow('Tracking', cdet)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()

def circleDetection(mask, frame):
    """
    #image = cv2.imread("sample_mask.png")
    #image2 = cv2.imread("capture.jpg")
    mask = cv2.bitwise_not(mask)
    image = mask
    output = frame.copy()
    gray = image #cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 300, numpy.array([]), 10, 30, 60, 300)
    if circles is not None and len(circles) != 0:
        print(len(circles))
        circles = numpy.uint16(numpy.around(circles))
        for i in circles[0,:]:
            cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 1)
            cv2.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.imshow("Output", output)
    """

    # Hough Circle Transformation (above) did not work
    # Therefore, tutorial from https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/ was followed

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    """
    # This code can be modified to delete incorrect contours
    
    for cnt in cnts:
        if cv2.contourArea(cnt) < 3000:
            cnts.remove(cnt)
    center = None
    """

    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        #print("area: ", cv2.contourArea(c))
        #cv2.waitKey(0)

        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

        pts.appendleft(center)
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        thickness = int(numpy.sqrt(buffer / float(i + 1)) * 1.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    return frame

def colorDetection(frame):
    frameoriginal = frame
    frame = cv2.medianBlur(frame, 15)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
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
    mask = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)

    res[mask == 255] = [0, 0, 255]

    #resblur[mask == 255] = [0, 0, 255]
    #cv2.imshow('resblur', resblur)

    return mask, res

if __name__ == '__main__':
    buffer = 32
    pts = deque(maxlen=buffer)
    run()