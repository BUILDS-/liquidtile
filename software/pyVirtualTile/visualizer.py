import sys
import pygame

colors = []

if len(sys.argv) >= 3:
    tWidth = int(sys.argv[1])
    tHeight= int(sys.argv[2])
elif len(sys.argv) >1:
    tWidth = tHeight = int(sys.argv[1])
else:
    tWidth = tHeight = 3

tileCount = tWidth * tHeight

for x in range(tileCount):
    colors.append(pygame.Color(0,0,0,0))
pygame.init()

dwidth  = 256
dheight = 256

cellSize    = min(dwidth / tWidth, dheight/tHeight)
cellOffset  = cellSize/10


runGame = True

rects = []
for y in range(tHeight):
    for x in range(tWidth):
        rects.append(pygame.Rect( (y*cellSize)+cellOffset/2, (x*cellSize)+cellOffset/2, dwidth/tWidth-cellOffset,dheight/tHeight-cellOffset))


displaySurface = pygame.display.set_mode((dwidth,dheight),pygame.DOUBLEBUF)
fpsClock = pygame.time.Clock()

def draw():
    for i in range(tileCount):
        displaySurface.fill(colors[i],rects[i])
        #print(colors[i])
    pygame.display.flip()              

def hexToColor(hexDigits):
    vals    = [hexDigits[x:x+2] for x in range(1,6,2)]
    color   = []
    for val in vals:
        color.append(int(val,16))
    return pygame.Color(color[0],color[1],color[2])

while(runGame):
    command = sys.stdin.readline()
    if command == ':u\n':
        print('update')
        draw()
    else:
        target          = int(command[1],16)
        color           = hexToColor(command[1:])
        colors[target]  = color
	pygame.display.update()
	#Handle window messages to prevent freezing
	events = pygame.event.get()
    for e in events:
        if (e.type == pygame.QUIT):
            runGame = False
