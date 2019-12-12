import IK as ik
from controll.Hit import *
from Point import Point
from Position import Position


class HitManager:
    SPEED = 0.4
    POWER = 5

    def __init__(self, ser, xyloheight):
        self.ser = ser
        self.currentPosition = Point(0, 23, 12)
        self.targetPosition = None
        self.qh = QuadraticHit(ser, xyloheight)
        self.rh = RightAngledTriangularHit(ser, xyloheight)
        self.th = TriangularHit(ser, xyloheight)
        self.uh = UniformHit(ser, xyloheight)
        self.lh = None
        self.snh = SameNoteHit(ser, xyloheight)

    def sendToArduino(self, pos):
        string = str(pos.m0) + ', ' + str(pos.m1) + ', ' + str(pos.m2) + '\n'
        b = string.encode('utf-8')
        self.ser.write(b)

    def hit(self, note, hittype, speed='', power=''):
        if speed == '':
            speed = self.SPEED
        if power == '':
            power = self.POWER

        self.targetPosition = note.coords
        distance = math.fabs(self.targetPosition.x - self.currentPosition.x)
        speed = distance / 30
        if distance == 0:
            speed = 0.5

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

        anglepath = []

        for i in path:
            pos = ik.getAngles(i)
            #anglepath.append(Position(pos[0], pos[1], pos[2]))
            time.sleep(0.01)
            self.sendToArduino(Position(pos[0], pos[1], pos[2]))

        #for p in anglepath:
        #    self.sendToArduino(p)

        self.setCurrent(self.targetPosition)
        #time.sleep(note.delay)

    def setCurrent(self, point):
        self.currentPosition = point

    def getCurrentPos(self):
        print(self.ser.read())


