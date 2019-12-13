import math
from Position import Position
from Point import Point


class Kinematics:
    def __init__(self, wrist, elbow, shoulder, initialPosition):
        self.wrist = wrist
        self.elbow = elbow
        self.shoulder = shoulder
        self.origin = Point(0, 0, self.shoulder)
        self.currentPosition = initialPosition

    def getAngles(self, t, curpos):
        # Calculate distance between target and origin
        try:
            dist2Target = math.sqrt((t.y - self.origin.y)**2 + (t.z - self.origin.z)**2)
            print('\nDistance to target: ', dist2Target, ' cm')

            if dist2Target > self.wrist + self.elbow:
                raise Exception("DISTANCE TO TARGET TOO LARGE")

            c = math.atan2(t.x, t.y)*-1

            projectedPosition = Point(curpos.x * math.cos(c) - curpos.y * math.sin(c),
                                      curpos.x * math.sin(c) + curpos.y * math.cos(c), curpos.z)
            print(projectedPosition)
            distanceOfProjPosFromOrigin = math.sqrt(projectedPosition.x ** 2 + projectedPosition.y ** 2)
            angleBetweenTargetAndProjectedPosition = math.atan(dist2Target / distanceOfProjPosFromOrigin) * 180 / math.pi
            print(c, angleBetweenTargetAndProjectedPosition)
            c = c * 180 / math.pi - angleBetweenTargetAndProjectedPosition
            print(' angle between: ', angleBetweenTargetAndProjectedPosition, ' newAngle: ', c)


            cos_b = ((self.elbow ** 2) + (self.wrist ** 2) - (dist2Target ** 2)) / (2 * self.wrist * self.elbow)
            b = math.acos(cos_b) * 180 / math.pi

            if self.angleToMotorAngle(b) > 90:
                raise Exception("self.wrist ANGLE TOO LARGE (> 90)")
            if self.angleToMotorAngle(b) < 0:
                raise Exception("self.wrist ANGLE IS NEGATIVE")

            cos_a1 = ((self.elbow ** 2) + (dist2Target ** 2) - (self.wrist ** 2)) / (2 * self.elbow * dist2Target)
            a1 = math.acos(cos_a1)*180/math.pi
            a2 = math.asin(t.y / dist2Target)*180/math.pi
            a = a1+a2

            if c < -90 or c > 90:
                print(c)
                raise Exception("BASE ANGLE OUT OF BOUNDS")

            if self.angleToMotorAngle(a)*-1 < -90:
                raise Exception("self.elbow ANGLE TOO LARGE (> -90)")
            if self.angleToMotorAngle(a)*-1 > 0:
                raise Exception("self.elbow ANGLE IS NEGATIVE")

            print('Original angles - origin angle: ', c, ' elbow angle: ', a, ' wrist angle: ', b)
            print('Arduino angles - origin angle: ', c, ' elbow angle: ', self.angleToMotorAngle(a)*-1,
                  ' wrist angle: ', self.angleToMotorAngle(b), '\n')

            return Position(c, self.angleToMotorAngle(a)*-1, self.angleToMotorAngle(b))
        except Exception as e:
            raise Warning("[!] OUT OF REACH - ", e)


    def angleToMotorAngle(self, a):
        return 180 - a

