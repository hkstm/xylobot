import serial
from control.HitManager import HitManager
from control.SongManager import SongManager


class ControlManager:

    def __init__(self, simu_xylo):
        self.ser = self.initArduino(9600, "COM3")
        self.hm = HitManager(self.ser, simu_xylo)
        self.sm = SongManager(self.hm)
        self.startMarker = 60
        self.endMarker = 62
        self.simu_xylo = simu_xylo

    def play(self, dynamics='p', hittype='triangle 2'):
        self.sm.play(dynamics, hittype)

    def addSong(self, name, tempo, notes):
        self.sm.add(name, tempo, notes)

    def hit(self, note, dynamics='pp', hittype='', tempo=0):
        malletBounce = 0
        if dynamics == 'pp':
            note.power = 1
            malletBounce = -0.1
        elif dynamics == 'mp':
            note.power = 2
            malletBounce = 0.7
        elif dynamics == 'p':
            note.power = 3
            malletBounce = 1
        elif dynamics == 'mf':
            note.power = 4
            malletBounce = 1.5
        elif dynamics == 'f':
            note.power = 5
            malletBounce = 1.3
        elif dynamics == 'ff':
            note.power = 5
            malletBounce = 1
        note.hittype = hittype
        print('malletBounce: ', malletBounce)
        self.sm.hit(note, tempo=tempo, malletBounce=malletBounce)

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







