import time

from Point import Point
from Position import Position
import math
import IK as ik

ACCURACY_COEFF = 100

class Hit:
    def __init__(self, ser, xyloheight):
        self.ser = ser
        self.hit_height = xyloheight
        self.prehit_height = 0
        self.origin = None
        self.target = None
        self.midpoint = None
        self.speed = 0
        self.power = 0
        self.offset_target = None
        self.offset_midpoint = None
        self.offset_origin = None
        self.path = []
        self.x = 0
        self.z = 0
        self.left = True

    def set(self, origin, target, speed, power):
        self.path = []
        self.prehit_height = self.hit_height + power
        self.origin = origin
        self.target = target
        self.speed = speed

        if self.origin.x < self.target.x:
            self.midpoint = Point(self.origin.x + (math.fabs(self.target.x - self.origin.x) / 2), 0, self.prehit_height)
            self.left = True
        elif self.origin.x > self.target.x:
            self.midpoint = Point(self.origin.x - (math.fabs(self.target.x - self.origin.x) / 2), 0, self.prehit_height)
            self.left = False

        print('Current position: ', self.origin, ' target: ', self.target, ' midpoint: ', self.midpoint, ' speed: ',
              self.speed, ' power: ', self.power)

    def getPath(self):
        return self.path

class SameNoteHit(Hit):
    def __init__(self, ser, xyloheight):
        super().__init__(ser, xyloheight)
        self.z = 0

    def calculatePath(self):
        i = 0
        while self.z <= self.prehit_height:
            i = i + self.speed + (i / ACCURACY_COEFF)
            self.z = self.origin.z + i
            self.path.append(Point(self.origin.x, self.origin.y, self.z))

        i = 0
        while self.z >= self.hit_height:
            i = i + self.speed + (i / ACCURACY_COEFF)
            self.z = self.prehit_height - i
            self.path.append(Point(self.origin.x, self.origin.y, self.z))


class RightAngledTriangularHit(Hit):

    def __init__(self, ser, xyloheight):
        super().__init__(ser, xyloheight)
        self.slope = 0
        self.b = 0

    def getFunction(self):
        self.slope = (self.midpoint.z - self.target.z) / math.fabs(self.target.x - self.origin.x)
        self.b = self.midpoint.z - self.slope * self.origin.x
        print('slope: ', self.slope, ' b: ', self.b)

    def calculatePath(self):
        self.getFunction()
        if self.left:
            i = 0
            while self.x < self.target.x:
                i = i + self.speed + (i / ACCURACY_COEFF)
                self.x = self.origin.x + i
                self.z = self.slope * self.x + self.b
                self.path.append(Point(self.x, self.origin.y, self.z-5))

            j = 0
            while self.z > self.target.z:
                j = j + self.speed + (j / ACCURACY_COEFF)
                self.z = self.target.z - j
                self.path.append(Point(self.target.x, self.target.y, self.z))
        else:
            i = 0
            while self.x > self.target.x:
                i = i + self.speed + (i / ACCURACY_COEFF)
                self.x = self.origin.x - i
                self.z = self.slope * (self.target.x + i) + self.b
                self.path.append(Point(self.x, self.origin.y, self.z))

            j = 0
            while self.z > self.target.z:
                j = j + self.speed + (j / ACCURACY_COEFF)
                self.z = self.midpoint.z - j
                self.path.append(Point(self.target.x, self.target.y, self.z))


class TriangularHit(Hit):
    def __init__(self, ser, xyloheight):
        super().__init__(ser, xyloheight)
        self.slope = 0
        self.b = 0

    def getFunction(self, up):
        if up:
            self.slope = (self.midpoint.z - self.origin.z) / (math.fabs(self.midpoint.x - self.origin.x))
        else:
            self.slope = -1 * (self.midpoint.z - self.origin.z) / (math.fabs(self.midpoint.x - self.origin.x))
        self.b = self.midpoint.z - self.slope * self.midpoint.x

    def calculatePath(self):
        self.getFunction(True)
        if self.left:
            i = 0
            while self.x < self.midpoint.x:
                i = i + self.speed + (i / ACCURACY_COEFF)
                self.x = self.origin.x + i
                self.z = self.slope * self.x + self.b
                self.path.append(Point(self.x, self.origin.y, self.z))

            self.getFunction(False)
            j = 0
            while self.x < self.target.x:
                j = j + self.speed + (j / ACCURACY_COEFF)
                self.x = self.midpoint.x + j
                self.z = self.slope * self.x + self.b
                self.path.append(Point(self.x, self.origin.y, self.z))
        else:
            i = 0
            while self.x > self.midpoint.x:
                i = i + self.speed + (i / ACCURACY_COEFF)
                self.x = self.origin.x - i
                self.z = self.slope * (self.target.x + i) + self.b
                self.path.append(Point(self.x, self.origin.y, self.z))

            self.getFunction(False)
            j = 0
            while self.x > self.target.x:
                j = j + self.speed + (j / ACCURACY_COEFF)
                self.x = self.midpoint.x - j
                self.z = self.slope * (self.midpoint.x + j) + self.b
                self.path.append(Point(self.x, self.origin.y, self.z))


class UniformHit(Hit):
    def __init__(self, ser, xyloheight):
        super().__init__(ser, xyloheight)

    def calculatePath(self):
        if self.left:
            i = 0
            while self.z < self.midpoint.z - 1:
                i = i + self.speed + (i / ACCURACY_COEFF)
                self.z = self.origin.z + i
                self.path.append(Point(self.origin.x, self.origin.y, self.z))

            j = 0
            while self.x < self.target.x - 1:
                j = j + self.speed + (j / ACCURACY_COEFF)
                self.x = self.origin.x + j
                self.path.append(Point(self.x, self.origin.y, self.midpoint.z))

            k = 0
            while self.z > self.target.z + 1:
                k = k + self.speed + (k / ACCURACY_COEFF)
                self.z = self.midpoint.z - k
                self.path.append(Point(self.target.x, self.origin.y, self.z))
        else:
            i = 0
            while self.z < self.midpoint.z - 1:
                i = i + self.speed + (i / ACCURACY_COEFF)
                self.z = self.origin.z + i
                self.path.append(Point(self.origin.x, self.origin.y, self.z))

            j = 0
            while self.x > self.target.x + 1:
                j = j + self.speed + (j / ACCURACY_COEFF)
                self.x = self.origin.x - j
                self.path.append(Point(self.x, self.origin.y, self.midpoint.z))

            k = 0
            while self.z > self.target.z + 1:
                k = k + self.speed + (k / ACCURACY_COEFF)
                self.z = self.midpoint.z - k
                self.path.append(Point(self.target.x, self.origin.y, self.z))


class QuadraticHit(Hit):
    def __init__(self, ser, xyloheight):
        super().__init__(ser, xyloheight)
        self.a = 0
        self.b = 0
        self.c = 0
        self.ratio = 0

    def calculatePath(self):
        self.getFunction()
        if self.left:
            i = 0
            while self.x < self.offset_target.x:
                i = i + self.speed + (i / ACCURACY_COEFF)
                self.x = self.offset_origin.x + i
                self.z = self.x ** 2 * self.a + self.x * self.b + self.c
                self.path.append(Point(self.origin.x + self.x, self.origin.y, self.z))
        else:
            i = 0
            while self.x > self.offset_target.x:
                i = i + self.speed + (i / ACCURACY_COEFF)
                self.x = self.offset_origin.x - i
                self.z = self.x ** 2 * self.a + self.x * self.b + self.c
                self.path.append(Point(self.origin.x + self.x, self.origin.y, self.z))


    def getFunction(self):
        self.generateOffset()
        self.ratio = self.offset_target.x / self.offset_midpoint.x
        self.c = self.offset_origin.z
        self.a = (0 - ((self.offset_midpoint.z - self.c) * self.ratio)) / \
                 (self.offset_target.x ** 2 - ((self.offset_midpoint.x ** 2) * self.ratio))
        self.b = ((self.offset_midpoint.z - self.offset_origin.z) - (self.offset_midpoint.x ** 2 * self.a)) / \
                 self.offset_midpoint.x
        print('Quadratic parameters - a: ', self.a, ' b: ', self.b, ' c: ', self.c)

    def generateOffset(self):
        self.offset_target = Point(self.target.x - self.origin.x, 0, self.target.z)
        self.offset_midpoint = Point(self.midpoint.x - self.origin.x, 0, self.midpoint.z)
        self.offset_origin = Point(0, 0, self.target.z)
        print('Offset - origin: ', self.offset_origin, ' midpoint: ', self.offset_midpoint, ' target: ', self.offset_target)



