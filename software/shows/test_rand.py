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
import random

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
        t.setPixel(random.randint(0,8), [random.randint(0,0xff), random.randint(0,0xff),random.randint(0,0xff)])
        t.update()
        sleep(.1)
except:
    print "CLOSING!!!"
    t.close()
