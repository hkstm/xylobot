import cv2
import numpy as np

u = np.uint8([[[0, 236, 236]]])
import numpy as np
import cv2

green = np.uint8([[[0, 255, 0]]])
hsvGreen = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
print(hsvGreen)

lowerLimit = hsvGreen[0][0][0] - 10, 100, 100
upperLimit = hsvGreen[0][0][0] + 10, 255, 255

print(upperLimit)
print(lowerLimit)