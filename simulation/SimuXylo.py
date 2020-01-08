from SimuVector import SimuVector
from SimuKey import SimuKey
# from XylobotGUI import screen_factor
from win32api import GetSystemMetrics
import math
import time
import itertools

biv = None
sv = None


class SimuXylo:
    # CM!

    DISTANCEBETWEENMIDPOINTS = 20.5 / 7
    HEIGHT_DIFF = (11.5 - 8.3) / 7
    WIDTH = (15) / 7
    previousConstructedKeyLoc = SimuVector(450, 170, 0)
    previousConstructedKeyHeight = 11.5

    COLORS = ["blue", "green", "yellow", "orange", "red", "purple", "white", "pink"]
    multi = 12
    CM_TOPIX_multiplier_X = multi
    CM_TOPIX_multiplier_Y = -multi
    CM_TOPIX_X_OFFSET = 266
    CM_TOPIX_Y_OFFSET = 400

    def getConversions(self):
        return 0, self.CM_TOPIX_X_OFFSET, self.CM_TOPIX_Y_OFFSET

    def __init__(self, rotation, location=SimuVector(0, 0, 0)):
        screen_factor = 0.9
        self.arm_width = 20
        self.mallet_width = 5
        self.direction = 0
        self.lower_joint_angle = 160
        self.upper_joint_angle = 210
        self.base_length = 18.5
        self.lower_arm_length = 10
        self.upper_arm_length = 10
        self.mallet_length = 5
        self.distance = 20
        self.multiplier = 20
        self.xylophone_height = 10
        self.keywidth = self.multiplier * 2

        self.height = GetSystemMetrics(1) * screen_factor  # only works on windows with 1 screen I think
        self.width = GetSystemMetrics(0) * screen_factor  # only works on windows with 1 screen I think

        self.division = self.multiplier * 1
        self.top = self.height / 2 - self.multiplier * 5.53
        self.bottom = self.height / 2 + self.multiplier * 5.53
        self.left = self.width / 2 - self.multiplier * 11 - self.division / 2
        self.c = 0.4714
        self.rotation = rotation
        # TODO idk if canvas is needed for anything but it should not be
        # self.canvas = canvas

        self.createKeys()
        self.goodRotate(0)
        self.setXyloMidpoint(SimuVector(0, 10, 0), cm=True)
        # for key in self.keys:
        # self.draw_square(key.getPoints(),key.getColor())

        midp = self.getXyloMidpoint()

    # self.canvas.create_line(0, 0,midp.x,midp.y, fill="pink", width=10, joinstyle=ROUND)
    # print('cenx: ', self.CENTER_X)
    # print('ceny: ', self.CENTER_Y)

    def getKeys(self):
        return self.keys

    def createKeys(self):
        self.keys = []
        for color in self.COLORS:
            # newKeyLoc = copy.deepcopy(self.previousConstructedKeyLoc.deepCopy())
            # LOCATION IS IN PIXELS
            newKeyLoc = self.previousConstructedKeyLoc
            # THE PREVIOUSCONSTRUCTEDKEYLOC IS NEVER USED AGAIN,
            # AND THE ACTUAL LOCATION IS RECALCULATED IN THE CONSTRUCTOR OF THE SIMUKEY
            self.previousConstructedKeyLoc.x += self.DISTANCEBETWEENMIDPOINTS * self.CM_TOPIX_MULTIPLIER_X
            newKey = SimuKey(color, newKeyLoc, 0, self.previousConstructedKeyHeight * self.CM_TOPIX_MULTIPLIER_X,
                             self.WIDTH * self.CM_TOPIX_MULTIPLIER_X)
            print('previousconstructedkeyheight: ', self.previousConstructedKeyHeight)
            self.previousConstructedKeyHeight -= self.HEIGHT_DIFF

            self.keys.append(newKey)

    # def draw_square(self, points, color="red"):
    #     #print('square should be drawn!:')
    #     #print(np.matrix(points))
    #     self.canvas.create_polygon(points, fill=color)

    def midpoint(self, p1, p2):
        newVec = SimuVector((p1.x + p2.x) / 2, (p1.y + p2.y) / 2, p1.z)
        # print('xylomid: ',newVec.x, newVec.y)
        return SimuVector((p1.x + p2.x) / 2, (p1.y + p2.y) / 2, p1.z)

    def getXyloMidpoint(self, cm=False):
        return self.midpoint(self.keys[3].location, self.keys[4].location)

    def setXyloMidpoint(self, midpoint, cm=False):
        xmultiplier = 1
        ymultiplier = 1
        xoffset = 0
        yoffset = 0
        if (cm):
            xmultiplier = self.CM_TOPIX_MULTIPLIER_X
            ymultiplier = self.CM_TOPIX_MULTIPLIER_Y
            xoffset = self.CM_TOPIX_X_OFFSET
            yoffset = self.CM_TOPIX_Y_OFFSET

        currentXyloMidVec = self.getXyloMidpoint()
        toTranslateX = xoffset + midpoint.x * xmultiplier - currentXyloMidVec.x
        toTranslateY = yoffset + midpoint.y * ymultiplier - currentXyloMidVec.y
        for key in self.keys:
            key.translate(toTranslateX, toTranslateY)

    def getKeyLocation(self, index, cm=False):
        xmultiplier = 1
        ymultiplier = 1
        xoffset = 0
        yoffset = 0
        if (cm):
            xmultiplier = self.CM_TOPIX_MULTIPLIER_X
            ymultplier = self.CM_TOPIX_MULTIPLIER_Y
            xoffset = self.CM_TOPIX_X_OFFSET
            yoffset = self.CM_TOPIX_Y_OFFSET

        keys = self.keys
        keyloc = keys[index].getKeyMidpoint()
        x = (keyloc.x - xoffset) / xmultiplier
        y = (keyloc.y - yoffset) / ymultiplier
        return SimuVector(x, y, 0)

    def setRotation(self, angle):
        self.goodRotate(angle - self.rotation)

    def goodRotate(self, angle):
        self.rotation += angle
        currentXyloMidVec = self.getXyloMidpoint()
        toTranslateX = 0 - currentXyloMidVec.x
        toTranslateY = 0 - currentXyloMidVec.y

        # toTranslateX = currentXyloMidVec.x -cenx
        # toTranslateY = currentXyloMidVec.y - ceny

        for key in self.keys:
            key.translate(toTranslateX, toTranslateY)

            key.rotate(angle)
            key.translate(-toTranslateX, -toTranslateY)

    def update_base(self):
        self.base = self.bottom + self.multiplier * self.distance - 110.6

    def get_b_line(self):
        return (self.width / 2, self.base, self.width / 2, self.base,
                self.width / 2 + self.multiplier * self.lower_arm_length * math.cos(
                    math.radians(self.lower_joint_angle)) * math.sin(
                    math.radians(self.direction)),
                self.base + self.multiplier * (self.lower_arm_length * math.cos(
                    math.radians(self.lower_joint_angle)) * math.cos(
                    math.radians(self.direction))),
                self.width / 2 + self.multiplier * (self.lower_arm_length * math.cos(
                    math.radians(self.lower_joint_angle)) * math.sin(
                    math.radians(self.direction)) +
                                                    self.upper_arm_length * math.cos(
                            math.radians(self.upper_joint_angle)) * math.sin(
                            math.radians(self.direction))),
                self.base + self.multiplier * (self.lower_arm_length * math.cos(
                    math.radians(self.lower_joint_angle)) * math.cos(
                    math.radians(self.direction)) +
                                               self.upper_arm_length * math.cos(
                            math.radians(self.upper_joint_angle)) * math.cos(
                            math.radians(self.direction))))

    def get_s_line(self):
        return (self.width / 2 + self.multiplier * (self.distance), self.height,
                self.width / 2 + self.multiplier * (self.distance), self.height - self.multiplier * self.base_length,
                self.width / 2 + self.multiplier * (self.distance + self.lower_arm_length * math.cos(
                    math.radians(self.lower_joint_angle)) * math.cos(
                    math.radians(self.direction))),
                self.height - self.multiplier * (self.base_length + self.lower_arm_length * math.sin(
                    math.radians(self.lower_joint_angle))),
                self.width / 2 + self.multiplier * (self.distance + self.lower_arm_length * math.cos(
                    math.radians(self.lower_joint_angle)) * math.cos(
                    math.radians(self.direction)) +
                                                    self.upper_arm_length * math.cos(
                            math.radians(self.upper_joint_angle)) * math.cos(
                            math.radians(self.direction))),
                self.height - self.multiplier * (self.base_length + self.lower_arm_length * math.sin(
                    math.radians(self.lower_joint_angle)) +
                                                 self.upper_arm_length * math.sin(
                            math.radians(self.upper_joint_angle))))

    def get_b_mallet(self):
        return (self.width / 2 + self.multiplier * (
                self.lower_arm_length * math.cos(math.radians(self.lower_joint_angle)) * math.sin(
            math.radians(self.direction)) +
                self.upper_arm_length * math.cos(math.radians(self.upper_joint_angle)) * math.sin(
            math.radians(self.direction)) +
                (self.arm_self.width / (2 * self.multiplier)) * math.cos(math.radians(self.upper_joint_angle - 90))),
                self.base + self.multiplier * (self.lower_arm_length * math.cos(
                    math.radians(self.lower_joint_angle)) * math.cos(
                    math.radians(self.direction)) +
                                               self.upper_arm_length * math.cos(
                            math.radians(self.upper_joint_angle)) * math.cos(
                            math.radians(self.direction)) +
                                               (self.arm_self.width / (2 * self.multiplier)) * math.sin(
                            math.radians(self.upper_joint_angle - 90))),
                self.width / 2 + self.multiplier * (self.lower_arm_length * math.cos(
                    math.radians(self.lower_joint_angle)) * math.sin(
                    math.radians(self.direction)) +
                                                    (
                                                            self.upper_arm_length + self.mallet_length) * math.cos(
                            math.radians(self.upper_joint_angle)) * math.sin(
                            math.radians(self.direction)) +
                                                    (self.arm_self.width / (2 * self.multiplier)) * math.cos(
                            math.radians(self.upper_joint_angle - 90))),
                self.base + self.multiplier * (self.lower_arm_length * math.cos(
                    math.radians(self.lower_joint_angle)) * math.cos(
                    math.radians(self.direction)) +
                                               (self.upper_arm_length + self.mallet_length) * math.cos(
                            math.radians(self.upper_joint_angle)) * math.cos(
                            math.radians(self.direction)) +
                                               (self.arm_self.width / (2 * self.multiplier)) * math.sin(
                            math.radians(self.upper_joint_angle - 90))))

    def get_s_mallet(self):
        return (self.width / 2 + self.multiplier * (
                self.distance + self.lower_arm_length * math.cos(math.radians(self.lower_joint_angle)) * math.cos(
            math.radians(self.direction)) +
                self.upper_arm_length * math.cos(math.radians(self.upper_joint_angle)) * math.cos(
            math.radians(self.direction)) +
                (self.arm_self.width / (2 * self.multiplier)) * math.cos(math.radians(self.upper_joint_angle - 90))),
                self.height - self.multiplier * (self.self.base_length + self.lower_arm_length * math.sin(
                    math.radians(self.lower_joint_angle)) +
                                                 self.upper_arm_length * math.sin(
                            math.radians(self.upper_joint_angle)) +
                                                 (self.arm_self.width / (2 * self.multiplier)) * math.sin(
                            math.radians(self.upper_joint_angle - 90))),
                self.width / 2 + self.multiplier * (self.distance + self.lower_arm_length * math.cos(
                    math.radians(self.lower_joint_angle)) * math.cos(
                    math.radians(self.direction)) +
                                                    (self.upper_arm_length + self.mallet_length) * math.cos(
                            math.radians(self.upper_joint_angle)) * math.cos(
                            math.radians(self.direction)) +
                                                    (self.arm_self.width / (2 * self.multiplier)) * math.cos(
                            math.radians(self.upper_joint_angle - 90))),
                self.height - self.multiplier * (self.self.base_length + self.lower_arm_length * math.sin(
                    math.radians(self.lower_joint_angle)) +
                                                 (self.upper_arm_length + self.mallet_length) * math.sin(
                            math.radians(self.upper_joint_angle)) +
                                                 (self.arm_self.width / (2 * self.multiplier)) * math.sin(
                            math.radians(self.upper_joint_angle - 90))))

    def fill_canvas(self, birds_eye_view, side_view, goal_direction, goal_lower_joint_angle, goal_upper_joint_angle,
                    seconds):
        biv = birds_eye_view
        sv = side_view
        sleep_time = seconds / abs(goal_direction - self.direction)
        width = birds_eye_view.winfo_screenwidth() / 3
        height = birds_eye_view.winfo_screenheight() / 2
        bottom = height / 2 + self.multiplier * 5.53
        base = bottom + self.multiplier * self.distance - 110.6
        left = width / 2 - self.multiplier * 11 - self.division / 2
        s_line = side_view.find_withtag("s_line")
        b_line = birds_eye_view.find_withtag("b_line")
        s_mallet = side_view.find_withtag("s_mallet")
        b_mallet = birds_eye_view.find_withtag("b_mallet")

        keys = self.getKeys()
        for key in keys:
            color = key.getColor()
            thiskey = birds_eye_view.find_withtag(color)
            pts = key.getPoints()
            # for tuplee in pts:
            # 	for pt in tuplee:
            # 		print(pt)
            # birds_eye_view.coords(thiskey,(pts[0][0],pts[0][1]),(pts[1][0],pts[1][1]),(pts[2][0],pts[2][1]),(pts[3][0],pts[3][1]))
            birds_eye_view.coords(thiskey, *flatten(pts))

        done = False
        while not done:
            done = True
            if (self.direction < goal_direction):
                self.direction += 1
                done = False
            elif (self.direction > goal_direction):
                self.direction -= 1
                done = False
            if (self.lower_joint_angle < goal_lower_joint_angle):
                self.lower_joint_angle += 1
                done = False
            elif (self.lower_joint_angle > goal_lower_joint_angle):
                self.lower_joint_angle -= 1
                done = False
            if (self.upper_joint_angle < goal_upper_joint_angle):
                self.upper_joint_angle += 1
                done = False
            elif (self.upper_joint_angle > goal_upper_joint_angle):
                self.upper_joint_angle -= 1
                done = False
            birds_eye_view.coords(b_line, width / 2, self.base,
                                  width / 2, self.base,
                                  width / 2 + self.multiplier * self.lower_arm_length * math.cos(
                                      math.radians(self.lower_joint_angle)) * math.sin(math.radians(self.direction)),
                                  self.base + self.multiplier * (
                                          self.lower_arm_length * math.cos(
                                      math.radians(self.lower_joint_angle)) * math.cos(
                                      math.radians(self.direction))),
                                  width / 2 + self.multiplier * (
                                          self.lower_arm_length * math.cos(
                                      math.radians(self.lower_joint_angle)) * math.sin(
                                      math.radians(self.direction)) +
                                          self.upper_arm_length * math.cos(
                                      math.radians(self.upper_joint_angle)) * math.sin(
                                      math.radians(self.direction))),
                                  self.base + self.multiplier * (
                                          self.lower_arm_length * math.cos(
                                      math.radians(self.lower_joint_angle)) * math.cos(
                                      math.radians(self.direction)) +
                                          self.upper_arm_length * math.cos(
                                      math.radians(self.upper_joint_angle)) * math.cos(
                                      math.radians(self.direction))))
            side_view.coords(s_line, width / 2 + self.multiplier * (self.distance), height,
                             width / 2 + self.multiplier * (self.distance), height - self.multiplier * self.self.base_length,
                             width / 2 + self.multiplier * (
                                     self.distance + self.lower_arm_length * math.cos(
                                 math.radians(self.lower_joint_angle)) * math.cos(
                                 math.radians(self.direction))),
                             height - self.multiplier * (
                                     self.self.base_length + self.lower_arm_length * math.sin(
                                 math.radians(self.lower_joint_angle))),
                             width / 2 + self.multiplier * (
                                     self.distance + self.lower_arm_length * math.cos(
                                 math.radians(self.lower_joint_angle)) * math.cos(
                                 math.radians(self.direction)) +
                                     self.upper_arm_length * math.cos(math.radians(self.upper_joint_angle)) * math.cos(
                                 math.radians(self.direction))),
                             height - self.multiplier * (
                                     self.self.base_length + self.lower_arm_length * math.sin(
                                 math.radians(self.lower_joint_angle)) +
                                     self.upper_arm_length * math.sin(math.radians(self.upper_joint_angle))))
            birds_eye_view.coords(b_mallet, width / 2 + self.multiplier * (
                    self.lower_arm_length * math.cos(math.radians(self.lower_joint_angle)) * math.sin(
                math.radians(self.direction)) +
                    self.upper_arm_length * math.cos(math.radians(self.upper_joint_angle)) * math.sin(
                math.radians(self.direction)) -
                    (self.arm_width / (2 * self.multiplier)) * math.sin(math.radians(self.direction - 90))),
                                  self.base + self.multiplier * (
                                          self.lower_arm_length * math.cos(
                                      math.radians(self.lower_joint_angle)) * math.cos(
                                      math.radians(self.direction)) +
                                          self.upper_arm_length * math.cos(
                                      math.radians(self.upper_joint_angle)) * math.cos(
                                      math.radians(self.direction)) -
                                          (self.arm_width / (2 * self.multiplier)) * math.cos(
                                      math.radians(self.direction - 90))),
                                  width / 2 + self.multiplier * (
                                          self.lower_arm_length * math.cos(
                                      math.radians(self.lower_joint_angle)) * math.sin(
                                      math.radians(self.direction)) +
                                          (self.upper_arm_length + self.mallet_length) * math.cos(
                                      math.radians(self.upper_joint_angle)) * math.sin(math.radians(self.direction)) -
                                          (self.arm_width / (2 * self.multiplier)) * math.sin(
                                      math.radians(self.direction - 90))),
                                  self.base + self.multiplier * (
                                          self.lower_arm_length * math.cos(
                                      math.radians(self.lower_joint_angle)) * math.cos(
                                      math.radians(self.direction)) +
                                          (self.upper_arm_length + self.mallet_length) * math.cos(
                                      math.radians(self.upper_joint_angle)) * math.cos(math.radians(self.direction)) -
                                          (self.arm_width / (2 * self.multiplier)) * math.cos(
                                      math.radians(self.direction - 90))))
            side_view.coords(s_mallet, width / 2 + self.multiplier * (
                    self.distance + self.lower_arm_length * math.cos(math.radians(self.lower_joint_angle)) * math.cos(
                math.radians(self.direction)) +
                    self.upper_arm_length * math.cos(math.radians(self.upper_joint_angle)) * math.cos(
                math.radians(self.direction)) +
                    (self.arm_width / (2 * self.multiplier)) * math.cos(math.radians(self.upper_joint_angle - 90))),
                             height - self.multiplier * (
                                     self.self.base_length + self.lower_arm_length * math.sin(
                                 math.radians(self.lower_joint_angle)) +
                                     self.upper_arm_length * math.sin(math.radians(self.upper_joint_angle)) +
                                     (self.arm_width / (2 * self.multiplier)) * math.sin(
                                 math.radians(self.upper_joint_angle - 90))),
                             width / 2 + self.multiplier * (
                                     self.distance + self.lower_arm_length * math.cos(
                                 math.radians(self.lower_joint_angle)) * math.cos(
                                 math.radians(self.direction)) +
                                     (self.upper_arm_length + self.mallet_length) * math.cos(
                                 math.radians(self.upper_joint_angle)) * math.cos(math.radians(self.direction)) +
                                     (self.arm_width / (2 * self.multiplier)) * math.cos(
                                 math.radians(self.upper_joint_angle - 90))),
                             height - self.multiplier * (
                                     self.self.base_length + self.lower_arm_length * math.sin(
                                 math.radians(self.lower_joint_angle)) +
                                     (self.upper_arm_length + self.mallet_length) * math.sin(
                                 math.radians(self.upper_joint_angle)) +
                                     (self.arm_width / (2 * self.multiplier)) * math.sin(
                                 math.radians(self.upper_joint_angle - 90))))
            time.sleep(sleep_time)
            if ((width / 2 + self.multiplier * (
                    self.distance + self.lower_arm_length * math.cos(math.radians(self.lower_joint_angle)) * math.cos(
                math.radians(self.direction)) +
                    (self.upper_arm_length + self.mallet_length) * math.cos(math.radians(self.upper_joint_angle)) * math.cos(
                math.radians(self.direction)) +
                    (self.arm_width / (2 * self.multiplier)) * math.cos(
                math.radians(self.upper_joint_angle - 90))) >= width / 2 - self.multiplier * 5.53) &
                    (width / 2 + self.multiplier * (
                            self.distance + self.lower_arm_length * math.cos(
                        math.radians(self.lower_joint_angle)) * math.cos(
                        math.radians(self.direction)) +
                            (self.upper_arm_length + self.mallet_length) * math.cos(
                        math.radians(self.upper_joint_angle)) * math.cos(
                        math.radians(self.direction)) +
                            (self.arm_width / (2 * self.multiplier)) * math.cos(
                        math.radians(self.upper_joint_angle - 90))) <= width / 2 + self.multiplier * 5.53) &
                    (width / 2 + self.multiplier * (
                            self.lower_arm_length * math.cos(math.radians(self.lower_joint_angle)) * math.sin(
                        math.radians(self.direction)) +
                            (self.upper_arm_length + self.mallet_length) * math.cos(
                        math.radians(self.upper_joint_angle)) * math.sin(math.radians(self.direction)) -
                            (self.arm_width / (2 * self.multiplier)) * math.sin(
                        math.radians(self.direction - 90))) <= left + 7 * (self.keywidth + self.division) + self.keywidth) &
                    (width / 2 + self.multiplier * (
                            self.lower_arm_length * math.cos(math.radians(self.lower_joint_angle)) * math.sin(
                        math.radians(self.direction)) +
                            (self.upper_arm_length + self.mallet_length) * math.cos(
                        math.radians(self.upper_joint_angle)) * math.sin(math.radians(self.direction)) -
                            (self.arm_width / (2 * self.multiplier)) * math.sin(
                        math.radians(self.direction - 90))) >= left + 0 * (self.keywidth + self.division)) &
                    (height - self.multiplier * (
                            self.self.base_length + self.lower_arm_length * math.sin(
                        math.radians(self.lower_joint_angle)) +
                            (self.upper_arm_length + self.mallet_length) * math.sin(math.radians(self.upper_joint_angle)) +
                            (self.arm_width / (2 * self.multiplier)) * math.sin(
                        math.radians(self.upper_joint_angle - 90))) >= height - self.multiplier * self.xylophone_height)):
                done = True
            side_view.update_idletasks()
            birds_eye_view.update_idletasks()
        return self.direction, self.lower_joint_angle, self.upper_joint_angle

    def update_joint_angles(self, direction, lower_joint_angle, upper_joint_angle):
        self.direction = direction
        self.lower_joint_angle = lower_joint_angle
        self.upper_joint_angle = upper_joint_angle

    def get_side_view_rectangle(self):
        topleftx = self.width / 2 - self.multiplier * 5.53
        toplefty = self.height - self.multiplier * self.xylophone_height
        bottomrightx = self.width / 2 + self.multiplier * 5.53
        bottomrighty = self.height
        return topleftx, toplefty, bottomrightx, bottomrighty

    def moveSimulationRobot(self, angle1, angle2, angle3):
        width = biv.winfo_screenwidth() / 3
        height = biv.winfo_screenheight() / 2
        bottom = height / 2 + self.multiplier * 5.53
        base = bottom + self.multiplier * self.distance - 110.6
        left = width / 2 - self.multiplier * 11 - self.division / 2
        s_line = sv.find_withtag("s_line")
        b_line = biv.find_withtag("b_line")
        s_mallet = sv.find_withtag("s_mallet")
        b_mallet = biv.find_withtag("b_mallet")

    def updateXyloDrawing(self, birds_eye_view):
        keys = self.getKeys()
        for key in keys:
            color = key.getColor()
            print(color)
            thiskey = birds_eye_view.find_withtag(color)
            pts = key.getPoints()
            # for tuplee in pts:
            # 	for pt in tuplee:
            # 		print(pt)
            # birds_eye_view.coords(thiskey,(pts[0][0],pts[0][1]),(pts[1][0],pts[1][1]),(pts[2][0],pts[2][1]),(pts[3][0],pts[3][1]))
            # np.print(flatten(pts))
            # newpts = flatten(pts)
            # for item in newpts:
            # 	print(item)

            birds_eye_view.coords(thiskey, *flatten(pts))
            # birds_eye_view.coords(thiskey, *newpts)

            print(key.getKeyMidpoint().y)
            print(key.getPoints()[0])
            birds_eye_view.update_idletasks()

        # ##TODO REMOVE THIS TESTER:
        # print(xylo.getKeyLocation( 0, cm = True).x,"  ",xylo.getKeyLocation(0, cm = True).y)
        # midpp = xylo.getXyloMidpoint()
        # offsets = xylo.getConversions()
        # birds_eye_view.create_line(midpp.x, midpp.y, offsets[1],offsets[2])


def flatten(list_of_lists):
    """Flatten one level of nesting"""
    return itertools.chain.from_iterable(list_of_lists)
