import serial
import xylobot.IK as ik
import xylobot.delayexample as delay
from xylobot.Point import Point
from xylobot.Position import Position
from xylobot.Control.HitManager import HitManager
from xylobot.Control.SongManager import SongManager


class ControlManager:
    XYLO_HEIGHT = 13

    def __init__(self):
        self.ser = self.initArduino(9600, "COM3")
        #self.ser = 0

        self.hm = HitManager(self.ser, self.XYLO_HEIGHT)
        self.sm = SongManager(self.hm)
        self.startMarker = 60
        self.endMarker = 62

    def play(self):
        self.sm.play()

    def addSong(self, name, tempo, notes):
        self.sm.add(name, tempo, notes)

    def setNoteCoordinates(self, coords):
        self.sm.initializeCoords(coords)

    def getSongs(self):
        return self.sm.getSongs()

    def initArduino(self, baudRate, serPort):
        ser = serial.Serial(serPort, baudRate)
        print("Serial port " + serPort + " opened,  Baudrate " + str(baudRate))
        return ser





