import IK as ik
from controll.Hit import *
from Point import Point
from Position import Position


class HitManager:
    SPEED = 0.4
    POWER = 3
    DT = 0.01

    def __init__(self, ser, xyloheight):
        self.ser = ser
        self.currentPosition = Point(0, 23, 13)
        self.targetPosition = None
        self.qh = QuadraticHit(ser, xyloheight)
        self.rh = RightAngledTriangularHit(ser, xyloheight)
        self.th = TriangularHit(ser, xyloheight)
        self.uh = UniformHit(ser, xyloheight)
        self.lh = None
        self.snh = SameNoteHit(ser, xyloheight)
        self.positions = []
        self.hittype = 'quadratic'

    def hit(self):
        for p in self.positions:
            time.sleep(self.DT)
            self.sendToArduino(p)

    def calculatePath(self, note, speed='', power=''):
        self.positions = []
        if speed == '':
            speed = self.SPEED
        if power == '':
            power = self.POWER

        self.targetPosition = note.coords
        distance = math.fabs(self.targetPosition.x - self.currentPosition.x)
        speed = distance / 100
        if distance == 0:
            speed = 0.5

        h = None

        print(self.targetPosition, self.currentPosition)
        if self.targetPosition.x == self.currentPosition.x:
            print('kek?')
            h = self.snh
        else:
            if self.hittype == 'quadratic':
                h = self.qh
            if self.hittype == 'triangle 1':
                h = self.th
            if self.hittype == 'triangle 2':
                h = self.rh
            if self.hittype == 'triangle 3':
                h = self.lh
            if self.hittype == 'uniform':
                h = self.uh

        h.set(self.currentPosition, self.targetPosition, speed, power)
        h.calculatePath()

        print('Points: ')
        for p in h.getPath():
            try:
                p.x = round(p.x, 2)
                p.y = round(p.y, 2)
                p.z = round(p.z, 2)
                pos = ik.getAngles(p)
                self.positions.append(Position(pos[0], pos[1], pos[2]))
                print(p)
            except Warning as w:
                self.setCurrent(self.currentPosition)
                self.positions = []
                return Warning(w)
            self.setCurrent(self.targetPosition)
            # Readjust the height
            pos = ik.getAngles(Point(self.currentPosition.x, self.currentPosition.y, self.currentPosition.z + 1))
            self.positions.append(Position(pos[0], pos[1], pos[2]))

    def sendToArduino(self, pos):
        string = str(pos.m0) + ', ' + str(pos.m1) + ', ' + str(pos.m2) + '\n'
        b = string.encode('utf-8')
        self.ser.write(b)

    def setCurrent(self, point):
        self.currentPosition = point

    def getCurrentPos(self):
        print(self.ser.read())

    def getArduinoPositions(self):
        return self.positions

    def standTall(self):
        self.sendToArduino(Position(0, 0, 0))

    def setHitType(self, hittype):
        self.hittype = hittype


