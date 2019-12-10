import Control as Control
from Point import Point as Point
from Position import Position as Position
import IK as ik
import computervision.Grid as Grid
import math

keyList = []
currentPoint = Point(12.6,25,12)
currentPos = ik.getAngles(currentPoint)
Control.sendToArduino(Position(currentPos[0], currentPos[1], currentPos[2]))
rang = 100




def calibrate():
    height = 11

    keyList = Grid.generateList()
    keyList[0].x = 12.6
    keyList[0].y = 25
    keyList[0].z = height

    keyList[1].x = 9.4
    keyList[1].y = 24
    keyList[1].z = height

    keyList[2].x = 6.4
    keyList[2].y = 23
    keyList[2].z = height

    keyList[3].x = 3.4
    keyList[3].y = 23
    keyList[3].z = height

    keyList[4].x = 0.4
    keyList[4].y = 23
    keyList[4].z = height

    keyList[5].x = -2.4
    keyList[5].y = 23
    keyList[5].z = height

    keyList[6].x = -6.2
    keyList[6].y = 23.8
    keyList[6].z = height

    keyList[7].x = -9.7
    keyList[7].y = 24.5
    keyList[7].z = height

    for k in keyList:
        find(k)

def find(key):
    moveTo(Point(key.x,key.y,key.z))
    offset = Grid.getOffset(key)
    error = 50
    while abs(offset[0]) > error or abs(offset[1] > error):
        print(" Px & y are: ", key.px, " ", key.py)

        print(" Offsets are: ", offset[0], " ", offset[1])
        print(" Keys are at: ", key.x, " ", key.y)
        if abs(offset[0])>error:
            key.x -= offset[0]*0.001
        if abs(offset[1])>error:
            key.y -= offset[1]*0.001
        moveTo(Point(key.x, key.y, key.z))
        offset = Grid.getOffset(key)
    print(" KEYFOUND")

def moveTo(point):
    global currentPoint
    c = ik.getAngles(currentPoint)
    c2 = ik.getAngles(point)
    p = Position(c[0],c[1],c[2])
    g = Position(c2[0],c2[1],c2[2])
    m0dif = g.m0-p.m0
    m1dif = g.m1-p.m1
    m2dif = g.m2-p.m2

    for i in range(0, rang):
        temp = Position(p.m0 + m0dif/rang*i, p.m1 + m1dif/rang*i, p.m2)
        Control.sendToArduino(temp)

    currentPoint = point

calibrate()

