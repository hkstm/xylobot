import cv2
import numpy
from collections import deque
import imutils

def run(previous_coordinates, boundarycenterleft, boundarycenterright):
    cap = cv2.VideoCapture(1)

    width = int(cap.get(3))
    height = int(cap.get(4))
    print(width)
    print(height)


    #writer = cv2.VideoWriter('color-vide.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))


    y1 = 0 #50
    y2 = 400
    x1 = 0 #20
    x2 = 480

    while (1):
        _, frame = cap.read()
        #frame = frame[y1:y2, x1:x2]  # crop frame

        mask, res, ((x, y), radius) = colorDetection(frame, previous_coordinates, boundarycenterleft, boundarycenterright)

        #try:
            #cv2.imshow('Frame',frame)
            #cv2.imshow('Mask', mask)
            #cv2.imshow('Res', res)
            #cv2.imwrite('res.jpg', res)
            #writer.write(res)
            #cv2.imshow('Pure Color Detection', res)
        #except:
            #print("Could not print all requested frames")

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

        if ((x,y))[0] is not None and ((x,y))[1]:
            print(" Mallet ",((x + x1, y + y1), radius))
            #writer.release()
            cap.release()
            cv2.destroyAllWindows()
            return ((x, y), radius)
    #writer.release()
    cap.release()
    cv2.destroyAllWindows()



def colorDetection(frame, prec, bcl, bcr):
    frameoriginal = frame
    framecopy = cv2.medianBlur(frame, 15)

    hsv = cv2.cvtColor(framecopy, cv2.COLOR_BGR2HSV)
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
    #mask = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)


    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    #removeSmallAreas(mask, cnts)
    res[mask == 255] = [255, 255, 255]


    #resblur[mask == 255] = [0, 0, 255]
    #cv2.imshow('resblur', resblur)

    res, ((x, y), radius) = drawCircle(cnts, res, prec, bcl, bcr)

    return mask, res, ((x, y), radius)

def drawCircle(cnts, frame, prec, bcl, bcr):
    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        # print("area: ", cv2.contourArea(c))
        # cv2.waitKey(0)
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            try:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            except:
                continue
            if prec == (None, None):
                prec = ((x,y), radius)[0]
            print("prec: ", prec)
            print("newc ", ((x,y), radius)[0])
            if 60 > radius > 10 and (bcl[0] + 5 < ((x, y), radius)[0][0] < bcr[0] - 5): # and (abs(((x, y), radius)[0][0] - prec[0]) < 100 and abs(((x, y), radius)[0][1] - prec[1]) < 100)
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                return frame, ((x, y), radius)
    print("No mallet detected")
    cv2.imshow('frame', frame)
    return frame, ((None, None), None)


def removeSmallAreas(mask, cnts):
    if len(cnts) > 0:
        for cnt in cnts:
            c = cv2.contourArea(cnt)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius < 10:
                cv2.drawContours(mask, c, "black")
    return mask

if __name__ == '__main__':
    ff = 0
    buffer = 32
    pts = deque(maxlen=buffer)
    run((0,0))