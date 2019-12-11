import xylobot.IK as ik
from xylobot.Control.Hit import *
from xylobot.Point import Point
from xylobot.Position import Position


class HitManager:
    SPEED = 1

    def __init__(self, ser):
        self.ser = ser
        self.power = 0
        self.currentPosition = Point(0, 25, 12)
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
        if (self.targetPosition.x == self.currentPosition.x):
            print('Target same as origin, won\'t move!')
        else:
            self.qh.set(self.currentPosition, self.targetPosition, self.SPEED)

        path = self.qh.getPath()
        print('Points: ')
        for p in path:
            print(p)
        #anglepath = []

        #for i in path:
        #    pos = ik.getAngles(i)
        #    #anglepath.append(Position(pos[0], pos[1], pos[2]))
        #    self.sendToArduino(Position(pos[0], pos[1], pos[2]))

        #for p in anglepath:
        #    self.sendToArduino(p)

        self.setCurrent(self.targetPosition)

    def setCurrent(self, point):
        self.currentPosition = point

    def getCurrentPos(self):
        print(self.ser.read())


