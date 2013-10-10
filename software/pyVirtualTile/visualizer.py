import sys
import pygame

colors = []

for x in range(9):
    colors.append(pygame.Color(0,0,0,0))
pygame.init()

dwidth  = 256
dheight = 256

rects = []
for y in range(3):
    for x in range(3):
        rects.append(pygame.Rect(y*(dheight/3)+4,x*(dheight/3)+4,dwidth/3-8,dheight/3-8))


displaySurface = pygame.display.set_mode((dwidth,dheight),pygame.DOUBLEBUF)
fpsClock = pygame.time.Clock()

def draw():
    for i in range(9):
        displaySurface.fill(colors[i],rects[i])
        print colors[i]
    pygame.display.flip()              

def hexToColor(hexDigits):
    vals    = [hexDigits[x:x+2] for x in range(1,6,2)]
    color   = []
    for val in vals:
        color.append(int(val,16))
    return pygame.Color(color[0],color[1],color[2])

while(1):
    command = sys.stdin.readline()
    if command == ':u\n':
        print 'update'
        draw()
    else:
        target          = int(command[1])
        color           = hexToColor(command[1:])
        colors[target]  = color
