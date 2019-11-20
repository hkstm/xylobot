
#Minimum and maximal angles of each joint, still to be defined
minAngle1 = 20
maxAngle1 = 60
minAngle2 = 20
maxAngle2 = 60
minAngle3 = 20
maxAngle3 = 60



def tryToSendToArduino(coordinates):
    import serial

    if(coordinates[0]<minAngle1):
        raise Exception('The value for the first angle was too small, it was:{}'.format(coordinates[0]))
    elif(coordinates[0]>maxAngle1):
        raise Exception('The value for the first angle was too big, it was:{}'.format(coordinates[0]))
    if (coordinates[1] < minAngle2):
        raise Exception('The value for the second angle was too small, it was:{}'.format(coordinates[1]))
    elif (coordinates[1] > maxAngle2):
        raise Exception('The value for the second angle was too big, it was:{}'.format(coordinates[1]))
    if (coordinates[2] < minAngle3):
        raise Exception('The value for the third angle was too small, it was:{}'.format(coordinates[2]))
    elif (coordinates[2] > maxAngle3):
        raise Exception('The value for the third angle was too big, it was:{}'.format(coordinates[2]))
    else:
        baudRate = 9600
        serPort = "COM3"
        ser = serial.Serial(serPort, baudRate)
        stringToSend = (str(round(coordinates[0], 2)) + "," + str(round(coordinates[1], 2)) + "," + str(round(coordinates[2], 2)) + "\n")
        ser.write(stringToSend.encode('UTF-8'))