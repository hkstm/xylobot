import cv2
import numpy

# Needs further refining

def run():
    cap = cv2.VideoCapture(1)
    while (1):
        _, frame = cap.read()
        mask, res = colorDetection(frame)
        #circleDetection(mask, frame) # DOES NOT WORK (yet?)

        # cv.imshow('frame',frame)
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()

def circleDetection(mask, frame): # DOES NOT WORK (yet?)
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
    run()
    #circleDetection(0, 0)