import numpy as np
import cv2

cap = cv2.VideoCapture(1)
while(True):
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(frame, (9, 9), 0)
    edges = cv2.Canny(blur, 100, 200)
    cv2.imshow('Edges', edges)

    cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()