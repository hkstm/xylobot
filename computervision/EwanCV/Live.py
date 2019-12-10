import numpy as np
import cv2

green = np.uint8([[[40, 208, 12]]])
hsvGreen = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
lowerGreen = hsvGreen[0][0][0] - 10, 100, 100
upperGreen = hsvGreen[0][0][0] + 10, 255, 255
lower_green = np.array(lowerGreen)
upper_green = np.array(upperGreen)
blue = np.uint8([[[196, 22, 0]]])

hsvBlue = cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)
lowerBlue = hsvBlue[0][0][0] - 10, 100, 100
upperBlue = hsvBlue[0][0][0] + 10, 255, 255
lower_blue = np.array(lowerBlue)
upper_blue = np.array(upperBlue)
white = np.uint8([[[255, 255, 255]]])

hsvWhite = cv2.cvtColor(white, cv2.COLOR_BGR2HSV)
lowerWhite = hsvWhite[0][0][0] - 50, 0, 0
upperWhite = hsvWhite[0][0][0] + 50, 10, 255
print(lowerWhite)
lower_white = np.array(lowerWhite)
upper_white = np.array(upperWhite)

cap = cv2.VideoCapture(1)

while(True):
    ret, frame = cap.read()
    frame = frame[50:350, 50:650]
    template = cv2.imread('xytempl.jpg', 0)
    blur = cv2.GaussianBlur(frame, (9, 9), 0)
    edges = cv2.Canny(blur, 100, 200)
    cv2.imshow('Edges', edges)
    test = cv2.matchTemplate(edges, template, eval('cv2.TM_CCOEFF '))
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(test)
    (startX, startY) = (int(maxLoc[0]), int(maxLoc[1]))
    (endX, endY) = (int((maxLoc[0])), int((maxLoc[1])))

    # draw a bounding box around the detected result and display the image
    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.imshow("Image", frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()