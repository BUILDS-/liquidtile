import sys
import pygame

#GLOBALS
colors  =   []
rects   =   []

displaySurface = None

dwidth  = 256
dheight = 256
tileCount = cellSize = cellOffset = 0

def draw():
    global colors
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

def init():
    global rects,colors,tileCount,cellSize,cellOffset,displaySurface
    #Get commandline arguments and decide how big our virtual tile is
    if len(sys.argv) >= 3:
        tWidth = int(sys.argv[1])
        tHeight= int(sys.argv[2])
    elif len(sys.argv) >1:
        tWidth = tHeight = int(sys.argv[1])
    else:
        tWidth = tHeight = 3

    tileCount = tWidth * tHeight

    #Pygame setup functions
    pygame.init()
    displaySurface = pygame.display.set_mode((dwidth,dheight),pygame.DOUBLEBUF)

    #Calculate how big our individual cells in the tile should be based on how big our window is.
    cellSize    = min(dwidth / tWidth, dheight/tHeight)
    cellOffset  = cellSize/10

    #Initialize the array of tile colors.
    for x in range(tileCount):
        colors.append(pygame.Color(0,0,0,0))

    #Initialize the locations of our tiles on the screen
    for y in range(tHeight):
        for x in range(tWidth):
            rects.append(pygame.Rect( (y*cellSize)+cellOffset/2, (x*cellSize)+cellOffset/2, dwidth/tWidth-cellOffset,dheight/tHeight-cellOffset))


def main():
    runGame = True
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

if __name__ == "__main__":
    init()
    main()
