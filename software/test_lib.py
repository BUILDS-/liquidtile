#!python
##
# test0.py  
# Authors: Christopher J. Woodall <chris.j.woodall at gmail.com>, Daniel E. Cooper <dannyc at bu dot edu>
# 
# Test code which ramps up the r g and b values down
# each column, for use with the loopback adapter. Uses nxn library functionality.
##

import pyLiquidTile
from time import sleep
import sys

t = pyLiquidTile.LiquidTileNxN(0,width=3,height=3, loopback=True)
t.clear()
while(True):
    for i in range(0,255,32):
        t.setColumn(0,(i,i,i))
        t.setRow(0,(255-i,255-i,255-i))
        t.setCell(1,1,(128,128,128))
        t.addToCell(2,2,(1,1,1))
        t.pushFrame()            
        t.update()
        sleep(.1)
