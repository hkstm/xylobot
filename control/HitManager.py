from control.Hit import *
from .Point import Point
from .Position import Position
from . import IK as ik

import time


class HitManager:

    def __init__(self, ser):
        self.xyloheight = 12.5
        self.ser = ser
        self.currentPosition = Point(1.1, 23, 13)
        self.targetPosition = None
        self.qh = QuadraticHit(ser, self.xyloheight)
        self.rh = RightAngledTriangularHit(ser, self.xyloheight)
        self.th = TriangularHit(ser, self.xyloheight)
        self.uh = UniformHit(ser, self.xyloheight)
        self.gh = Glissando(ser, self.xyloheight)
        self.lh = None
        self.snh = SameNoteHit(ser, self.xyloheight)
        self.positions = []
        self.servospeed = 0.05

    def hit(self):
        for p in self.positions:
            print('- Position: ', p)
            self.sendToArduino(p)
            time.sleep(self.servospeed)

    def calculatePath(self, note, tempo=0, malletBounce=0):
        print('[*] Calculating path...')
        print('[*] Playing note: ', note)
        self.positions = []
        self.targetPosition = note.coords
        distance = math.sqrt((self.currentPosition.x - self.targetPosition.x) ** 2 + note.power ** 2)
        note.speed = distance / (3 + tempo)  # approx cm between keys

        h = None
        print('target: ', self.targetPosition, ' current: ', self.currentPosition, ' distance: ', distance, ' speed: ', note.speed)
        if math.fabs(self.targetPosition.x - self.currentPosition.x) <= 0.5:
            print('Same key is to be hit')
            h = self.snh
            note.speed = distance
            self.servospeed = 0.1
        else:
            self.servospeed = 0.05
            if note.hittype == 'quadratic':
                h = self.qh
            if note.hittype == 'triangle 1':
                h = self.th
            if note.hittype == 'triangle 2':
                h = self.rh
            if note.hittype == 'triangle 3':
                h = self.lh
            if note.hittype == 'uniform':
                h = self.uh
            if note.hittype == 'glissando':
                h = self.gh
                malletBounce = 0

        if note.key is 'c6' or note.key is 'c7':
            h.setHeight(self.xyloheight + 0.5 + malletBounce)
        if note.key is 'd6' or note.key is 'b6':
            h.setHeight(self.xyloheight + 0.3 + malletBounce)
        if note.key is 'e6' or note.key is 'a6':
            h.setHeight(self.xyloheight + 0.1 + malletBounce)

        #self.xyloheight = self.xyloheight + malletBounce
        #h.setHeight(self.xyloheight + malletBounce)
        print('note speed: ', note.speed)
        h.set(self.currentPosition, self.targetPosition, note.speed, note.power)

        h.calculatePath()

        lastPos = None

        # print('Points: ')
        for p in h.getPath():
            print('- Point: ', p)
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

        # self.setCurrent(self.targetPosition)
        if lastPos is None:
            self.setCurrent(self.targetPosition)
        else:
            self.setCurrent(lastPos)


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

