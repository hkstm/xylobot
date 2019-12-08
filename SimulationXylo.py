from SimuVector import SimuVector
from SimuKey import SimuKey
import numpy as np

import copy
from tkinter import *
import math

class SimulationXylo:
    #All lengths are in cm!
    #Distances between notes:
    DISTANCEBETWEENMIDPOINTS = 60
    HEIGHT_DIFF = 15
    COLORS = ["blue","green","yellow","orange","red", "purple","white","blue"]
    previousConstructedKeyLoc = SimuVector(450,170,0)
    previousConstructedKeyHeight = 300;


    def __init__(self, canvas, rotation,cenx, ceny, location = SimuVector(0,0,0)):
        self.rotation = rotation
        self.canvas = canvas


        self.createKeys()
        self.goodRotate(45)
        for key in self.keys:
            self.draw_square(key.getPoints(),key.getColor())

        midp = self.getXyloMidpoint()
        #self.canvas.create_line(0, 0,midp.x,midp.y, fill="pink", width=10, joinstyle=ROUND)
        # print('cenx: ', self.CENTER_X)
        # print('ceny: ', self.CENTER_Y)



    def createKeys(self):
        self.keys = []
        for color in self.COLORS:
            self.previousConstructedKeyLoc.x+= self.DISTANCEBETWEENMIDPOINTS
            #newKeyLoc = copy.deepcopy(self.previousConstructedKeyLoc.deepCopy())
            newKeyLoc = self.previousConstructedKeyLoc
            self.previousConstructedKeyHeight -= self.HEIGHT_DIFF
            newKey = SimuKey(color,newKeyLoc,0,self.previousConstructedKeyHeight)
            self.keys.append(newKey)

    def draw_square(self, points, color="red"):
        #print('square should be drawn!:')
        #print(np.matrix(points))
        self.canvas.create_polygon(points, fill=color)



    def midpoint(self, p1, p2):
        newVec = SimuVector((p1.x + p2.x) / 2, (p1.y + p2.y) / 2, p1.z)
        print('xylomid: ',newVec.x, newVec.y)
        return SimuVector((p1.x + p2.x) / 2, (p1.y + p2.y) / 2, p1.z)


    def getXyloMidpoint(self):
        return self.midpoint(self.keys[3].location, self.keys[4].location)

    def setXyloMidpoint(self,midpoint):
        currentXyloMidVec = self.getXyloMidpoint()
        toTranslateX = midpoint.x - currentXyloMidVec.x
        toTranslateY = midpoint.y - currentXyloMidVec.y
        for key in self.keys:
            key.translate(toTranslateX,toTranslateY)


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

