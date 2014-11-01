#!/bin/env python2

import sys
import numpy as np
import cv2
import math

if len(sys.argv) != 3 and len(sys.argv) != 4 and len(sys.argv) != 5 and len(sys.argv) != 6 and len(sys.argv) != 7:
    print "USAGE: ./draw_octree_csv octree.csv image [height] [thickness] [draw_factor] [ideal_mode]"
    sys.exit()
    
minx = maxx = miny = maxy = res = 0.0
height = None
thickness = None
draw_factor = None
ideal_mode = False
if len(sys.argv) > 3:
    height = float(sys.argv[3])
if len(sys.argv) > 4:
    thickness = float(sys.argv[4])
if len(sys.argv) > 5:
    draw_factor = float(sys.argv[5])
else:
    draw_factor = 1.0
if len(sys.argv) > 6:
    ideal_mode = sys.argv[6] == '1'

print 'draw_factor', draw_factor
print 'ideal_mode', ideal_mode
print 'height', height, thickness
    
filename = sys.argv[1]
f = open(filename)
data = list()
for line in f:
    spl = line[:-1].split(",")
    # first line
    if res == 0:
        minx, maxx, miny, maxy, res = np.array(spl).astype('float')
	print spl
    else:
        add = True
        dat = np.array(spl).astype('float')
        if height is not None:
            if thickness is None or thickness == -1:
                if abs(dat[2] - height) > dat[3]/2.0:
                    add = False
            else:
                if abs(dat[2] - height) > thickness:
                    add = False
            
        if add:
            data.append(dat)
    
img = np.zeros(((maxy - miny) / res * draw_factor, (maxx - minx) / res * draw_factor), dtype='float')

for dat in data:
    x, y, z, size, val = dat
    x -= minx
    y -= miny
    x /= res
    y /= res
    x *= draw_factor
    y *= draw_factor
#     x, y = int(x, int(y)

    if ideal_mode:
	p = math.exp(val)/(1+math.exp(val))
	if p <= 0.45: val = -100
	elif p >= 0.55: val = 100
	else: val = 0
    
    # if img[y,x] < val:
#     xp = math.exp(val)
    sz = (size/res) * draw_factor
    img[round(y-sz/2):round(y+sz/2), round(x-sz/2):round(x+sz/2)] = val # xp / (1 + xp)
#     img[y-sz/2:y+sz/2, x-sz/2:x+sz/2] = xp / (1 + xp)
#     img[y, x] = xp / (1 + xp)
        
xp = np.exp(img)
img = xp / (1+xp)
print 'Writing image', sys.argv[2]
imgout = np.array(img)
imgout = np.ones_like(imgout) - imgout
imgout *= 255
imgout = imgout.astype('uint8')
cv2.imwrite(sys.argv[2], imgout)
# cv2.imshow('img', xp / (1+xp))
# cv2.waitKey()
