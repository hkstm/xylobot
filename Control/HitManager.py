import xylobot.IK as ik
from xylobot.Control.Hit import *
from xylobot.Point import Point
from xylobot.Position import Position


class HitManager:
    SPEED = 2
    POWER = 4

    def __init__(self, ser, xyloheight):
        self.ser = ser
        self.currentPosition = Point(0, 25, 12)
        self.targetPosition = None
        self.qh = QuadraticHit(ser, xyloheight)
        self.rh = RightAngledTriangularHit(ser, xyloheight)
        self.th = TriangularHit(ser, xyloheight)
        self.uh = UniformHit(ser, xyloheight)
        self.lh = None
        self.snh = SameNoteHit(ser, xyloheight)

    def hit(self, note, hittype, speed='', power=''):
        if speed == '':
            speed = self.SPEED
        if power == '':
            power = self.POWER

        self.targetPosition = note.coords

        if self.targetPosition.x == self.currentPosition.x:
            self.snh.set(self.currentPosition, self.targetPosition, speed, power)
            path = self.snh.getPath()
        else:
            if hittype == 'quadratic':
                self.qh.set(self.currentPosition, self.targetPosition, speed, power)
                path = self.qh.getPath()
            if hittype == 'triangle 1':
                self.th.set(self.currentPosition, self.targetPosition, speed, power)
                path = self.th.getPath()
            if hittype == 'triangle 2':
                self.rh.set(self.currentPosition, self.targetPosition, speed, power)
                path = self.rh.getPath()
            if hittype == 'triangle 3':
                self.lh.set(self.currentPosition, self.targetPosition, speed, power)
                path = self.lh.getPath()
            if hittype == 'uniform':
                self.uh.set(self.currentPosition, self.targetPosition, speed, power)
                path = self.uh.getPath()

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


