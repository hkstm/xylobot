import time

import Control as Control
from Point import Point as Point
from Position import Position as Position
import IK as ik
import computervision.Grid as Grid
import math

keyList = []
currentPoint = Point(12.6, 25, 12)
rang = 100
discoveredPoints = []


def calibrate():
    global keyList, currentPoint, rang, discoveredPoints

    currentPoint = Point(12.6, 25, 12)
    currentPos = ik.getAngles(currentPoint)
    Control.sendToArduino(Position(currentPos[0], currentPos[1], currentPos[2]))

    height = 10
    Control.sendToArduino(Position(0,0,0))
    # prrrr = ik.getAngles((Point(14.35, 20.5, 11)))
    # Control.sendToArduino(Position(prrrr[0],prrrr[1], prrrr[2]))
    # time.sleep(5)
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
        moveTo(Point(k.x, k.y, k.z + 10))
        newx, newy, newz = find(k)
        discoveredPoints.append([newx, newy, Control.getZ()])
        i = 0
        while i < len(keyList):
            keyList[i].y = newy
            keyList[i].x = newx - 12/6.75
            i += 1
    return discoveredPoints

def find(key):
    moveTo(Point(key.x,key.y,key.z))
    offset = Grid.getOffset(key)
    error = 5
    stepsize = 0.05
    while abs(offset[0]) > error or abs(offset[1] > error):
        print(key.key," Px & y are: ", key.px, " ", key.py)
        print(" Offsets are: ", offset[0], " ", offset[1])
        print(" Keys are at: ", key.x, " ", key.y)
        if abs(offset[0])>error:
            key.x -= offset[0]*stepsize
        if abs(offset[1])>error:
            key.y -= offset[1]*stepsize
        moveTo(Point(key.x, key.y, key.z))
        offset = Grid.getOffset(key, (key.px, key.py))
    print(" KEYFOUND " , key.x, " ", key.y, " ", key.z, " With px, py and malletx, mallety : ", key.px, ", ", key.py, ", ", key.px + offset[0], ", ", key.py + offset[1])
    return key.x, key.y, key.z

def moveTo(point):
    global currentPoint
    print(" CURRENT POINT EQUALS ", currentPoint)
    c = ik.getAngles(currentPoint)
    c2 = ik.getAngles(point)
    p = Position(c[0],c[1],c[2])
    g = Position(c2[0],c2[1],c2[2])
    m0dif = g.m0-p.m0
    m1dif = g.m1-p.m1
    m2dif = g.m2-p.m2

    for i in range(1, rang):
        temp = Position(p.m0 + m0dif/rang*i, p.m1 + m1dif/rang*i, p.m2 + m2dif/rang*i)
        Control.sendToArduino(temp)

    currentPoint = point

if __name__ == '__main__':
    print(calibrate())
