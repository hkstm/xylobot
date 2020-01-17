import serial
from control.HitManager import HitManager
from control.SongManager import SongManager


class ControlManager:

    def __init__(self):
        self.ser = self.initArduino(9600, "COM3")
        #self.ser = 0

        self.hm = HitManager(self.ser)
        self.sm = SongManager(self.hm)
        self.startMarker = 60
        self.endMarker = 62

    def play(self):
        self.sm.play()

    def addSong(self, name, tempo, notes):
        self.sm.add(name, tempo, notes)

    def hit(self, note, hittype=''):
        self.sm.hit(note)

    def hitPoint(self, point):
        self.sm.hitPoint(point)

    def setNoteCoordinates(self, coords):
        self.sm.initializeCoords(coords)

    def getSongs(self):
        return self.sm.getSongs()

    def initArduino(self, baudRate, serPort):
        ser = serial.Serial(serPort, baudRate)
        print("Serial port " + serPort + " opened,  Baudrate " + str(baudRate))
        return ser

    def sendToArduino(self, pos):
        self.hm.sendToArduino(pos)

    def setHitType(self, hittype):
        self.hm.setHitType(hittype)







