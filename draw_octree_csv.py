#!/bin/env python2

import sys
import numpy as np
import cv2
import math

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print "USAGE: ./draw_octree_csv octree.csv [height]"
    sys.exit()
    
minx = maxx = miny = maxy = res = 0.0
height = None
if len(sys.argv) == 3:
    height = float(sys.argv[2])
    
filename = sys.argv[1]
f = open(filename)
data = list()
for line in f:
    spl = line[:-1].split(",")
    # first line
    if res == 0:
        minx, maxx, miny, maxy, res = np.array(spl).astype('float')
    else:
        add = True
        dat = np.array(spl).astype('float')
        if height is not None:
            if abs(dat[2] - height) > dat[3]:
                add = False
            
        if add:
            data.append(dat)
    
img = np.zeros(((maxy - miny) / res, (maxx - minx) / res), dtype='float')

for dat in data:
    x, y, z, size, val = dat
    x -= minx
    y -= miny
    x /= res
    y /= res
    x, y = int(x), int(y)
    
    # if img[y,x] < val:
#     xp = math.exp(val)
    img[y:y+(size/res), x:x+(size/res)] = val # xp / (1 + xp)
        
xp = np.exp(img)
cv2.imshow('img', xp / (1+xp))
cv2.waitKey()