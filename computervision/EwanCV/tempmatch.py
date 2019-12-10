import numpy as np
import cv2
import imutils

cap = cv2.VideoCapture(1)
template = cv2.imread('temp.jpg')
cv2.imshow("template", template)
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found = None

    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        resized = imutils.resize


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()