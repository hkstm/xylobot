import xylobot.IK as ik
from xylobot.Control.Hit import *


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
    SPEED = 50

    def __init__(self, ser):
        self.ser = ser
        self.power = 0
        self.currentPosition = Point(0, 25, 15)
        self.targetPosition = None
        self.qh = QuadraticHit()
        self.rh = RightAngledTriangularHit()
        self.th = TriangularHit()
        self.uh = UniformHit()

    def sendToArduino(self, pos):
        string = str(pos.m0) + ', ' + str(pos.m1) + ', ' + str(pos.m2) + '\n'
        b = string.encode('utf-8')
        self.ser.write(b)

    def hit(self, note):
        self.targetPosition = note.coords
        self.qh.set(self.currentPosition, self.targetPosition, self.SPEED)

        path = self.qh.getPath()
        anglepath = []

        for i in path:
            pos = ik.getAngles(i)
            anglepath.append(Position(pos[0], pos[1], pos[2]))

        for p in anglepath:
            self.sendToArduino(p)

        self.setCurrent(path[len(path) - 1])

    def setCurrent(self, point):
        self.currentPosition = point

    def getCurrentPos(self):
        print(self.ser.read())


