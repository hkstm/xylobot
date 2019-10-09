import cv2
import numpy

# Needs further refining

cap = cv2.VideoCapture("xylotest.mp4")
while(1):
    _, frame = cap.read()
    frame = cv2.medianBlur(frame, 5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_black = numpy.array([0,0,0])
    upper_black = numpy.array([190,255,30])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    mask = cv2.bitwise_not(mask)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    res = cv2.medianBlur(res, 5)
    mask = cv2.bitwise_not(mask)
    res[mask == 255] = [0, 0, 255]
    #cv.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()