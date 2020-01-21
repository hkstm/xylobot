import numpy as np
import cv2
from computervision import Grid
from computervision.CenterPoint import CenterPoint
from computervision import VideoCamera as vc
import PIL


cap = None
DONE = False
finalObj = None
bready = False
b2ready = False
finalObj2 = None
swapped = False
list = []
boundarycenterleft = None
boundarycenterright = None

def run(gui):
    global finalObj, DONE, bready, b2ready, finalObj2, list, swapped, boundarycenterleft, boundarycenterright, cap
    cap = gui.vid_bird.vid
    width, height = cap.getDimensions()
    swapped = False
    #bready = False
    #b2ready = False
    while(DONE == False):
        ret, frame = cap.getNextFrame()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # cv2.imshow('hsv', hsv)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([60, 80, 50])
        mask = cv2.inRange(hsv, lower_black, upper_black)
        # cv2.imshow('original', mask)
        kernel = np.ones((2, 2), np.uint8)
        erode = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.dilate(erode, kernel, iterations=1)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_CLOSE, kernel)
        mask = dilatemask
        # cv2.imshow('blackmask', mask)
        blackcnts = cv2.findContours(mask.copy(),
                                     cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)[-2]
        try:
            if len(blackcnts) > 0:
                black_area = max(blackcnts, key=cv2.contourArea)
                Obj = cv2.fitEllipse(black_area)
                center = Obj[0]
                size = Obj[1]
                if (size[0] > 16 and size[0] < 25 and size[1] > 100 and size[1] < 130):
                    finalObj = Obj
                    bready = True
                elif (size[0] > 14 and size[0] < 25 and size[1] > 150 and size[1] < 200):
                    finalObj2 = Obj
                    b2ready = True
        except Exception as e:
            continue

#SECOND HALF!!!!!!!!!!!!!!!!!!!!!!!!!!

#Crop image
        if bready:
            print("bready x: ", int(finalObj[0][0]))
            if int(finalObj[0][0]) > int(width/2):
                offsetright = int(width/2)
                offset = 0
            else:
                offset = int(finalObj[0][0]) + 370
                offsetright = 640
        elif b2ready:
            print("b2ready x: ", int(finalObj2[0][0]))
            if int(finalObj2[0][0]) > int(width/2):
                offsetright = int(width/2)
                offset = 0
            else:
                offset = int(finalObj2[0][0]) + 370
                offsetright = 640
        else:
            offset = 420
            offsetright = 640
        crop = frame[0:height, offset:offsetright]
        # cv2.imshow('crop', crop)
#Change to hsv, find black mask, reduce noise using morphology
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_black, upper_black)
        kernel = np.ones((2, 2), np.uint8)
        erode = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.dilate(erode, kernel, iterations=1)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((3, 3), np.uint8)
        dilatemask = cv2.morphologyEx(dilatemask, cv2.MORPH_CLOSE, kernel)
        mask = dilatemask

#Finding Contours and Ellipses
        blackcnts = cv2.findContours(mask.copy(),
                                     cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)[-2]
        try:
            if len(blackcnts) > 0:
                black_area = max(blackcnts, key=cv2.contourArea)
                Obj2 = cv2.fitEllipse(black_area)
                angle = Obj[2]
                center = Obj2[0]
                size = Obj2[1]
                center = (center[0] + offset, center[1])
                Obj2 = (center, size, angle)
                if (size[0] > 16 and size[0] < 25 and size[1] > 100 and size[1] < 130):
                    finalObj = Obj2
                    bready = True
                elif (size[0] > 14 and size[0] < 25 and size[1] > 150 and size[1] < 200):
                    finalObj2 = Obj2
                    b2ready = True
        except Exception as e:
            continue
        
        if bready:
            cv2.ellipse(frame, finalObj, (0, 255, 255), 2)
            cv2.circle(frame, (int(finalObj[0][0]), int(finalObj[0][1])), 1, (0, 0, 255), 3)
            boundarycenterleft = (int(finalObj[0][0]), int(finalObj[0][1]))
        if b2ready:
            cv2.ellipse(frame, finalObj2, (255, 0, 0), 2)
            cv2.circle(frame, (int(finalObj2[0][0]), int(finalObj2[0][1])), 1, (0, 0, 255), 3)
            boundarycenterright = (int(finalObj2[0][0]), int(finalObj2[0][1]))
        if b2ready and bready and (abs(int(finalObj2[0][0]) - int(finalObj[0][0])) > 100 or abs(int(finalObj2[0][1]) - int(finalObj[0][1])) > 100):
            swapped = False
            if ((int(finalObj2[0][0]) - int(finalObj[0][0])) < 0):#CHECK WITH RHYS
                boundarycenterleft = (int(finalObj2[0][0]), int(finalObj2[0][1]))
                boundarycenterright = (int(finalObj[0][0]), int(finalObj[0][1]))
                print((int(finalObj2[0][0]) - int(finalObj[0][0])))
                temp = finalObj
                finalObj = finalObj2
                finalObj2 = temp
                swapped = True
            lineThickness = 2
            cv2.line(frame, (int(finalObj[0][0]), int(finalObj[0][1])), (int(finalObj2[0][0]), int(finalObj2[0][1])), (0, 255, 0), lineThickness)
            cv2.circle(frame, (int(finalObj[0][0] + (1 / 9) * (finalObj2[0][0] - finalObj[0][0])), int((finalObj[0][1] + (1 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1,(0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (2 / 9)*(finalObj2[0][0]-finalObj[0][0])), int((finalObj[0][1] + (2/9)*(finalObj2[0][1]-finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (3 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (3 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (4 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (4 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (5 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (5 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (6 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (6 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (7 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (7 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            cv2.circle(frame, (int(finalObj[0][0] + (8 / 9) * (finalObj2[0][0] - finalObj[0][0])),
                               int((finalObj[0][1] + (8 / 9) * (finalObj2[0][1] - finalObj[0][1])))), 1, (0, 0, 255), 3)
            #print(" List Found")
            if swapped: #CHECK WITH RHYS
                createList2(int(finalObj[0][0]), int(finalObj2[0][0]), int(finalObj[0][1]), int(finalObj2[0][1]))
            else:
                createList1(int(finalObj[0][0]), int(finalObj2[0][0]), int(finalObj[0][1]), int(finalObj2[0][1]))

            cv2.imwrite('centerpoints.jpg', cv2.resize(frame, (int(gui.canvaswidth), int(gui.canvasheight))))
            print('Image saved')
            DONE = True

        # cv2.imshow('frame', frame)
        if frame is not None:
            gui.centerpoints_img = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(cv2.cvtColor(cv2.resize(frame, (int(gui.canvaswidth), int(gui.canvasheight))), cv2.COLOR_BGR2RGB)))
            gui.plot_canvas.create_image(gui.canvaswidth / 2, gui.canvasheight / 2, image=gui.centerpoints_img)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    #cap.release()
    cv2.destroyAllWindows()

def Swapped():
    global swapped
    return swapped

def getList():
    global list
    return list

def createList1(blackcx, black2cx, blackcy, black2cy):
    global list
    print(" LIST CERATED NORMAL")
    list.append(CenterPoint("c6", int(blackcx + (8 / 9) * (black2cx - blackcx)),
                            int(blackcy + (8 / 9) * (black2cy - blackcy)), 0, 0, 0))
    list.append(
        CenterPoint("d6", int(blackcx + (7 / 9) * (black2cx - blackcx)), int(blackcy + (7 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("e6", int(blackcx + (6 / 9) * (black2cx - blackcx)), int(blackcy + (6 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("f6", int(blackcx + (5 / 9) * (black2cx - blackcx)), int(blackcy + (5 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("g6", int(blackcx + (4 / 9) * (black2cx - blackcx)), int(blackcy + (4 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("a6", int(blackcx + (3 / 9) * (black2cx - blackcx)), int(blackcy + (3 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("b6", int(blackcx + (2 / 9) * (black2cx - blackcx)), int(blackcy + (2 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("c7", int(blackcx + (1 / 9) * (black2cx - blackcx)), int(blackcy + (1 / 9) * (black2cy - blackcy)),
                    0, 0, 0))

def createList2(blackcx, black2cx, blackcy, black2cy):
    global list
    print(" LIST CERATED SWAPPED")
    list.append(CenterPoint("c7", int(blackcx + (8 / 9) * (black2cx - blackcx)),
                            int(blackcy + (8 / 9) * (black2cy - blackcy)), 0, 0, 0))
    list.append(
        CenterPoint("b6", int(blackcx + (7 / 9) * (black2cx - blackcx)), int(blackcy + (7 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("a6", int(blackcx + (6 / 9) * (black2cx - blackcx)), int(blackcy + (6 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("g6", int(blackcx + (5 / 9) * (black2cx - blackcx)), int(blackcy + (5 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("e6", int(blackcx + (4 / 9) * (black2cx - blackcx)), int(blackcy + (4 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("f6", int(blackcx + (3 / 9) * (black2cx - blackcx)), int(blackcy + (3 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("d6", int(blackcx + (2 / 9) * (black2cx - blackcx)), int(blackcy + (2 / 9) * (black2cy - blackcy)),
                    0, 0, 0))
    list.append(
        CenterPoint("c6", int(blackcx + (1 / 9) * (black2cx - blackcx)), int(blackcy + (1 / 9) * (black2cy - blackcy)),
                    0, 0, 0))

def getBoundaryMidpoints():
    global boundarycenterleft, boundarycenterright
    return boundarycenterleft, boundarycenterright

def destroyWindows():
    try:
        cap.release()
        cv2.destroyAllWindows()
    except:
        print("No getSides() windows to destroy")

if __name__ == '__main__':
    run()
