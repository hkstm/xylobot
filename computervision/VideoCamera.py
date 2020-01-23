import cv2
import threading

class NewVideoCamera(object):
    # filename can be 0 to access the webcam - code used from https://stackoverflow.com/questions/50660947/how-to-access-1-webcam-with-2-threads
    def __init__(self, filename = '0'):
        self.lock = threading.Lock()
        self.openVideo(filename)

    def openVideo(self, filename):
        self.lock.acquire()
        self.videoCap = cv2.VideoCapture(filename)
        # print('format: ', self.videoCap.get(cv2.CAP_PROP_FORMAT))
        self.lock.release()

    def getNextFrame(self):
        self.lock.acquire()
        frame = None
        ret = False
        # if no video opened return None
        if self.videoCap.isOpened():
            ret, frame = self.videoCap.read()
        self.lock.release()
        return ret, frame

    def getDimensions(self):
        width = int(self.videoCap.get(3))
        height = int(self.videoCap.get(4))
        return width, height

    def getCap(self):
        return self.videoCap()

    def isOpen(self):
        return self.videoCap.isOpened()

    # def setDimensions(self, width, height):
    #     self.videoCap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    #     self.videoCap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def release(self):
        self.videoCap.release()
        cv2.destroyAllWindows()
