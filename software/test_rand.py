#!python
##
# test0.py  
# Authors: Christopher J. Woodall <chris.j.woodall at gmail.com>
# 
# Test code which ramps up the r g and b values down
# each column.
##

import pyFireTile
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

print port
t = pyFireTile.FireTile3x3(port)
t.open()
t.clear()

try:
    while 1:
	t.setPixel(random.randint(0,9), [random.randint(0,255), random.randint(0,255),random.randint(0,128)])
	t.update()
        sleep(.1)
except:
    print "CLOSING!!!"
    t.close()
