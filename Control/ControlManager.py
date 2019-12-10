import serial
import IK as ik
import delayexample as delay
from Point import Point
from Position import Position

class ControlManager():

    baudRate = 9600
    serPort = "COM3"
    ser = serial.Serial(serPort, baudRate)
    print("Serial port " + serPort + " opened,  Baudrate " + str(baudRate))
    startMarker = 60
    endMarker = 62
    noteCoordinates = [[18, 25, 15], [14, 25, 15], [10, 25, 15], [7, 25, 15], [4, 25, 15], [0, 25, 15], [-3, 25, 15],
                       [-6, 25, 15]]
    notes = ['c6', 'd6', 'e6', 'f6', 'g6', 'a6', 'b6', 'c7']
    speed = 20

    def __init__(self):
        self.currentPosition = None
        self.targetPosition = None

    #   Takes a list of Note objects
    def play(self, notes):
        for i in notes:
            print('[*] Playing note: ', i)
            delay.sleep(i.delay)
            self.hitkey(i.key)

    #   Takes a string c6, d6, e6, f6, g6, a6, b6, c7
    def hitkey(self, a):

        #   TO-DO, get coord from CV
        #   point = Grid.getKey(a) #for instance where Grid is the class that defines the xy grid at the start.
        print('[*] Hitting ', a)
        point = self.noteCoordinates[self.notes.index(a)]
        p = Point(point[0], point[1], point[2])
        self.hit(p)

    #   Takes a point object and translates it to a position object, which in turn is sent to Arduino.
    # def hit(point):
    #     x = point.x
    #     y = point.y
    #     z = point.z
    #     pos = ik.getAngles(point)
    #     sendToArduino(pos)

    def sendToArduino(self, pos):
        string = str(pos.m0) + ', ' + str(pos.m1) + ', ' + str(pos.m2) + '\n'
        # print("inside send to Arduino")
        # print(string)
        b = string.encode('utf-8')
        self.ser.write(b)

    def setCurrent(self, point):
        self.getCurrentPos()
        print('[*] Setting current position to ', point)
        self.currentPoint = point
        curPosAngles = ik.getAngles(point)
        self.currentPosition = Position(curPosAngles[0], curPosAngles[1], curPosAngles[2])
        print('[*] Setting angles for new current position ', self.currentPosition)

    #   I'm not sure what ser.read returns, I guess a string
    #   TO-DO
    def getCurrentPos(self):
        s = self.ser.read()
        print('Current position from arduino: ', s)
        #   currentPosition = s
        #   currentPoint = ik.getCoordinates(currentPosition)

    #   BEWARE  # From hereon out x,y,z might represent motor angles 0,1,2. This will be cleaned up at a later stage
    #   A point is simply translated to a position and the phase one method takes over
    def hit(self, point):
        # speed 0-100 indicates the percentage of the maximal speed that is desired
        path = self.getPath(point, 20)
        xpath = path[0]
        ypath = path[1]
        zpath = path[2]
        leng = int(len(xpath))

        for i in range(0, leng):
            x = xpath[i]
            y = ypath[i]
            z = zpath[i]
            position = Position(x, y, z)
            self.sendToArduino(position)

        # Loop through path & sendToArduino(point in path), delay
        # update current position / point
        self.setCurrent(point)

    def getPath(self, point, speed):
        # TO_DO
        print('[*] Getting path to ', point)

        # curPosAngles = ik.getAngles(currentPosition)
        # curpos = Position(curPosAngles[0], curPosAngles[1], curPosAngles[2])
        curpos = self.currentPosition
        print('[*] Getting angles for current position ', curpos)
        # curpos = ik.getAngles(currentPosition)
        posAngles = ik.getAngles(point)
        pos = Position(posAngles[0], posAngles[1], posAngles[2])
        print('[*] Getting angles for target position ', pos)

        # pos = ik.getAngles(point)

        x0 = curpos.m0
        x1 = pos.m0
        y0 = curpos.m1
        y1 = pos.m1
        z0 = curpos.m2
        z1 = pos.m2

        xpath = []
        ypath = []
        zpath = []
        path = []

        if x1 > x0:
            zmid = z0 + 0.6 * (x1 - x0)
        else:
            zmid = z0 + 0.6 * -(x1 - x0)

        if x1 - x0 == 0:
            zmid = z0 + 20
            for i in range(0, speed):
                x = x0 + (i + 1) * ((x1 - x0) / speed)
                y = y0 + (i + 1) * ((y1 - y0) / speed)

                if i < speed / 2:
                    z = z0 + (i + 1) * (zmid - z0) / speed
                else:
                    z = zmid + (i + 1) * (z1 - zmid) / speed
                xpath.append(x)
                ypath.append(y)
                zpath.append(z)
        else:
            a = (y1 - y0) / (x1 - x0)
            b = y0 - a * x0

            for i in range(0, speed):
                x = x0 + (i + 1) * ((x1 - x0) / speed)
                y = a * x + b
                xpath.append(x)
                ypath.append(y)

                if i < speed / 2:
                    z = z0 + (i + 1) * (zmid - z0) / speed
                else:
                    z = zmid + (i + 1) * (z1 - zmid) / speed
                zpath.append(z)

        path.append(xpath)
        path.append(ypath)
        path.append(zpath)

        return path


