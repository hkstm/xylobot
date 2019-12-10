import numpy as np
import cv2

image = cv2.imread("Xylophone.jpeg")
cv2.imwrite("canny.jpg", cv2.Canny(image, 200, 300))
cv2.imshow("canny", cv2.imread("canny.jpg"))
cv2.waitKey()
cv2.destroyAllWindows()