import IK as ik
from controll.Hit import *
from Point import Point
from Position import Position


class HitManager:
    POWER = 5

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
        self.tempo = 0.1

    def hit(self):
        for p in self.positions:
            self.sendToArduino(p)
            # print('tempo: ', self.tempo)
            time.sleep(self.tempo)

    def calculatePath(self, note, speed='', power=''):
        # print('[*] calculating path...')
        self.positions = []
        if power == '':
            power = self.POWER

        self.targetPosition = note.coords
        distance = math.fabs(self.targetPosition.x - self.currentPosition.x)
        speed = distance / 40
        if distance == 0:
            speed = 0.1

        h = None
        #
        # print('target: ', self.targetPosition, ' current: ', self.currentPosition)
        if self.targetPosition.x == self.currentPosition.x:
            print('Same key is to be hit')
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

        lastPos = None

        # print('Points: ')
        for p in h.getPath():
            try:
                p.x = round(p.x, 2)
                p.y = round(p.y, 2)
                p.z = round(p.z, 2)
                pos = ik.getAngles(p)
                # print('pos: ', pos)
                lastPos = p
                self.positions.append(Position(pos[0], pos[1], pos[2]))
                # print(p)
            except Warning as w:
                print(w)
                self.setCurrent(self.currentPosition)
                self.positions = []
                return Warning(w)

            # Readjust the height

        #self.setCurrent(self.targetPosition)
        if lastPos is None:
            self.setCurrent(self.targetPosition)
        else:
            self.setCurrent(lastPos)
        pos = ik.getAngles(Point(self.currentPosition.x, self.currentPosition.y, 13.5))
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

    def setTempo(self, tempo):
        if tempo <= 100:
            self.tempo = tempo / (10 ** 4)
        if tempo <= 75:
            self.tempo = tempo / (10 ** 3.5)
        if tempo <= 50:
            self.tempo = tempo / (10 ** 3)
        if tempo <= 25:
            self.tempo = tempo / (10 ** 2.5)
        if tempo <= 10:
            self.tempo = tempo / (10 ** 2)


