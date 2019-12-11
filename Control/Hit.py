from xylobot.Control.HitManager import Point
import math


class Hit:

    PREHIT_HEIGHT = 15
    HIT_HEIGHT = 12

    def __init__(self, origin='', target='', speed=''):
        self.origin = origin
        self.target = target
        self.speed = speed
        self.midpoint = Point(origin.x + (math.fabs(target.x - origin.x) / 2), 0, self.PREHIT_HEIGHT)
        self.offset_target = None
        self.offset_midpoint = None
        self.offset_origin = None
        self.offset()
        print(self.origin, ' ', self.midpoint, ' ', self.target)
        self.path = []
        self.x = 0
        self.z = 0

    def offset(self):
        self.offset_target = Point(self.target.x - self.origin.x, 0, self.target.z)
        self.offset_midpoint = Point(self.midpoint.x - self.origin.x, 0, self.midpoint.z)
        self.offset_origin = Point(0, 0, self.target.z)

    def set(self, origin, target, speed):
        self.origin = origin
        self.target = target
        self.speed = speed


class RightAngledTriangularHit(Hit):

    def __init__(self, o='', t='', s=''):
        super().__init__(o, t, s)
        self.slope = 0
        self.b = 0

    def getFunction(self):
        self.slope = (self.PREHIT_HEIGHT - self.target.z) / (self.target.x - self.origin.x)
        self.b = self.origin.z - self.slope * self.origin.x

    def generatePoints(self):
        self.getFunction()
        i = 0
        while self.x <= self.target.x:
            i = i + 1 / self.speed
            self.x = self.origin.x + i
            self.z = self.slope * self.x + self.b
            self.path.append(Point(self.x, self.origin.y, self.z))

        j = 0
        while self.z >= self.target.z:
            j = j + 1 / self.speed
            self.z = self.PREHIT_HEIGHT - j
            self.path.append(Point(self.target.x, self.target.y, self.z))

    def getPath(self):
        self.generatePoints()
        return self.path


class TriangularHit(Hit):

    def __init__(self, o='', t='', s=''):
        super().__init__(o, t, s)
        self.slope = 0
        self.b = 0

    def getFunction(self):
        self.slope = (self.midpoint.z - self.origin.z) / (self.midpoint.x - self.origin.x)
        self.b = self.origin.z - self.slope * self.origin.x
        print('slope: ', self.slope, ' b: ', self.b)

    def generatePoints(self):
        self.getFunction()
        i = 0
        while self.x <= self.midpoint.x:
            i = i + 1 / self.speed
            self.x = self.origin.x + i
            self.z = self.slope * self.x + self.b
            self.path.append(Point(self.x, self.origin.y, self.z))

        j = 0
        self.b = self.target.z + self.slope * self.target.x
        while self.x <= self.target.x:
            j = j + 1 / self.speed
            self.x = self.midpoint.x + j
            self.z = -1 * self.slope * self.x + self.b
            self.path.append(Point(self.x, self.origin.y, self.z))

    def getPath(self):
        self.generatePoints()
        return self.path



class UniformHit(Hit):

    def __init__(self, o='', t='', s=''):
        super().__init__(o, t, s)

    def generatePoints(self):
        i = 0
        while self.z <= self.midpoint.z:
            i = i + 1 / self.speed
            self.z = self.origin.z + i
            self.path.append(Point(self.origin.x, self.origin.y, self.z))

        j = 0
        while self.x <= self.target.x:
            j = j + 1 / self.speed
            self.x = self.origin.x + j
            self.path.append(Point(self.x, self.origin.y, self.midpoint.z))

        k = 0
        while self.z >= self.target.z:
            k = k + 1 / self.speed
            self.z = self.midpoint.z - k
            self.path.append(Point(self.target.x, self.origin.y, self.z))

    def getPath(self):
        self.generatePoints()
        return self.path


class QuadraticHit(Hit):

    def __init__(self, o='', t='', s=''):
        super().__init__(o, t, s)
        self.a = 0
        self.b = 0
        self.c = 0
        self.ratio = 0

    def getFunction(self):
        self.getRatio()
        print(self.offset_origin, ' ', self.offset_midpoint, ' ', self.offset_target)
        self.c = self.offset_origin.z
        self.a = (0 - ((self.offset_midpoint.z - self.c) * self.ratio)) / \
                 (self.offset_target.x ** 2 - ((self.offset_midpoint.x ** 2) * self.ratio))
        self.b = ((self.offset_midpoint.z - self.offset_origin.z) - (self.offset_midpoint.x ** 2 * self.a)) / \
                 self.offset_midpoint.x
        print('a: ', self.a, ' b: ', self.b, ' c: ', self.c)

    def getRatio(self):
        self.ratio = self.offset_target.x * (1 / self.offset_midpoint.x)
        print('ratio: ', self.ratio)

    def generatePoints(self):
        self.getFunction()
        i = 0
        while self.x <= self.offset_target.x:
            i = i + 1 / self.speed
            self.x = self.offset_origin.x + i
            self.z = self.x ** 2 * self.a + self.x * self.b + self.c
            self.path.append(Point(self.origin.x + self.x, self.origin.y, self.z))

    def getPath(self):
        self.generatePoints()
        return self.path


qh = QuadraticHit(Point(10, 25, 12), Point(18, 25, 12), 50)
uh = UniformHit(Point(10, 25, 12), Point(18, 25, 12), 50)
th = TriangularHit(Point(10, 25, 12), Point(18, 25, 12), 50)
rh = RightAngledTriangularHit(Point(10, 25, 12), Point(18, 25, 12), 50)
#path = qh.getPath()
#path = uh.getPath()
#path = th.getPath()
path = rh.getPath()
for i in path:
    print(i)




