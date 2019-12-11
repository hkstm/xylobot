from xylobot.Position import Position
from xylobot.Point import Point
import xylobot.IK as ik


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)


class Position:
    def __init__(self, m0, m1, m2):
        self.m0 = m0
        self.m1 = m1
        self.m2 = m2

    def __str__(self):
        return "({}, {}, {})".format(self.m0, self.m1, self.m2)


class HitManager:
    def __init__(self, ser):
        self.ser = ser
        self.power = 0
        self.currentPosition = None
        self.targetPosition = None

    def sendToArduino(self, pos):
        string = str(pos.m0) + ', ' + str(pos.m1) + ', ' + str(pos.m2) + '\n'
        b = string.encode('utf-8')
        self.ser.write(b)

    def hitkey(self, a):

        #   TO-DO, get coord from CV
        #   point = Grid.getKey(a) #for instance where Grid is the class that defines the xy grid at the start.
        print('[*] Hitting ', a)
        point = self.noteCoordinates[self.notes.index(a)]
        p = Point(point[0], point[1], point[2])
        self.hit(p)

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

        curpos = self.currentPosition
        print('[*] Getting angles for current position ', curpos)
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

    def setCurrent(self, point):
        print('[*] Setting current position to ', point)
        self.currentPoint = point
        curPosAngles = ik.getAngles(point)
        self.currentPosition = Position(curPosAngles[0], curPosAngles[1], curPosAngles[2])
        print('[*] Setting angles for new current position ', self.currentPosition)

    def getCurrentPos(self):
        print(self.ser.read())


