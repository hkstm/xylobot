try:
    from control import Control as Control
except:
    import Control as Control

from .Point import Point as Point
from .Position import Position as Position
# import IK
from . import IK as ik
import computervision.Grid as Grid

import numpy as np
import math
Coefficient = 1

FIRST = True
stepsize = 0.05
error = 5
lastPointV = None



def calibrate(gui, cm):
    global Coefficient, lastPointV, stepsize
    discoveredPoints = []



    #height = Control.getZ()
    height = 12
    hitHeight = 14
    #control.sendToArduino(Position(0,0,0))
    cm.sendToArduino(Position(0,0,0))

    # prrrr = ik.getAngles((Point(14.35, 20.5, 11)))
    # control.sendToArduino(Position(prrrr[0],prrrr[1], prrrr[2]))
    # time.sleep(5)
    keyList = Grid.generateList(gui)
    #gui.updateCenterpointsImage()

    keyList[0].x = 9
    keyList[0].y = 23
    keyList[0].z = height

    keyList[1].x = 9.4
    keyList[1].y = 23
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
    keyList[6].y = 23
    keyList[6].z = height

    keyList[7].x = -7
    keyList[7].y = 23
    keyList[7].z = height




    if (Grid.Swapped()):
        print("Keylist swapped in calibrator, starting right")
        Coefficient = -1
        # keyList2 = keyList

        # for j in range(0, 7):
        #     i = 7-j
        #     keyList2[i] = keyList[j]
        for k in keyList:
            print(k.key, " xyz = ", k.x, " ", k.y, "  ", k.z)
        print("Coefficient: ", Coefficient)

        keyList = np.flip(keyList, 0)
        #keyList = keyList2

        for k in keyList:
            print(k.key, " xyz = ", k.x, " ", k.y, "  ", k.z)
        print("Coefficient: ", Coefficient)



    # control.sendToArduino(Position(currentPos[0], currentPos[1], currentPos[2]))
    #cm.sendToArduino(Position(currentPos[0], currentPos[1], 0))

    currentPoint = Point(0, keyList[0].y, keyList[0].z)
    t = ik.getAngles(currentPoint)
    moveToPos(cm, Position(t[0], t[1], t[2]), Position(0,0,0), 500)

    currentPoint = Point(keyList[0].x, keyList[0].y, keyList[0].z)
    r = ik.getAngles(currentPoint)
    moveToPos(cm, Position(r[0], r[1], r[2]), Position(t[0],t[1],t[2]), 200)




    for k in keyList:
        # stepsize = 0.07
        print("Current Key XYZ = " , k.x , "  " , k.y , "  " , k.z)
        #currentPoint = moveTo(Point(k.x, k.y, k.z + 10), currentPoint)
        newx, newy, newz, currentPoint = find(cm, k, currentPoint)
        #discoveredPoints.append([newx, newy, height])
        discoveredPoints.append(Point(newx, newy, hitHeight))
        i = 0
        print("Key: ", k,"  ", lastPointV.m0, " ", lastPointV.m1," ",lastPointV.m2)
        while i < len(keyList):
            keyList[i].y = newy
            keyList[i].x = newx - (12/6.75 * Coefficient)
            i += 1
    return discoveredPoints

def find(cm, key, currentPoint):
    global Coefficient, error, stepsize
    oldPoint = currentPoint
    currentPoint = moveTo(cm, Point(key.x,key.y,key.z), currentPoint)
    offset = Grid.getOffset(key)
    print("offsets: ", offset[0], offset[1])
    #if offset is (None, None):
        # moveTo(cm, oldPoint, currentPoint)
        # return find(cm, Point(key.x - (12/6.75 * Coefficient), key.y, key.z), oldPoint)
    #else:
    try:
        while abs(offset[0]) > error or abs(offset[1] > error):
            print(key.key," Px & y are: ", key.px, " ", key.py)
            print(" Offsets are: ", offset[0], " ", offset[1])
            print(" Keys are at: ", key.x, " ", key.y)
            if abs(offset[0])>error:
                key.x -= offset[0]*stepsize #* Coefficient
            if abs(offset[1])>error:
                key.y -= offset[1]*stepsize
            if stepsize > 0.02:
                stepsize -= 0.01
            currentPoint = moveTo(cm, Point(key.x, key.y, key.z), currentPoint)
            offset = Grid.getOffset(key, (key.px, key.py))
        print(" KEYFOUND " , key.x, " ", key.y, " ", key.z, " With px, py and malletx, mallety : ", key.px, ", ", key.py, ", ", key.px + offset[0], ", ", key.py + offset[1])
        #gui.update_log(f'KEYFOUND  {key.x}, {key.y}, {key.z} With px, py and malletx, mallety : ", {key.px}, {key.py}, {key.px + offset[0]}, {key.py + offset[1]}')
        return key.x, key.y, key.z, currentPoint
    except Exception as e:
        print(e)
        stepsize = 0.02
        currentPoint = moveTo(cm, Point(key.x - (12/6.75 * Coefficient), key.y - (12/6.75 * Coefficient), key.z), oldPoint)
        return find(cm, key, currentPoint)

def moveTo(cm, point, currentPoint, rang = 100):
    global lastPointV
    #currentPoint.y -= 3
    #currentPoint.x -= 3
    print(" CURRENT POINT EQUALS ", currentPoint.x, currentPoint.y, currentPoint.z)
    print(" POINT EQUALS ", point.x, point.y, point.z)
    c = ik.getAngles(currentPoint)
    c2 = ik.getAngles(point)
    p = Position(c[0],c[1],c[2])
    g = Position(c2[0],c2[1],c2[2])
    m0dif = g.m0-p.m0
    m1dif = g.m1-p.m1
    m2dif = g.m2-p.m2

    for i in range(1, rang):
        temp = Position(p.m0 + m0dif/rang*i, p.m1 + m1dif/rang*i, p.m2 + m2dif/rang*i)
        lastPointV = temp
        #control.sendToArduino(temp)
        cm.sendToArduino(temp)


    currentPoint = point
    return currentPoint

def moveToPos(cm, pos, currentPos, rang = 100):
    #currentPoint.y -= 3
    #currentPoint.x -= 3
    print(" CURRENT POINT EQUALS ", currentPos.m0, currentPos.m1, currentPos.m2)
    print(" POINT EQUALS ", pos.m0, pos.m1, pos.m2)

    p = currentPos
    g = pos
    m0dif = g.m0-p.m0
    m1dif = g.m1-p.m1
    m2dif = g.m2-p.m2

    for i in range(1, rang):
        temp = Position(p.m0 + m0dif/rang*i, p.m1 + m1dif/rang*i, p.m2 + m2dif/rang*i)
        #control.sendToArduino(temp)
        cm.sendToArduino(temp)


    currentPoint = pos
    return currentPoint

def destroyWindows():
    global Coefficient
    Grid.destroyWindows()
    Coefficient = 1
    print("Windows destroyed")

def monitor(gui):
    while(1):
        bcl, bcr = Grid.monitorSides(gui)


if __name__ == '__main__':
    print(calibrate())