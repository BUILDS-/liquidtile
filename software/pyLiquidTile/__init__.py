import serial,sys
import numpy as np

class LiquidTile(object):
    """
    Generic Liquid Tile, supports the basic LiquidTile UART protocol (v1):

    LiquidTile UART protocol is an ASCII formatted serial communications protocol. 
    Standard speed is 19200 baud.
    """
    def __init__(self, port="", speed=19200, loopback=False):
        self.port = port
        self.speed = speed
        self.ser = None
        self.loopback = loopback

        if self.loopback:
            self.ser = sys.stdout 
        else:
            self.ser = serial.Serial(self.port, self.speed)

    def setPixel(self, addr, color):
        send_str = ":{0:0x}{1:02x}{2:02x}{3:02x}\n".format(addr, int(color[0])&0xff, int(color[1])&0xff,int(color[2])&0xff)
        self.ser.write(send_str)

    def update(self):
        self.ser.write(":u\n")
        self.ser.flush()

    def clear(self, tile_size=9):
        for i in range(tile_size):
            self.setPixel(i, [0,0,0])

    def close(self):
        self.ser.close()

class LiquidTile3x3(LiquidTile):
    """
    Supports specific mapping for a 3x3 tile_size
    """
    def setCoordinate(self, coordinates, color):
        """
        Set coordinate to color

        @var coordinate is a tuple (x, y) where x and y are integers in the range [0, 2]
        @var color is an array of 3 colors [r,g,b]
        """
        addr = coordinates[0] + coordinates[1]*3
        self.setPixel(addr, color)

    def setFrame(self,frame):
        """
        Set frame

        @var frame is a 3x3x3 array (grid with the rgb colors in each spot)
        """
        for x in range(3):
            for y in range(3):
                self.setCoordinate((x,y),frame[x][y])

class LiquidTileNxN(LiquidTile):
    
    #Constants
    
    def __init__(self, port="", speed=19200,width = 3, height = 3, loopback=False):
        LiquidTile.__init__(self,port,speed,loopback)
        self.width      = width
        self.height     = height
        
        self.fullMask   = np.ones(shape=(height,width),dtype=np.int32) * 255
        self.emptyMask  = np.zeros(shape=(height,width),dtype=np.int32)


        self.frame      =   np.zeros(shape=(3,height,width),dtype=np.int16)
        self.red        =   self.frame[0]
        self.green      =   self.frame[1]
        self.blue       =   self.frame[2]
    def pushFrame(self):
        for y in xrange(self.height):
            for x in xrange(self.width):
                self.setPixel(x+(self.width*y),[self.red[x][y],self.green[x][y],self.blue[x][y]])
    
    def scaleBrightness(self,scale):
        '''
        Scale the brightness of the whole frame by scale factor.

        @var scale is the scale factor to multiply all color values by, usually a float.
        '''
        self.frame *= scale
        self.frame &= 255
    
    def addToCell(self,x,y,color):
        '''
        Add the colors in a given cell with a given color value.

        @var x is the x coordinate of the cell.
        @var y is the y coordinate of the cell.
        @var color is a (r,g,b) color tuple to be added.
        '''
        self.red[x][y]  += color[0]
        self.green[x][y]  += color[1]
        self.blue[x][y]  += color[2]
        self.frame &= 255

    def addToColumn(self,column,color):
        '''
        Add the colors in a given column with a given color value

        @var column designates the column to be added to.
        @var color is a (r,g,b) color tuple to be added.
        '''

        self.red[:,column] += color[0]
        self.green[:,column] += color[1]
        self.blue[:,column] += color[2]
        self.frame &= 255

    def addToRow(self,row,color):
        '''
        Add the colors in a given row with a given color value

        @var row designates the row to be added to.
        @var color is a (r,g,b) color tuple to be added.
        '''
        
        self.red[row] += color[0]
        self.green[row] += color[1]
        self.blue[row] += color[2]
        self.frame &= 255

    def setCell(self,x,y,color):
        '''
        Set the colors in a given row to a given color value.
        
        @var x is the x coordinate of the cell.
        @var y is the y coordinate of the cell.
        @var color is a (r,g,b) color tuple that cell will be set to.
        
        '''

        self.red[x][y]  = color[0]
        self.green[x][y]  = color[1]
        self.blue[x][y]  = color[2]
        self.frame &=255

    def setColumn(self,column,color):
        '''
        Set the colors in a given column to a given color value

        @var column designates the column to be set.
        @var color is a (r,g,b) color tuple that the column will be set to.
        '''

        self.red[:,column] = color[0]
        self.green[:,column] = color[1]
        self.blue[:,column] = color[2]
        self.frame &= 255

    def setRow(self,row,color):
        '''
        Set the colors in a given row with to given color value

        @var row designates the row to be added to.
        @var color is a (r,g,b) color tuple that the row will be set to.
        '''

        self.red[row] = color[0]
        self.green[row] = color[1]
        self.blue[row] = color[2]
        self.frame &= 255

