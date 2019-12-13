from Point import Point
from controll.SongManager import Note
from controll.ControlManager import ControlManager
import time


class TestComponents:
    hittypes = ['quadratic', 'triangle 1', 'triangle 2', 'uniform']
    tempos = [100, 50, 20]
    leftlimits = [
        Point(0, 23, 14),
        Point(5, 23, 14),
        Point(10, 23, 14),
        Point(13, 23, 14),
        Point(15, 23, 14),
        Point(16, 23, 14),
        Point(18, 23, 14),
        Point(20, 23, 14),
    ]
    rightlimits = [
        Point(0, 23, 14),
        Point(-5, 23, 14),
        Point(-7, 23, 14),
        Point(-9, 23, 14),
        Point(-11, 23, 14),
        Point(-12, 23, 14),
        Point(-14, 23, 14),
        Point(-18, 23, 14),
    ]
    coords = [
        Point(10.25, 23, 12),
        Point(7.29, 23, 12),
        Point(3.71, 23, 12),
        Point(1.01, 23, 12),
        Point(-1.6, 23, 12),
        Point(-5.05, 23, 12),
        Point(-8.5, 23, 12),
        Point(-10.2, 23, 12)
    ]
    delay = 0.3
    notes = [
        Note('c6', delay),
        Note('d6', delay),
        Note('e6', delay),
        Note('f6', delay),
        Note('g6', delay),
        Note('a6', delay),
        Note('b6', delay),
        Note('c7', delay)
    ]

    keysequences = ['07162534', '02467531', '0770']


class Experiments:

    def __init__(self, cm):
        self.cm = cm
        self.cm.setNoteCoordinates(TestComponents.coords)

    def run(self):
        self.testHitAngles()
        self.testBounds()

    def testHitAngles(self):
        for note in self.getNotesFromSequence('000444777'):
            self.cm.hit(note)

        print('[*] Testing hit types')
        for type in TestComponents.hittypes:
            print('[*] Hit type: ', type)
            self.cm.setHitType(type)
            self.testTempo()

        #self.cm.setHitType('glissando')
        #self.cm.play()

    def testTempo(self):
        print('[*] Testing the tempo')
        for t in TestComponents.tempos:
            print('[*] Setting tempo to: ', t)
            self.cm.setTempo(t)
            self.cm.play()
            time.sleep(5)


    def setTempo(self, t):
        for song in self.cm.getSongs():
            song.setTempo(t)

    def testBounds(self):
        print('[*] Testing the bounds')
        for i in TestComponents.leftlimits:
            self.cm.hitPoint(i)
        for i in TestComponents.rightlimits:
            self.cm.hitPoint(i)

    def getNotesFromSequence(self, sequence=''):
        for seq in TestComponents.keysequences:
            notes = []
            for key in list(seq):
                notes.append(TestComponents.notes[int(key)])
            self.cm.addSong('test', 100, notes)
        else:
            notes = []
            for key in list(sequence):
                notes.append(TestComponents.notes[int(key)])
            return notes

e = Experiments(ControlManager())
e.run()