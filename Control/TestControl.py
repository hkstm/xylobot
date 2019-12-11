from xylobot.Control.ControlManager import ControlManager
from xylobot.Control.HitManager import Point
from xylobot.Control.SongManager import Note
from xylobot.Control.Hit import QuadraticHit
import random

coords = [
    Point(18, 25, 15),
    Point(14, 25, 15),
    Point(10, 25, 15),
    Point(7, 25, 15),
    Point(4, 25, 15),
    Point(0, 25, 15),
    Point(-3, 25, 15),
    Point(-6, 25, 15)
]

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


#cm = ControlManager()
#cm.setNoteCoordinates(coords)
#cm.addSong('test', 20, randomNotes(0.8, 5))
#cm.play()