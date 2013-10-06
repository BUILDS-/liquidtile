import pyFireTile
from time import sleep

t = led_tile.LEDTile("/dev/tty.usbserial-A600aflQ")
t.open()
t.clear()

try:
    while 1:
        for j in (range(255)[0::16]):
            for i in range(9):
                if i in [0,3,6]:
                    t.setPixel(i, [j, 0,0])
                elif i in [1,4,7]:
                    t.setPixel(i, [0, j, 0])
                else:   
                    t.setPixel(i, [0, 0, j])
            t.ser.write(':u\n')
            sleep(.1)
        for j in reversed(range(255)[0::16]):
            for i in range(9):
                if i in [0,3,6]:
                    t.setPixel(i, [j, 0,0])
                elif i in [1,4,7]:
                    t.setPixel(i, [0, j, 0])
                else:   
                    t.setPixel(i, [0, 0, j])
            t.ser.write(':u\n')
            sleep(.1)
except:
    print "CLOSING!!!"
    t.close()
