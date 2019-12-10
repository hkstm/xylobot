import numpy as np
import cv2

image = cv2.imread("Xylophone3.jpeg")
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



hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

green_mask = cv2.inRange(hsv, lower_green, upper_green)

blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

white_mask = cv2.inRange(hsv, lower_white, upper_white)

greencnts = cv2.findContours(green_mask.copy(),
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
if len(greencnts) > 0:
    green_area = max(greencnts, key=cv2.contourArea)
    (xg, yg, wg, hg) = cv2.boundingRect(green_area)
    cv2.rectangle(image, (xg, yg), (xg + wg, yg + hg), (0, 0, 255), 2)

green_x = xg
green_y = yg
green_height = hg
green_width = wg
green_centerx = int(green_x + (green_width/2))
green_centery = int(green_y + (green_height/2))

cv2.circle(image, (green_centerx, green_centery), 2, (0, 0, 255), 5)

bluecnts = cv2.findContours(blue_mask.copy(),
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

if len(bluecnts) > 0:
    blue_area = max(bluecnts, key=cv2.contourArea)
    (xg, yg, wg, hg) = cv2.boundingRect(blue_area)
    cv2.rectangle(image, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)

blue_x = xg
blue_y = yg
blue_height = hg
blue_width = wg
blue_centerx = int(blue_x + (blue_width/2))
blue_centery = int(blue_y + (blue_height/2))

cv2.circle(image, (blue_centerx, blue_centery), 2, (0, 255, 0), 5)

whitecnts = cv2.findContours(white_mask.copy(),
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

if len(whitecnts) > 0:
    white_area = max(whitecnts, key=cv2.contourArea)
    (xg, yg, wg, hg) = cv2.boundingRect(white_area)
    cv2.rectangle(image, (xg, yg), (xg + wg, yg + hg), (0, 0, 0), 2)

white_x = xg
white_y = yg
white_height = hg
white_width = wg
white_centerx = int(white_x + (white_width/2))
white_centery = int(white_y + (white_height/2))

cv2.circle(image, (white_centerx, white_centery), 2, (0, 0, 0), 5)

avg_width =int((blue_width + green_width + white_width) / 3)
height_diff = int(((blue_height - green_height) + ((green_height - white_height) / 3))/2)
space_between = (green_x - (blue_x +blue_width))

xg = green_x + green_width + space_between
yg = int(green_y + (height_diff/2))
wg = int(avg_width)
hg = int(green_height - (height_diff/2))
cx = int(xg + (wg/2))
cy = int(yg + (hg/2))


cv2.rectangle(image, (xg, yg), (xg + wg, yg + hg), (255, 150, 0), 2)
cv2.circle(image, (cx, cy), 2, (255, 150, 0), 5)

space_between = int((white_x -(4*avg_width) - (green_x + green_width))/5)

for x in range(3):

    xg = xg + wg + space_between
    yg = int(yg + (height_diff / 2))
    hg = hg - height_diff
    cx = int(xg + (wg / 2))
    cy = int(yg + (hg / 2))
    cv2.rectangle(image, (xg, yg), (xg + wg, yg + hg), (255, 150, 0), 2)
    cv2.circle(image, (cx, cy), 2, (255, 150, 0), 5)

xg = white_x + white_width + space_between
yg = int(white_y + (height_diff/2))
hg = int(white_height - (height_diff/2))
cx = int(xg + (wg/2))
cy = int(yg + (hg/2))

cv2.rectangle(image, (xg, yg), (xg + wg, yg + hg), (255, 150, 0), 2)
cv2.circle(image, (cx, cy), 2, (255, 150, 0), 5)

while True:
    cv2.imshow('image', image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()