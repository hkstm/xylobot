import serial
import time
import Point
import Position
import computervision.Grid as Grid
import IK as ik
import delayexample as delay
from Point import Point
from Position import Position

currentPosition = Position(21,57,-51)
currentPoint = None

baudRate = 9600
serPort = "COM3"
#ser = serial.Serial(serPort, baudRate)
print("Serial port " + serPort + " opened,  Baudrate " + str(baudRate))
startMarker = 60
endMarker = 62

z = 12
#notes = [[18, 25, z], [14, 25, z], [10, 25, z], [7, 24, z+0.022], [4, 23.5, z+0.022], [1, 25, z], [-3, 25, z], [-6, 25, z]]

#notes = [[11.67938232421875, 24.716214752197267, z], [8.070569695366752, 23.445574188232424, z], [4.915512254503036, 23.170574188232425, z], [1.8723734537760397, 23.170574188232425, z], [-1.117361111111113, 23.170574188232425, z], [-4.532638888888891, 23.170574188232425, z], [-7.310416666666669, 23.895574188232427, z], [-11.31440370347765, 25.022781372070316, z]]

#notes = [[10.25, 23, 12], [7.298546685112846, 25.239398193359374, 12], [3.7181376817491305, 24.618950500488282, 12], [1.0128165690104156, 24.058391418457035, 12], [-1.6065462917751745, 23.74452056884766, 12], [-5.050903049045139, 23.642464599609376, 12], [-8.5511225382487, 23.642464599609376, 12], [-12.27368394639757, 24.626063232421878, 12]]]

#notes = [[12.2458740234375, 24.212860107421875, z], [7.9213463677300355, 23.353560638427734, z],
 #        [4.883616807725696, 22.581473541259765, z], [2.3116083780924495, 22.581473541259765, z],
  #       [-1.0233120388454844, 22.581473541259765, z], [-4.359870486789278, 22.581473541259765, z],
   #      [-7.193417612711587, 23.279550170898435, z], [-11.043839051988389, 24.347423553466797, z]]
speed = 20

#   Takes a list of Note objects
def play(list):
    for i in list:
        print('[*] Playing note: ', i)
        delay.sleep(i.delay)
        hitkey(i.key)

#   Takes a string c6, d6, e6, f6, g6, a6, b6, c7
def hitkey(a):

    #   TO-DO, get coord from CV
    #   point = Grid.getKey(a) #for instance where Grid is the class that defines the xy grid at the start.
       print('[*] Hitting ', a)
       if a == "c6":
           point = notes[0]

       if a == "d6":
           point = notes[1]

       if a == "e6":
           point = notes[2]

       if a == "f6":
           point = notes[3]

       if a == "g6":
           point = notes[4]

       if a == "a6":
           point = notes[5]

       if a == "b6":
           point = notes[6]

       if a == "c7":
           point = notes[7]

       p = Point(point[0], point[1], point[2])
       hit(p)


#   Takes a point object and translates it to a position object, which in turn is sent to Arduino.
# def hit(point):
#     x = point.x
#     y = point.y
#     z = point.z
#     pos = ik.getAngles(point)
#     sendToArduino(pos)

def sendToArduino(pos):
    string = str(pos.m0) + ', ' + str(pos.m1) + ', ' + str(pos.m2) + '\n'
    #print("inside send to Arduino")
    #print(string)
    b = string.encode('utf-8')
    #ser.write(b)

def setCurrent(point):
    print('[*] Setting current position to ', point)
    global currentPoint
    currentPoint = point
    global currentPosition
    curPosAngles = ik.getAngles(point)
    currentPosition = Position(curPosAngles[0], curPosAngles[1], curPosAngles[2])
    print('[*] Setting angles for new current position ', currentPosition)


#   I'm not sure what ser.read returns, I guess a string
#   TO-DO
def getCurrentPos():
    s = ser.read()
    print(s)
    #   currentPosition = s
    #   currentPoint = ik.getCoordinates(currentPosition)


#   BEWARE  # From hereon out x,y,z might represent motor angles 0,1,2. This will be cleaned up at a later stage
#   A point is simply translated to a position and the phase one method takes over
def hit(point):
    # speed 0-100 indicates the percentage of the maximal speed that is desired
    path = getPath(point, 20)
    xpath = path[0]
    ypath = path[1]
    zpath = path[2]
    leng = int(len(xpath))

    for i in range(0, leng):

        x = xpath[i]
        y = ypath[i]
        z = zpath[i]
        position = Position(x, y, z)
        sendToArduino(position)

    # Loop through path & sendToArduino(point in path), delay
    # update current position / point
    setCurrent(point)



def getPath(point, speed):
    # TO_DO
    print('[*] Getting path to ', point)


    #curPosAngles = ik.getAngles(currentPosition)
    #curpos = Position(curPosAngles[0], curPosAngles[1], curPosAngles[2])
    curpos = currentPosition
    print('[*] Getting angles for current position ', curpos)
    #curpos = ik.getAngles(currentPosition)
    posAngles = ik.getAngles(point)
    pos = Position(posAngles[0], posAngles[1], posAngles[2])
    print('[*] Getting angles for target position ', pos)

    #pos = ik.getAngles(point)



    x0 = curpos.m0
    x1 = pos.m0
    y0 = curpos.m1
    y1 = pos.m1
    z0 = curpos.m2
    z1 = pos.m2

    xpath = []
    ypath = []
    zpath = []
    path = []

    zmid = z0 - 50
    ymid = y0 + 20

    if x1 - x0 == 0:
        zmid = z0 + 20
        for i in range(0, speed):
            x = x0 + (i + 1) * ((x1 - x0) / speed)

            if i < speed / 2:
                y = y0 + (i + 1) * ((ymid - y0) / speed)
                z = z0 + (i + 1) * (zmid - z0) / speed
            else:
                y = y0 + (i + 1) * ((y1 - ymid) / speed)
                z = zmid + (i + 1) * (z1 - zmid) / speed
            xpath.append(x)
            ypath.append(y)
            zpath.append(z)
    else:
        a = (y1 - y0) / (x1 - x0)
        b = y0 - a * x0

        for i in range(0, speed):
            x = x0 + (i + 1) * ((x1 - x0) / speed)
            y = a * x + b
            xpath.append(x)
            ypath.append(y)

            if i < speed / 2:
                z = z0 + (i + 1) * (zmid - z0) / speed
            else:
                z = zmid + (i + 1) * (z1 - zmid) / speed
            zpath.append(z)

    path.append(xpath)
    path.append(ypath)
    path.append(zpath)

    return path

def getZ():
    global z
    return z


def setNotes(newNotes):
    global notes
    notes = newNotes

