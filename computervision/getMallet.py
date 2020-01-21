import cv2
import numpy
from collections import deque
import imutils
from computervision import VideoCamera as vc
import PIL

cap = None
counter = 0

def run(gui, previous_coordinates, boundarycenterleft, boundarycenterright):
    global cap, counter
    counter = 0
    cap = gui.vid_bird.vid

    # width = int(cap.get(3))
    # height = int(cap.get(4))
    width, height = cap.getDimensions()
    print(width)
    print(height)


    #writer = cv2.VideoWriter('color-vide.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))


    y1 = 0 #50
    y2 = 400
    x1 = 0 #20
    x2 = 480

    while (1):
        ret, frame = cap.getNextFrame()
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

        gui.centerpoints_img = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(cv2.cvtColor(cv2.resize(res, (460, 388)), cv2.COLOR_BGR2RGB)))
        gui.plot_canvas.create_image(gui.canvaswidth / 2, gui.canvasheight / 2,
                                          image=gui.centerpoints_img)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

        if ((x,y))[0] is not None and ((x,y))[1]:
            print(" Mallet ",((x + x1, y + y1), radius))
            #writer.release()
            # cap.release()
            cv2.destroyAllWindows()
            return ((x, y), radius)
        elif counter > 20:
            return ((None, None), None)
        previous_coordinates = (None, None)
        counter += 1
    #writer.release()
    # cap.release()
    cv2.destroyAllWindows()



def colorDetection(frame, prec, bcl, bcr):
    frameoriginal = frame
    framecopy = cv2.medianBlur(frame, 15)

    hsv = cv2.cvtColor(framecopy, cv2.COLOR_BGR2HSV)
    lower_black = numpy.array([0, 0, 0])
    upper_black = numpy.array([100, 255, 30])
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

    # res[mask == 255] = [255, 255, 255]


    #resblur[mask == 255] = [0, 0, 255]
    #cv2.imshow('resblur', resblur)

    res, ((x, y), radius) = drawCircle(cnts, res, prec, bcl, bcr, mask)
    # mask = removeSmallAreas(mask, cnts)

    return mask, res, ((x, y), radius)

def drawCircle(cnts, frame, prec, bcl, bcr, mask):
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
            #print("prec: ", prec)
            #print("newc ", ((x,y), radius)[0])
            # print("x difference: ", abs(((x, y), radius)[0][0] - prec[0]))
            # print("y difference: ", abs(((x, y), radius)[0][1] - prec[1]))
            # print("radius in bounds? ", 30 > radius > 10, " radius: ", radius)
            # print("not outside? ", bcl[0], bcr[0])

            area = cv2.contourArea(c)
            print("area: ", area)

            if 1000 > area > 100 and (bcl[0] + 20 < ((x, y), radius)[0][0] < bcr[0] - 20):  # ((abs(((x, y), radius)[0][0] - prec[0]) < 100 and abs(((x, y), radius)[0][1] - prec[1]) < 100)):
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius-1), (255, 255, 255), cv2.FILLED, 8, 0);
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 3)
                cv2.circle(frame, center, 3, (0, 0, 255), -1)
                # cv2.imshow("mallet frame", frame)
                # cv2.waitKey(500)
                return frame, ((x, y), radius)
    print("No mallet detected")
    # cv2.imshow('frame', frame)
    frame[mask == 255] = [255, 255, 255]
    return frame, ((None, None), None)


def removeSmallAreas(mask, cnts):
    if len(cnts) > 0:
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            try:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            except:
                continue
            # cnt = cv2.contourArea(c)
            if 0 < radius < 0:
                img = cv2.drawContours(img, [c], 0, (255, 255, 255), 3)
    return mask

def destroyWindows():
    global cap
    try:
        cap.release()
        cv2.destroyAllWindows()
    except:
        print("No getMallet() windows to destroy")

if __name__ == '__main__':
    ff = 0
    buffer = 32
    pts = deque(maxlen=buffer)
    run((0,0))