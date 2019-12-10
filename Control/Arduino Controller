# 19 July 2014

# in case any of this upsets Python purists it has been converted from an equivalent JRuby program

# this is designed to work with ... ArduinoPC2.ino ...

# the purpose of this program and the associated Arduino program is to demonstrate a system for sending
#   and receiving data between a PC and an Arduino.

# The key functions are:
#    sendToArduino(str) which sends the given string to the Arduino. The string may
#                       contain characters with any of the values 0 to 255
#
#    recvFromArduino()  which returns an array.
#                         The first element contains the number of bytes that the Arduino said it included in
#                             message. This can be used to check that the full message was received.
#                         The second element contains the message as a string


# the overall process followed by the demo program is as follows
#   open the serial connection to the Arduino - which causes the Arduino to reset
#   wait for a message from the Arduino to give it time to reset
#   loop through a series of test messages
#      send a message and display it on the PC screen
#      wait for a reply and display it on the PC

# to facilitate debugging the Arduino code this program interprets any message from the Arduino
#    with the message length set to 0 as a debug message which is displayed on the PC screen

# the message to be sent to the Arduino starts with < and ends with >
#    the message content comprises a string, an integer and a float
#    the numbers are sent as their ascii equivalents
#    for example <LED1,200,0.2>
#    this means set the flash interval for LED1 to 200 millisecs
#      and move the servo to 20% of its range

# receiving a message from the Arduino involves
#    waiting until the startMarker is detected
#    saving all subsequent bytes until the end marker is detected angle
# NOTES
#       this program does not include any timeouts to deal with delays in communication
#
#       for simplicity the program does NOT search for the comm port - the user must modify the
#         code to include the correct reference.
#         search for the lines
#               serPort = "/dev/ttyS80"
#               baudRate = 9600
#               ser = serial.Serial(serPort, baudRate)
#


# =====================================-1

#  Function Definitions

# =====================================

key0 = [-33, -25, -20, -13, -7, 0, 6, 12]
key1 = [-85, -82, -82, -75, -75, -75, -80, -90]
key2 = [24, 33, 33, 44, 42, 44, 35, 18]

import serial
import time
import xylobot.IK as ik
import xylobot.IK.Point as Point

import numpy as np

# 0 = connected to arduino
# 2 = print statements
DEBUG = 0

print
print
# ser = serial.Serial()
# NOTE the user must ensure that the serial port and baudrate are correct
if DEBUG == 0:
    baudRate = 9600
    serPort = "COM3"
    ser = serial.Serial(serPort, baudRate)
    print("Serial port " + serPort + " opened,  Baudrate " + str(baudRate))
    startMarker = 60
    endMarker = 62

def singlehit (cur, key, speed):
    goalPos = [key1[key], key2[key]]
    mid1 = key1[key]
    mid2 = key2[key] - 50

    oneincrement = (mid1 - cur[1]) / speed/2
    twoincrement = (mid2 - cur[2]) / speed/2


    for i in range(1, speed):

        one = i*oneincrement + cur[1]
        two = i*twoincrement + cur[2]


        string = str(cur[0]) + "," + str(one) + "," + str(two) + "\n"
        sendToArduino(string)

    string = str(cur[0]) + "," + str(goalPos[0]) + "," + str(goalPos[1]) + "\n"
    sendToArduino(string)


def playft(curkey, key, speed):

    hit([key0[curkey], key1[curkey], key2[curkey]], [key0[key], key1[key]+10, key2[key]-50], speed)
    singlehit([key0[key], key1[key]+10, key2[key]-50], key, speed)
    time.sleep(0.2)



def hit(curpos, pos, speed):
    # speed 0-100 indicates the percentage of the maximal speed that is desired
    path = getPath(curpos, pos, speed)
    xpath = path[0]
    ypath = path[1]
    zpath = path[2]
    leng = int(len(xpath))
    if DEBUG == 2:
        print(xpath)
        print(ypath)
        print(zpath)
    for i in range(0, leng):
        x = xpath[i]
        y = ypath[i]
        z = zpath[i]
        if DEBUG == 2:
            print('x' + str(i) + ' = ' + str(x))
            print('y' + str(i) + ' = ' + str(y))
            print('z' + str(i) + ' = ' + str(z))
            print()
        move(x, y, z)
    # Loop through path & sendToArduino(point in path), delay



def move(x, y, z):
    string = str(x) + ', ' + str(z) + ', ' + str(y) + '\n'
    if DEBUG == 0:
        sendToArduino(string)



def getPath(curpos, pos, speed):
    # TO_DO

    x0 = curpos[0]
    x1 = pos[0]
    z0 = curpos[1]
    z1 = pos[1]
    y0 = curpos[2]
    y1 = pos[2]

    xpath = []
    ypath = []
    zpath = []
    path = []
    if x1 > x0:
        zmid = z0 + 0.6 * (x1 - x0)
    else:
        zmid = z0 + 0.6 * -(x1 - x0)

    if x1 - x0 == 0:
        zmid = z0 + 20
        for i in range(0, speed):
            x = x0 + (i + 1) * ((x1 - x0) / speed)
            y = y0 + (i + 1) * ((y1 - y0) / speed)

            if i < speed / 2:
                z = z0 + (i + 1) * (zmid - z0) / speed
            else:
                z = zmid + (i + 1) * (z1 - zmid) / speed
            xpath.append(x)
            ypath.append(y)
            zpath.append(z)
    else:
        a = (y1 - y0) / (x1 - x0)
        b = y0 - a * x0

        if DEBUG == 2:
            print('x0 = ' + str(x0))
            print('x1 = ' + str(x1))
            print('y0 = ' + str(y0))
            print('y1 = ' + str(y1))
            print('z0 = ' + str(z0))
            print('z1 = ' + str(z1))

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
            if DEBUG == 2:
                print(x)
                print(y)
                print(z)
                print()

    path.append(xpath)
    path.append(ypath)
    path.append(zpath)

    return path



def sendToArduino(sendStr):
    print("inside send to Arduino")
    print(sendStr)
    b = sendStr.encode('utf-8')
    ser.write(b)

def send(x, y, z):
    point = ik.getAngles(Point(x, y, z))
    string = str(point[0]) + ', ' + str(point[1]) + ', ' + str(point[2]) + '\n'
    sendToArduino(string)


# ======================================

def recvFromArduino():
    global startMarker, endMarker

    ck = ""
    x = "z"  # any value that is not an end- or startMarker
    byteCount = -1  # to allow for the fact that the last increment will be one too many
    print("in receive from arduino ")
    # wait for the start character
    while ord(x) != startMarker:
        x = ser.read()
    print("in receive from arduino 3")
    # save data until the end marker is found
    while ord(x) != endMarker:
        if ord(x) != startMarker:
            ck = ck + x
            byteCount += 1
        x = ser.read()
    print("in receive from arduino 4")
    return (ck)


# ============================
def hitnote(a, b, speed):
    hit([key0[a], key1[a], key2[a]], [key0[b], key1[b], key2[b]], speed)


def hitsinglenote(a):
    string = str(key0[a]) + ', ' + str(key1[a]) + ', ' + str(key2[a]) + '\n'
    sendToArduino(string)


def waitForArduino():
    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded

    global startMarker, endMarker
    print("inside waiting for arduino")
    msg = ""
    while msg.find("Arduino is ready") == -1:

        while ser.inWaiting() == 0:
            print("<Arduino is ready>")
            pass

        msg = recvFromArduino()

        print(msg)


# ======================================

def runTest(td):
    print("Angles Received by Serial_COM from Call Serial")
    print(td)
    numLoops = len(td)
    waitingForReply = False

    n = 0
    while n < numLoops:

        teststr = td[n]

        if waitingForReply == False:
            sendToArduino(teststr)
            print("Sent from PC -- LOOP NUM " + str(n) + " TEST STR " + teststr)
            waitingForReply = True
            print("sending done")
        if waitingForReply == True:
            print("waitingForReply  = True ")
            while ser.inWaiting() == 0:
                pass
            dataRecvd = recvFromArduino()

            print("Reply Received  " + dataRecvd)
            n += 1
            waitingForReply = False

            print("===========")

        time.sleep(0)



# ======================================

# THE DEMO PROGRAM STARTS HERE



# ======================================


if DEBUG == 0:
    print("//////////////////// Serial Communication started//////////////////////////")
    ser.close  # closes serial port


