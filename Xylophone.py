import IK

LEFTBOUND = 18
RIGHTBOUND = -6
UPPERBOUND = 22
LOWERBOUND = 15
#           C          D        E         F       G         A          B         C
notes = [[18, 27, 15], [14, 27, 15], [10, 26, 15], [7, 25, 15], [4, 25, 15], [0, 26, 15], [-3, 26, 15], [-6, 27, 15]]

# TODO: Coordinate system of box and notes in relation to the bounds
# TODO: Define calibration as bot adjusting between left/right bounds (thus its Origin might change)
# TODO: Define note durations

def getMidpoint(noteToHit):
    oldPos = IK.getActualPos()
    print('Old position: ', oldPos.x, ' ', oldPos.y, ' ', oldPos.z)
    distanceBetweenNotesX = oldPos.x - noteToHit[0]
    distanceBetweenNotesY = oldPos.y - noteToHit[1]
    midpointX = oldPos.x - (distanceBetweenNotesX / 2)
    midpointY = oldPos.y - (distanceBetweenNotesY / 2)
    midpointZ = UPPERBOUND
    midpoint = IK.Point(midpointX, midpointY, midpointZ)
    print(midpoint.x, midpoint.y, midpoint.z)
    return midpoint


