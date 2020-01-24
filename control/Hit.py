from .Point import Point
import math

SPEED_COEFF = 0

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
        self.errormargin = 0.5

    def set(self, origin, target, speed, power):
        self.path = []
        self.prehit_height = self.hit_height + power
        self.origin = origin
        self.target = target
        self.speed = speed
        self.power = power

        if self.origin.x < self.target.x:
            self.midpoint = Point(self.origin.x + (math.fabs(self.target.x - self.origin.x) / 2), 0, self.prehit_height)
            self.left = True
        elif self.origin.x > self.target.x:
            self.midpoint = Point(self.origin.x - (math.fabs(self.target.x - self.origin.x) / 2), 0, self.prehit_height)
            self.left = False

        #print('Current position: ', self.origin, ' target: ', self.target, ' midpoint: ', self.midpoint, ' speed: ',
        #       self.speed, ' power: ', self.power)

    def setHeight(self, height):
        self.hit_height = height
        #print('Setting height to: ', self.hit_height)


    def getPath(self):
        return self.path

class SameNoteHit(Hit):
    def __init__(self, ser, xyloheight):
        super().__init__(ser, xyloheight)
        self.z = 0

    def calculatePath(self):
        i = 0
        while self.z <= self.prehit_height:
            i = i + self.speed
            self.z = self.hit_height + i
            print('------', self.z, ' ', self.prehit_height)
            if math.fabs(self.z - self.prehit_height) < 0.5:
                self.path.append(Point(self.origin.x, self.origin.y, self.z))
        self.path.append(Point(self.origin.x, self.origin.y, self.hit_height))
        self.z = 0


class RightAngledTriangularHit(Hit):

    def __init__(self, ser, xyloheight):
        super().__init__(ser, xyloheight)
        self.slope = 0
        self.b = 0

    def getFunction(self):
        self.slope = (self.prehit_height - self.hit_height) / math.fabs(self.target.x - self.origin.x)
        self.b = self.prehit_height - self.slope * self.target.x

    def calculatePath(self):
        #print('[*] Right angled triangle hit')
        self.getFunction()
        if self.left:
            #print('Going left')
            #print('x: ', self.origin.x, ' target x: ', self.target.x, ' z: ', self.z, ' slope: ', self.slope, ' b: ', self.b)
            i = 0
            while self.x < self.target.x:
                i = i + self.speed
                self.x = self.origin.x + i
                self.z = self.slope * self.x + self.b
                #print('x: ', self.x, ' target x: ', self.target.x, ' z: ', self.z, ' hit height: ', self.hit_height, ' prehit: ', self.prehit_height)
                if self.z >= self.hit_height:
                    self.path.append(Point(self.x, self.origin.y, self.z))
                if self.x > self.target.x:
                    if len(self.path) > 0:
                        self.path.pop()
                    self.path.append(Point(self.target.x, self.target.y, self.z))
        else:
            #print('Going right')
            #print('x: ', self.origin.x, ' target x: ', self.target.x, ' z: ', self.z, ' slope: ', self.slope, ' b: ', self.b)
            self.b = self.prehit_height - self.slope * self.origin.x
            i = 0
            while self.x > self.target.x:
                i = i + self.speed
                self.x = self.origin.x - i
                self.z = self.slope * (self.target.x + i) + self.b
                if self.z >= self.hit_height:
                    self.path.append(Point(self.x, self.origin.y, self.z))
                if self.x < self.target.x:
                    if len(self.path) > 0:
                        self.path.pop()
                    self.path.append(Point(self.target.x, self.target.y, self.z))

        self.path.append(Point(self.target.x, self.target.y, self.hit_height))


class TriangularHit(Hit):
    def __init__(self, ser, xyloheight):
        super().__init__(ser, xyloheight)
        self.slope = 0
        self.b = 0

    def getFunction(self):
        self.slope = (self.midpoint.z - self.origin.z) / (math.fabs(self.midpoint.x - self.origin.x))
        self.b = self.midpoint.z - self.slope * self.midpoint.x

    def calculatePath(self):
        self.getFunction()
        if self.left:
            i = 0
            #print('Going left')
            #print('x: ', self.origin.x, ' target x: ', self.target.x, ' z: ', self.z, ' slope: ', self.slope, ' b: ', self.b)
            while self.x < self.midpoint.x:
                i = i + self.speed
                self.x = self.origin.x + i
                self.z = self.slope * self.x + self.b
                #print('x: ', self.x, ' target x: ', self.target.x, ' z: ', self.z, ' hit height: ', self.hit_height, ' prehit: ', self.prehit_height)
                if self.x < self.midpoint.x:
                    self.path.append(Point(self.x, self.origin.y, self.z))
                else:
                    self.path.append(Point(self.midpoint.x, self.target.y, self.prehit_height))
        else:
            #print('Going right')
            #print('x: ', self.origin.x, ' target x: ', self.target.x, ' z: ', self.z, ' slope: ', self.slope, ' b: ', self.b)
            i = 0
            while self.x > self.midpoint.x:
                i = i + self.speed
                self.x = self.origin.x - i
                self.z = self.slope * (self.target.x + i) + self.b
                if self.x > self.midpoint.x:
                    self.path.append(Point(self.x, self.origin.y, self.z))
                else:
                    self.path.append(Point(self.midpoint.x, self.target.y, self.prehit_height))

        self.path.append(Point(self.target.x, self.target.y, self.hit_height))


class UniformHit(Hit):
    def __init__(self, ser, xyloheight):
        super().__init__(ser, xyloheight)

    def calculatePath(self):
        self.path.append(Point(self.origin.x, self.target.y, self.prehit_height))
        if self.left:
            j = 0
            while self.x < self.target.x:
                j = j + self.speed
                self.x = self.origin.x + j
                if self.x < self.target.x:
                    self.path.append(Point(self.x, self.target.y, self.prehit_height))
                else:
                    self.path.append(Point(self.target.x, self.target.y, self.prehit_height))
        else:
            j = 0
            while self.x > self.target.x:
                j = j + self.speed
                self.x = self.origin.x - j
                if self.x > self.target.x:
                    self.path.append(Point(self.x, self.target.y, self.prehit_height))
                else:
                    self.path.append(Point(self.target.x, self.target.y, self.prehit_height))
        self.path.append(Point(self.target.x, self.target.y, self.hit_height))

class Glissando(Hit):
    def __init(self, ser, xyloheight):
        super().__init__(ser, xyloheight)

    def calculatePath(self):
        self.path.append(Point(self.origin.x, self.origin.y, self.hit_height))
        self.path.append(Point(self.target.x, self.target.y, self.hit_height))


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
                i = i + self.speed
                self.x = self.offset_origin.x + i
                self.z = self.x ** 2 * self.a + self.x * self.b + self.c
                print('x: ', self.x, ' target x: ', self.target.x, ' z: ', self.z, ' slope: ',
                      ' b: ', self.b)
                if self.z >= self.hit_height:
                    self.path.append(Point(self.origin.x + self.x, self.target.y, self.z))
        else:
            i = 0
            while self.x > self.offset_target.x:
                i = i + self.speed
                self.x = self.offset_origin.x - i
                print('x: ', self.x, ' target x: ', self.target.x, ' z: ', self.z, ' slope: ',
                      ' b: ', self.b)
                self.z = self.x ** 2 * self.a + self.x * self.b + self.c
                if self.z >= self.hit_height:
                    self.path.append(Point(self.origin.x + self.x, self.target.y, self.z))


    def getFunction(self):
        self.generateOffset()
        self.ratio = self.offset_target.x / self.offset_midpoint.x
        self.c = self.offset_origin.z
        self.a = (0 - ((self.offset_midpoint.z - self.c) * self.ratio)) / \
                 (self.offset_target.x ** 2 - ((self.offset_midpoint.x ** 2) * self.ratio))
        self.b = ((self.offset_midpoint.z - self.offset_origin.z) - (self.offset_midpoint.x ** 2 * self.a)) / \
                 self.offset_midpoint.x
        #print('Quadratic parameters - a: ', self.a, ' b: ', self.b, ' c: ', self.c)

    def generateOffset(self):
        self.offset_target = Point(self.target.x - self.origin.x, 0, self.target.z)
        self.offset_midpoint = Point(self.midpoint.x - self.origin.x, 0, self.midpoint.z)
        self.offset_origin = Point(0, 0, self.target.z)
        # print('Offset - origin: ', self.offset_origin, ' midpoint: ', self.offset_midpoint, ' target: ', self.offset_target)


