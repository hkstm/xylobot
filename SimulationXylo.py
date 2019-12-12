from SimuVector import SimuVector
from SimuKey import SimuKey
import numpy as np

import copy
from tkinter import *
import math

class SimulationXylo:
    #CM!
    DISTANCEBETWEENMIDPOINTS = 20.5/7
    HEIGHT_DIFF = (11.5-8.3)/7
    WIDTH = (15)/7
    previousConstructedKeyLoc = SimuVector(450,170,0)
    previousConstructedKeyHeight = 11.5



    COLORS = ["blue","green","yellow","orange","red", "purple","white","pink"]
    CM_TOPIX_MULTIPLIER_X = 12
    CM_TOPIX_MULTIPLIER_Y = -12
    CM_TOPIX_X_OFFSET = 266
    CM_TOPIX_Y_OFFSET = 400

    def getConversions(self):
        return (0, self.CM_TOPIX_X_OFFSET, self.CM_TOPIX_Y_OFFSET)

    def __init__(self, canvas, rotation, location = SimuVector(0,0,0)):
        self.rotation = rotation
        self.canvas = canvas


        self.createKeys()
        self.goodRotate(0)
        self.setXyloMidpoint(SimuVector(0,10,0), cm = True)
        # for key in self.keys:
            #self.draw_square(key.getPoints(),key.getColor())

        midp = self.getXyloMidpoint()
        #self.canvas.create_line(0, 0,midp.x,midp.y, fill="pink", width=10, joinstyle=ROUND)
        # print('cenx: ', self.CENTER_X)
        # print('ceny: ', self.CENTER_Y)


    def getKeys(self):
        return self.keys

    def createKeys(self):
        self.keys = []
        for color in self.COLORS:
            #newKeyLoc = copy.deepcopy(self.previousConstructedKeyLoc.deepCopy())
            #LOCATION IS IN PIXELS
            newKeyLoc = self.previousConstructedKeyLoc
            #THE PREVIOUSCONSTRUCTEDKEYLOC IS NEVER USED AGAIN,
            #AND THE ACTUAL LOCATION IS RECALCULATED IN THE CONSTRUCTOR OF THE SIMUKEY
            self.previousConstructedKeyLoc.x += self.DISTANCEBETWEENMIDPOINTS * self.CM_TOPIX_MULTIPLIER_X
            newKey = SimuKey(color,newKeyLoc,0,self.previousConstructedKeyHeight*self.CM_TOPIX_MULTIPLIER_X, self.WIDTH*self.CM_TOPIX_MULTIPLIER_X)
            print('previousconstructedkeyheight: ',self.previousConstructedKeyHeight)
            self.previousConstructedKeyHeight -= self.HEIGHT_DIFF

            self.keys.append(newKey)

    def draw_square(self, points, color="red"):
        #print('square should be drawn!:')
        #print(np.matrix(points))
        self.canvas.create_polygon(points, fill=color)



    def midpoint(self, p1, p2):
        newVec = SimuVector((p1.x + p2.x) / 2, (p1.y + p2.y) / 2, p1.z)
        #print('xylomid: ',newVec.x, newVec.y)
        return SimuVector((p1.x + p2.x) / 2, (p1.y + p2.y) / 2, p1.z)


    def getXyloMidpoint(self, cm = False):
        return self.midpoint(self.keys[3].location, self.keys[4].location)

    def setXyloMidpoint(self,midpoint, cm = False):
        xmultiplier = 1
        ymultiplier = 1
        xoffset = 0
        yoffset = 0
        if(cm):
            xmultiplier = self.CM_TOPIX_MULTIPLIER_X
            ymultiplier = self.CM_TOPIX_MULTIPLIER_Y
            xoffset = self.CM_TOPIX_X_OFFSET
            yoffset = self.CM_TOPIX_Y_OFFSET

        currentXyloMidVec = self.getXyloMidpoint()
        toTranslateX = xoffset + midpoint.x*xmultiplier - currentXyloMidVec.x
        toTranslateY = yoffset + midpoint.y*ymultiplier - currentXyloMidVec.y
        for key in self.keys:
            key.translate(toTranslateX,toTranslateY)

    def getKeyLocation(self, index, cm = False):
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
        x = (keyloc.x - xoffset)/xmultiplier
        y = (keyloc.y - yoffset)/ymultiplier
        return SimuVector(x,y,0)


    def setRotation(self, angle):
        self.goodRotate(angle-self.rotation)


    def goodRotate(self, angle):
        self.rotation+= angle
        currentXyloMidVec = self.getXyloMidpoint()
        toTranslateX = 0-currentXyloMidVec.x
        toTranslateY = 0-currentXyloMidVec.y

        #toTranslateX = currentXyloMidVec.x -cenx
        #toTranslateY = currentXyloMidVec.y - ceny

        for key in self.keys:
            key.translate(toTranslateX,toTranslateY)

            key.rotate(angle)
            key.translate(-toTranslateX,-toTranslateY)

