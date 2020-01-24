import math
from .SimuVector import SimuVector


class SimuKey:

    WIDTH = 50
    def __init__(self, color, location, rotation, height, WIDTH):
        self.color = color
        self.location = location
        self.rotation = rotation
        self.height = height

        myX = self.location.getX()
        myY = self.location.getY()

        # print('before recalc loc: x: ',myX,'  y: ',myY)
        #Create the vertices
        #Location is seen as the middle of the key
        HALFHEIGHT = height/2
        HALFWIDTH = WIDTH / 2
        self.vertices = [

            [myX - HALFWIDTH, myY + HALFHEIGHT],
            [myX - HALFWIDTH, myY - HALFHEIGHT],
            [myX+HALFWIDTH, myY-HALFHEIGHT],
            [myX + HALFWIDTH, myY + HALFHEIGHT]]

        pointZeroSimuVec = SimuVector(self.vertices[0][0], self.vertices[0][1], 0)
        pointTwoSimuVec = SimuVector(self.vertices[2][0], self.vertices[2][1], 0)
        self.location = self.midpoint(pointZeroSimuVec, pointTwoSimuVec)






    def rotate(self, angle):
        self.rotation += angle
        points = self.vertices
        angle = math.radians(angle)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        new_points = []
        for x_old, y_old in points:
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append([x_new, y_new])

        #old way:
        # for x_old, y_old in points:
        #     x_old -= cx
        #     y_old -= cy
        #     x_new = x_old * cos_val - y_old * sin_val
        #     y_new = x_old * sin_val + y_old * cos_val
        #     new_points.append([x_new + cx, y_new + cy])

        pointZeroSimuVec = SimuVector(new_points[0][0], new_points[0][1], 0)
        pointTwoSimuVec = SimuVector(new_points[2][0], new_points[2][1],0)
        self.location = self.midpoint(pointZeroSimuVec, pointTwoSimuVec)
        #print('Midpoint',self.location.x, ' ', self.location.y)
        self.vertices = new_points
        return new_points

    def getPoints(self):
        return self.vertices

    def getKeyMidpoint(self):
        return self.location

    def midpoint(self, p1, p2):
        return SimuVector((p1.x + p2.x) / 2, (p1.y + p2.y) / 2, p1.z)

    def getColor(self):
        print(self.color)
        return self.color

    def translate(self, x, y):
        self.location.x+=x
        self.location.y+=y

        for i in range(len(self.vertices)):
            for j in range(len(self.vertices[i])):
                if(j ==0):
                    self.vertices[i][j]+=x
                elif(j==1):
                    self.vertices[i][j]+=y
