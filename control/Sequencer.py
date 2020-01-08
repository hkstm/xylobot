import control.Control as c
#from control.ControlManager import ControlManager
import random
from Note import Note

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
sequence = randomNotes(0.8, 8)
try:
    c.play(sequence)
    #cm.play(sequence)
except Exception as e:
    print(e)
    pass
