from computervision import VideoCamera as vc
import cv2
import PIL

n = 0
cap = None

def run(gui):
    global n, cap
    # cap = gui.vid_bird
    cap = vc.NewVideoCamera(0)
    ret, original_frame = cap.getNextFrame()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fgbg = cv2.createBackgroundSubtractorMOG2()
    while(n < 100):
        ret, frame = cap.getNextFrame()
        # cv2.imshow('Test', frame)

        # mask = motion(frame, fgbg, kernel)

        mask = colors(frame, frame)
        if n  % 3 == 0:
            original_frame = mask

        gui.centerpoints_img = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)))
        gui.plot_canvas.create_image(gui.canvaswidth / 2, gui.canvasheight / 2,
                                          image=gui.centerpoints_img)

        gui.update_log(f"connectedtosetup = False")
        # print("Test:", n)
        # print(cap.vid.getDimensions())
        n += 1
        # cv2.waitKey(100)
    # gui.updateCenterpointsImage()
    gui.update_log("-- Please connect setup and restart --")
    n = 0
    cv2.destroyAllWindows()

def colors(frame, originalframe):
    # firstframe = frame
    ret, frame = cap.getNextFrame()
    # framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # firstframegray = cv2.cvtColor(firstframe, cv2.COLOR_BGR2GRAY)
    frameDelta = cv2.absdiff(originalframe, frame)
    # frameDelta = cv2.bitwise_not(frameDelta)
    return frameDelta

def motion(frame, fgbg, kernel):
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    return fgmask