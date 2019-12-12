import math
import xylobot.Position as position

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

DEBUG = 1
# Length of stick, wrist, and their total
#L_STICK = 13.7
#WRIST_NO_STICK = 5
#WRIST = L_STICK + WRIST_NO_STICK
WRIST = 17.3
WRISTB = 17.55
# Length of elbow
ELBOW = 10.4
ELBOWB = 10.55

# Length of shoulder
SHOULDER = 18.8

# Origin
O = Point(0, 0, SHOULDER)

# Distance to target (3D)
dist2Target = 0

# Angles
cos_a1 = cos_b = 0
a = a1 = a2 = b = c = 0
actualPosition = Point(0, 27, SHOULDER)


def getAngles(t):
    # Calculate distance between target and origin
    try:
        t.z = t.z + 2
        dist2Target = math.sqrt((t.y - O.y)**2 + (t.z - O.z)**2)
        if DEBUG == 2:
            print('\nDistance to target: ', dist2Target, ' cm')

        if dist2Target > WRIST + ELBOW:
            raise Exception("DISTANCE TO TARGET TOO LARGE")



        cos_b = ((ELBOW ** 2) + (WRIST ** 2) - (dist2Target ** 2)) / (2 * WRIST * ELBOW)
        b = math.acos(cos_b) * 180 / math.pi

        if angleToMotorAngle(b) > 90:
            raise Exception("WRIST ANGLE TOO LARGE (> 90)")
        if angleToMotorAngle(b) < 0:
            raise Exception("WRIST ANGLE IS NEGATIVE")

        cos_a1 = ((ELBOW ** 2) + (dist2Target ** 2) - (WRIST ** 2)) / (2 * ELBOW * dist2Target)
        a1 = math.acos(cos_a1)*180/math.pi
        a2 = math.asin(t.y / dist2Target)*180/math.pi
        a = a1+a2

        c = math.atan2(t.x, t.y)*180/math.pi*-1
        angle1 = 180-a
        angle2 = 180-b
        if DEBUG == 2:
            print(angle1)
            print(angle2)
        d = (ELBOW*math.cos(math.radians(angle1)) + WRIST*math.cos(math.radians(angle1 + angle2)))
        e = (ELBOWB*math.cos(math.radians(angle1)) + WRISTB*math.cos(math.radians(angle1 + angle2)))
        c2 = math.degrees(math.acos(d/e))
        if DEBUG == 2:
            print(d, e, 'c2: ', c2)
        c = c - c2

        if c < -90 or c > 90:
            print(c)
            raise Exception("BASE ANGLE OUT OF BOUNDS")

        if angleToMotorAngle(a)*-1 < -90:
            raise Exception("ELBOW ANGLE TOO LARGE (> -90)")
        if angleToMotorAngle(a)*-1 > 0:
            raise Exception("ELBOW ANGLE IS NEGATIVE")

        setActualPos(t)
        if DEBUG == 2:
            print('Original angles - origin angle: ', c, ' elbow angle: ', a, ' wrist angle: ', b)
            print('Arduino angles - origin angle: ', c, ' elbow angle: ', angleToMotorAngle(a)*-1,
                  ' wrist angle: ', angleToMotorAngle(b), '\n')

        return [c, angleToMotorAngle(a)*-1, angleToMotorAngle(b)]
        #return [-1*c, angleToMotorAngle(a) * 1, -1*angleToMotorAngle(b)]
    except Exception as e:
        raise Warning("[!] OUT OF REACH - ", e)
        pass

#   def getCoordinates(position):
#       m0 = position.m0
#       m1 = position.m1
#       m2 = position.m2
#       length2d = 0
#       x = math.sin(m0)*length2d
#       y = math.cos(m0)*length2d
#       z = SHOULDER +

def angleToMotorAngle(a):
    #dif = math.fabs(90 - a)
    #return -90 + dif
    return 180 - a

def setActualPos(pos):
    if DEBUG == 2:
        print('Setting new position ', pos.x, ' ', pos.y, ' ', pos.z)
    global actualPosition
    actualPosition = pos

def getActualPos():
    return actualPosition

#getAngles(Point(0, 25.5, 15))
