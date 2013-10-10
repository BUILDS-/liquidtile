#!python
##
# test0.py  
# Authors: Christopher J. Woodall <chris.j.woodall at gmail.com>, Daniel E. Cooper <dannyc at bu dot edu>
# 
# Test code which ramps up the r g and b values down
# each column, for use with the loopback adapter.
##

import pyLiquidTile
from time import sleep
import sys

t = pyLiquidTile.LiquidTile3x3(0, loopback=True)
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
