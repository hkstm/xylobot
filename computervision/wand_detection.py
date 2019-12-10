import cv2
import numpy
from collections import deque
import imutils

# Global variables are to display the last known contour if no new contour is detected
((globalx, globaly), globalradius) = ((1, 1), 1)
globalc = None

def run():
    #Lucas_Kanade()
    #DenseOpticalFlow()
    use_color_detection_also = False

    cap = cv2.VideoCapture(1)
    cv2.CAP_PROP_FRAME_HEIGHT = 500
    cv2.CAP_PROP_FRAME_HEIGHT = 500

    width = int(cap.get(3))
    height = int(cap.get(4))
    print(width)
    print(height)


    writer = cv2.VideoWriter('trackoutput.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))
    firstframe = None

    # _, startingframe = cap.read() # can be used for absolute difference in frames (i.e. a static xylophone without a robot)
    # however it does not work well because of lighting changes causing too big of a difference being identified between
    # the static background frame and the new frame with the robot in sight.

    y1 = 50
    y2 = 400
    x1 = 50
    x2 = 500

    while (1):
        _, frame = cap.read()
        frame = frame[y1:y2, x1:x2]  # crop frame

        if use_color_detection_also is True:
            mask, res = colorDetection(frame)
        else:
            mask = frame


        if firstframe is None:
            firstframe = mask
            _, frame = cap.read()
            frame = frame[y1:y2, x1:x2]  # crop frame


        cdet, firstframe, frameDelta, thresh = circleDetection(frame, firstframe)

        try:
            # cv2.imshow('Frame',frame)
            # cv2.imshow('Mask', mask)
            cv2.imshow('frameDelta', frameDelta)
            cv2.imshow('thresh', thresh)
            cv2.imshow('Tracking', cdet)
            writer.write(frameDelta)
            #cv2.imshow('Pure Color Detection', res)
        except:
            print("Could not print all requested frames")


        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    writer.release()
    cap.release()
    cv2.destroyAllWindows()

def circleDetection(frame, firstframe):
    minarea = 500

    try:
        frameDelta, thresh = motionDetection(frame, firstframe)
        framecopy = frame.copy()
    except:
        frame, res = colorDetection(frame)
        frameDelta, thresh = motionDetection(frame, firstframe)
        framecopy = frame.copy()

    kernel = numpy.ones((20, 20), numpy.uint8)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    #kernel = numpy.ones((3, 3), numpy.uint8)
    #thresh = cv2.dilate(thresh, kernel, iterations=2)

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.medianBlur(thresh, 71)


    frame, firstframe, frameDelta, thresh = contourimage(frame, firstframe, frameDelta, thresh)

    firstframe = framecopy
    return frame, firstframe, frameDelta, thresh

def contourimage(frame, firstframe, frameDelta, thresh):
    global globalradius, globalx, globaly, globalc

    try:
        hsv = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2HSV)
        lower_black = numpy.array([0, 0, 0])
        upper_black = numpy.array([190, 255, 30])
        mask = cv2.inRange(hsv, lower_black, upper_black)
        mask = cv2.bitwise_not(mask)
    except:
        print("Frame is already HSV")
        mask = frameDelta

    kernel = numpy.ones((3, 3), numpy.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.medianBlur(mask, 5)

    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    thresh = mask

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 1:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)

        ((tempx, tempy), tempradius) = cv2.minEnclosingCircle(c)

        if tempradius > 10:
            ((x, y), radius) = ((tempx, tempy), tempradius)
            globalc = c
            globalradius = radius
            (globalx, globaly) = (x, y)
            #M = cv2.moments(c)
            #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            #cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #cv2.circle(frame, (int(globalx), int(globaly)), int(globalradius), (0, 255, 255), 2)

            cv2.drawContours(frame, [globalc], 0, (0, 0, 255), 2)
            #cv2.circle(frame, angle, int(globalradius), (0, 255, 255), 2)

            try:
                RotatedRect = cv2.fitEllipse(globalc)
                cv2.ellipse(frame, RotatedRect, (0, 255, 255), 2)
            except:
                print("Cannot fit ellipse")



    #else:
        #if globalradius > 1:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            #cv2.circle(frame, (int(globalx), int(globaly)), int(globalradius), (0, 255, 255), 2)
            #cv2.circle(thresh, center, int(radius), (255, 255, 255), -1, 8, 0)
            #cv2.drawContours(frame, [globalc], 0, (0, 0, 255), 2)
            #RotatedRect = cv2.fitEllipse(globalc)
            #cv2.ellipse(frame, RotatedRect, (0, 255, 255), 2)

    return frame, firstframe, frameDelta, thresh

def motionDetection(frame, firstframe):
    minarea = 500

    framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    firstframegray = cv2.cvtColor(firstframe, cv2.COLOR_BGR2GRAY)

    frameDelta = cv2.absdiff(firstframegray, framegray)
    cv2.imshow('frameDelta', frameDelta)

    kernel = numpy.ones((10, 10), numpy.uint8)
    thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]

    threshcopy = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)

    #circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1.8, 100, maxRadius=70)
    #if circles is not None:
    #    print(circles)
    #    # convert the (x, y) coordinates and radius of the circles to integers
    #    circles = numpy.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
    #    for (x, y, r) in circles:
    #        # draw the circle in the output image, then draw a rectangle
    #        # corresponding to the center of the circle
    #        cv2.circle(threshcopy, (x, y), r, (0, 0, 255), 4)
    #        cv2.imshow("thresh copy", threshcopy)

    frameDelta = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2RGB)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
    return frameDelta, threshcopy


def colorDetection(frame):
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

    res[mask == 255] = [0, 0, 255]

    #resblur[mask == 255] = [0, 0, 255]
    #cv2.imshow('resblur', resblur)

    return mask, res

def DenseOpticalFlow(): # Code from https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html
    cap = cv2.VideoCapture("wand_tracking_example.mp4")
    ret, frame1 = cap.read()
    prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    hsv = numpy.zeros_like(frame1)
    hsv[..., 1] = 255
    while (1):
        ret, frame2 = cap.read()
        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / numpy.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.imshow('frame2', bgr)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        elif k == ord('s'):
            cv2.imwrite('opticalfb.png', frame2)
            cv2.imwrite('opticalhsv.png', bgr)
        prvs = next

def Lucas_Kanade(): # Code from https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html
    cap = cv2.VideoCapture(1)
    # params for ShiTomasi corner detection
    feature_params = dict(maxCorners=100,
                          qualityLevel=0.3,
                          minDistance=7,
                          blockSize=7)
    # Parameters for lucas kanade optical flow
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    # Create some random colors
    color = numpy.random.randint(0, 255, (100, 3))
    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
    # Create a mask image for drawing purposes
    mask = numpy.zeros_like(old_frame)
    while (1):
        ret, frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        # Select good points
        good_new = p1[st == 1]
        good_old = p0[st == 1]
        # draw the tracks
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
            frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)
        img = cv2.add(frame, mask)
        cv2.imshow('frame', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)

if __name__ == '__main__':
    ff = 0
    buffer = 32
    pts = deque(maxlen=buffer)
    run()