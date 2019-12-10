import numpy as np
import cv2

image = cv2.imread("Xylophone.jpeg")
green = np.uint8([[[0, 255, 0]]])
hsvGreen = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
lowerGreen = hsvGreen[0][0][0] - 10, 100, 100
upperGreen = hsvGreen[0][0][0] + 10, 255, 255
lower_green = np.array(lowerGreen)
upper_green = np.array(upperGreen)
red = np.uint8([[[0, 0, 255]]])
hsvRed = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
lowerRed = hsvRed[0][0][0] - 5, 100, 100
upperRed = hsvRed[0][0][0] + 5, 255, 255
lower_red = np.array(lowerRed)
upper_red = np.array(upperRed)
orange = np.uint8([[[0, 119, 255]]])
hsvOrange = cv2.cvtColor(orange, cv2.COLOR_BGR2HSV)
lowerOrange = hsvOrange[0][0][0] - 3, 100, 100
upperOrange = hsvOrange[0][0][0] + 3, 255, 255
lower_orange = np.array(lowerOrange)
upper_orange = np.array(upperOrange)
purple = np.uint8([[[255, 0, 166]]])
hsvPurple = cv2.cvtColor(purple, cv2.COLOR_BGR2HSV)
lowerPurple = hsvPurple[0][0][0] - 10, 100, 100
upperPurple = hsvPurple[0][0][0] + 10, 255, 255
lower_purple = np.array(lowerPurple)
upper_purple = np.array(upperPurple)
blue = np.uint8([[[135, 2, 0]]])
hsvBlue = cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)
lowerBlue = hsvBlue[0][0][0] - 10, 100, 100
upperBlue = hsvBlue[0][0][0] + 10, 255, 255
lower_blue = np.array(lowerBlue)
upper_blue = np.array(upperBlue)


while(True):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_mask = cv2.bitwise_not(green_mask)

    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    red_mask = cv2.bitwise_not(red_mask)

    orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)
    orange_mask = cv2.bitwise_not(orange_mask)

    purple_mask = cv2.inRange(hsv, lower_purple, upper_purple)
    purple_mask = cv2.bitwise_not(purple_mask)

    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blue_mask = cv2.bitwise_not(blue_mask)


    #all_mask = green_mask + red_mask
    #all_mask = green_mask + orange_mask
    all_mask = orange_mask

    final = cv2.bitwise_and(image, image, mask = all_mask)
    final = cv2.medianBlur(final, 5)
    all_mask = cv2.bitwise_not(all_mask)
    final[all_mask == 255] = [255, 0, 0]
    cv2.imshow('image', image)
    cv2.imshow('final', final)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()