#!/bin/env python2
'''
Created on 01 Nov 2014

@author: alwynster
'''
import matplotlib.pyplot as pp
import numpy as np
import sys
import images

if len(sys.argv) != 3:
    print "USAGE: plot_diffs.py diffs.npz outfile"
    sys.exit()
    
data = np.load(sys.argv[1])
diffs = data['diffs']

count, x, patches = pp.hist(diffs)

print x
print count

images.save_latex(x[:-1], count, None, sys.argv[2], ylim=None, bar=True)