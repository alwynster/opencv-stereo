'''
Created on 01 Nov 2014

@author: alwynster
'''

import numpy as np
import cv2
import math
import sys
import os

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

if len(sys.argv) != 3 and len(sys.argv) != 4:
    print "USAGE: compare_octree_csv.py correct_tree.csv compare_tree.csv [height]"
    sys.exit()

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
    pt = data_point(np.array(dat).astype('float'))
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
                            differences.append((point2.val - point.val) / num)
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

file = '%s_%s.npz' % (file1, file2)
print
print 'saving', file
np.savez(file, diffs=np.array(differences))

