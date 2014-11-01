#!/bin/env python2
'''
Created on 01 Nov 2014

@author: alwynster
'''

import numpy as np
import cv2
import math
import sys
import os
import shutil
import matplotlib.pyplot as pp

eps = 1e-3
if len(sys.argv) != 4:
    print "USAGE: compare_octree_csv.py correct_tree.csv compare_tree.csv height"
    sys.exit()

minx = maxx = miny = maxy = res = 0.0

file1 = sys.argv[1]
file2 = sys.argv[2]
height = float(sys.argv[3])

data = list()
for line in open(file1):
    spl = line[:-1].split(",")
    # first line
    if res == 0:
        minx, maxx, miny, maxy, res = np.array(spl).astype('float')
    else:
        add = True
        dat = np.array(spl).astype('float')
        if abs(dat[2] - height) <= dat[3]/2.0:
            data.append(dat)

res = 0
data2 = list()
for line in open(file2):
    spl = line[:-1].split(",")
    # first line
    if res == 0:
        nminx, nmaxx, nminy, nmaxy, res = np.array(spl).astype('float')
        if nminx < minx: minx = nminx
        if nminy < miny: miny = nminy
        if nmaxx > maxx: maxx = nmaxx
        if nmaxy > maxy: maxy = nmaxy
    else:
        dat = np.array(spl).astype('float')
        if abs(dat[2] - height) <= dat[3]/2.0:
            data2.append(dat)

img = np.zeros(((maxy - miny) / res, (maxx - minx) / res), dtype='float')

for dat in data:
    x, y, z, size, val = dat
    x -= minx
    y -= miny
    x /= res
    y /= res

    '''
    p = math.exp(val)/(1+math.exp(val))
    if p <= 0.45: val = -100
    elif p >= 0.55: val = 100
    else: val = 0
    '''
    
    sz = (size/res)
    img[round(y-sz/2):round(y+sz/2), round(x-sz/2):round(x+sz/2)] = val # xp / (1 + xp)


img2 = np.zeros(((maxy - miny) / res, (maxx - minx) / res), dtype='float')

for dat in data2:
    x, y, z, size, val = dat
    x -= minx
    y -= miny
    x /= res
    y /= res

    sz = (size/res)
    img2[round(y-sz/2):round(y+sz/2), round(x-sz/2):round(x+sz/2)] = val # xp / (1 + xp)

img[np.where(img == np.min(img))] = -1000
img2[np.where(img2 == np.min(img2))] = np.min(img)

'''
pp.hist(img.flatten())
pp.figure()
pp.hist(img2.flatten())
pp.show()
'''

xp = np.exp(img)
img = xp / (1+xp)

xp = np.exp(img2)
img2 = xp / (1+xp)

# equalize:
'''
print np.min(img), np.min(img2)
img[np.where(img < 0.5)] = np.min(img2)

pp.hist(img2[:,:].flatten())
pp.show()
'''

'''
cv2.imwrite('a.png', (img * 255).astype('uint8'))
cv2.imwrite('b.png', (img2 * 255).astype('uint8'))
dimg = (img2-img)
cv2.imwrite('c.png', (dimg * 255).astype('uint8'))
'''

# compare:
sh = img.shape
diffs = list()
for i in range(sh[0]):
    for j in range(sh[1]):
        # ignore unknown
        if abs(img2[i, j] - 0.5) < eps:
            continue
        # add from ground
        diff = img2[i, j] - img[i, j]
        if abs(diff) > eps:
            diffs.append(diff)

fn = 'compare/%s_%s.npz' % (file1, file2)
print
print 'saving', fn
np.savez(fn, diffs=np.array(diffs))
try:
    shutil.copyfile(fn, '/copy/%s_%s.npz' % (file1,file2))
except:
    print '',
        
'''

class data_point:
    x, y, z, size, val = None, None, None, None, None
    uses = None
    def __init__(self, array):
        self.x, self.y, self.z, self.size, self.val = array
        self.uses = 0
        # convert val to probability
        xp = math.exp(self.val)
        self.val = xp / (xp + 1)

    def __str__(self):
        return '(%.2f, %.2f, %.2f, %.2f)' % (self.x, self.y, self.y, self.size) 



height = None
file1 = sys.argv[1]
file2 = sys.argv[2]
if len(sys.argv) > 3: height = float(sys.argv[3])

print 'reading', file1
correct_points = list()
for line in open(file1):
    dat = line.split(',')
    pt = data_point(np.array(dat).astype('float'))
    add = True
    if height is not None:
        if abs(pt.z - height) >= pt.size/2.0:
            add = False
    if add: correct_points.append(pt)
    
print 'reading', file2
incorrect_points = list()
for line in open(file2):
    dat = line.split(',')
    dat = np.array(dat).astype('float')
    if dat[4] != 0.5:
        pt = data_point(dat)
        add = True
        if height is not None:
            if abs(pt.z - height) >= pt.size/2.0:
                add = False
        if add: incorrect_points.append(pt)
    
print
print 'finding incorrect points'
# find incorrect point for all correct points
i = None
remove = None
differences = list()
for point in correct_points:
    for i in range(len(incorrect_points)):
        remove = False
        brk = False
        point2 = incorrect_points[i]

        if abs(point.x - point2.x) < point.size / 2.0:
            if abs(point.y - point2.y) < point.size / 2.0:
                if abs(point.z - point2.z) < point.size / 2.0:
                    # same size
                    point.uses += 1
                    if point2.size == point.size:
                        brk = True
                        remove = True
                        differences.append(point2.val - point.val)
                    else:
                        num = (point2.size / point.size) ** 2. # number of cor in inc
                        # check for larger incorrect 
                        if point2.size > point.size:
                            incorrect_points[i].uses += 1
                            remove = incorrect_points[i].uses == num
                            differences.append((point2.val - point.val))
                        else:
                            brk = True
                            remove = True
                            differences.append(point2.val - point.val)
                    if remove:
                        incorrect_points.remove(incorrect_points[i])
                        i -= 1
                    if brk:
                        break
print len(differences), 'diffs'

print
print 'adding rest of incorrect'
# incorrect not existing in correct
for point in incorrect_points:
    differences.append(point.val - 0.5)
print len(differences), 'diffs'

print
print 'adding rest of correct'
for point in correct_points:
    if point.uses == 0:
        differences.append(0.5 - point.val)    
print len(differences), 'diffs'

file = 'compare/%s_%s.npz' % (file1, file2)
print
print 'saving', file
np.savez(file, diffs=np.array(differences))
try:
    shutil.copyfile(file, '/copy/%s_%s.npz' % (file1,file2))
except:
    print '',
'''
