from controll.ControlManager import ControlManager
from Point import Point
from controll.Kinematics import Kinematics
from controll.SongManager import Note
from controll.Hit import QuadraticHit

import random

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
#notes = [[10.25, 23, 12], [7.298546685112846, 25.239398193359374, 12], [3.7181376817491305, 24.618950500488282, 12], [1.0128165690104156, 24.058391418457035, 12], [-1.6065462917751745, 23.74452056884766, 12], [-5.050903049045139, 23.642464599609376, 12], [-8.5511225382487, 23.642464599609376, 12], [-12.27368394639757, 24.626063232421878, 12]]]


def randomNotes(delay, amount):
    list = []
    for i in range(0, amount):
        r = int(random.randrange(1,8,1))

        if(r == 1):
            note = Note("c6", delay)

        if (r == 2):
            note = Note("d6", delay)

        if (r == 3):
            note = Note("e6", delay)

        if (r == 4):
            note = Note("f6", delay)

        if (r == 5):
            note = Note("g6", delay)

        if (r == 6):
            note = Note("a6", delay)

        if (r == 7):
            note = Note("b6", delay)

        if (r == 8):
            note = Note("c7", delay)
        list.append(note)
    return list


cm = ControlManager()
cm.setNoteCoordinates(coords)
cm.addSong('test', 20, randomNotes(0.8, 10))
for s in cm.getSongs():
   for n in s.notes:
        print(n)
cm.play()
k = Kinematics(17.3, 10.4, 18.8, Point(0, 23, 13))
k.getAngles(Point(15, 27, 22), Point(10, 21, 13))
