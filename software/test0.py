#!python
##
# test0.py  
# Authors: Christopher J. Woodall <chris.j.woodall at gmail.com>
# 
# Test code which ramps up the r g and b values down
# each column.
##

import pyLiquidTile
from time import sleep
import sys

if len(sys.argv) == 1:
    print "useage: test0.py <serial-port>"
    sys.exit(0)
elif len(sys.argv) == 2:
    port = sys.argv[1]
else:
    print "useage: test0.py <serial-port>"
    sys.exit(0)

loopback = False
if port == "loopback":
    loopback=True

t = pyLiquidTile.LiquidTile3x3(port, loopback=loopback)
    
t.clear()

try:
    while 1:
        for j in (range(255)[0::8]):
            for i in range(9):
                if i in [0,3,6]:
                    t.setPixel(i, [j, 0,0])
                elif i in [1,4,7]:
                    t.setPixel(i, [0, j, 0])
                else:   
                    t.setPixel(i, [0, 0, j])
            t.update()
            sleep(.1)
        for j in reversed(range(255)[0::16]):
            for i in range(9):
                if i in [0,3,6]:
                    t.setPixel(i, [j, 0,0])
                elif i in [1,4,7]:
                    t.setPixel(i, [0, j, 0])
                else:   
                    t.setPixel(i, [0, 0, j])
            t.update()
            sleep(.1)
except:
    print "CLOSING!!!"
    t.close()
