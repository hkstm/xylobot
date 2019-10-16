import pygame
import math
import IK

WIDTH = 800
HEIGHT = 600
MULTIPLIER = 10

WHITE = pygame.Color(255,255,255)
BLACK = pygame.Color(0,0,0)
RED = pygame.Color(255,0,0)
BLUE = pygame.Color(0,0,255)
GREEN = pygame.Color(0,255,0)
YELLOW = pygame.Color(0, 128, 255)
GRAY = pygame.Color(128,128,128)



def drawAxes():
    pygame.draw.line(screen, GRAY, (WIDTH - 20, HEIGHT - 20), (20, HEIGHT - 20), 6)
    pygame.draw.line(screen, GRAY, (WIDTH - 20, HEIGHT - 20), (WIDTH - 20, 20), 6)

def drawBot(base, elbow, wrist, a, b):
    a = 270 - a
    b = 270 - b

    startBaseX = WIDTH - 40
    startBaseY = HEIGHT - (base * MULTIPLIER)

    startElbowX = WIDTH - 30
    startElbowY = HEIGHT - (base * MULTIPLIER)
    endElbowX = startElbowX + math.cos(math.radians(a)) * elbow * MULTIPLIER
    endElbowY = startElbowY + math.sin(math.radians(a)) * elbow * MULTIPLIER
    endWristX = endElbowX + math.cos(math.radians(b)) * wrist * MULTIPLIER
    endWristY = endElbowY + math.sin(math.radians(b)) * wrist * MULTIPLIER

    pygame.draw.rect(screen, BLACK, pygame.Rect(startBaseX, startBaseY, 19, base * MULTIPLIER - 20))
    pygame.draw.circle(screen, RED, (int(startElbowX), int(startElbowY)), 5)
    pygame.draw.line(screen, BLACK, (startElbowX, startElbowY), (endElbowX, endElbowY))
    pygame.draw.circle(screen, RED, (int(endElbowX), int(endElbowY)), 5)
    pygame.draw.line(screen, BLACK, (endElbowX, endElbowY), (endWristX, endWristY))
    pygame.draw.circle(screen, BLACK, (int(endWristX), int(endWristY)), 5)

def drawTarget(x, y):
    pygame.draw.circle(screen, RED, (x, y), 5)
    pygame.draw.line(screen, GREEN, (WIDTH-30, HEIGHT - (19 * MULTIPLIER)), (x, y))

def transformCoords(x, y):
    newX = math.fabs(x - WIDTH) / MULTIPLIER
    newY = math.fabs(y - HEIGHT) / MULTIPLIER
    return newX, newY

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False
x = y = 0
a = b = 0
target = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            target = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            target = False

        screen.fill(WHITE)
        if target:
            drawTarget(x, y)
            t_Y, t_Z = transformCoords(x, y)
            print('\nTarget coords: ', t_Y, ' ', t_Z)
            target = IK.Point(0, round(t_Y, 2), round(t_Z, 2))
            try:
                angles = IK.getAngles(target)
                a = angles[1]
                b = angles[2]
            except Warning as w:
                print(w)
        drawAxes()
        drawBot(IK.SHOULDER, IK.ELBOW, IK.WRIST, a*-1, (a*-1+b))
        pygame.display.flip()

