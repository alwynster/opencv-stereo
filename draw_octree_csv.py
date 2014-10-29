#!/bin/env python2

import sys
import numpy as np
import cv2
import math

if len(sys.argv) != 3 and len(sys.argv) != 4 and len(sys.argv) != 5:
    print "USAGE: ./draw_octree_csv octree.csv image [height] [thickness]"
    sys.exit()
    
minx = maxx = miny = maxy = res = 0.0
height = None
thickness = None
if len(sys.argv) > 3:
    height = float(sys.argv[3])
if len(sys.argv) > 4:
    thickness = float(sys.argv[4])
    
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
            if thickness is None:
                if abs(dat[2] - height) > dat[3]:
                    add = False
            else:
                if abs(dat[2] - height) > thickness:
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
#     x, y = int(x, int(y)
    
    # if img[y,x] < val:
#     xp = math.exp(val)
    sz = (size/res)
    img[round(y-sz/2):round(y+sz/2), round(x-sz/2):round(x+sz/2)] += val # xp / (1 + xp)
#     img[y-sz/2:y+sz/2, x-sz/2:x+sz/2] = xp / (1 + xp)
#     img[y, x] = xp / (1 + xp)
        
xp = np.exp(img)
img = xp / (1+xp)
print 'Writing image', sys.argv[2]
imgout = np.array(img)
imgout *= 255
imgout = imgout.astype('uint8')
cv2.imwrite(sys.argv[2], imgout)
# cv2.imshow('img', xp / (1+xp))
# cv2.waitKey()