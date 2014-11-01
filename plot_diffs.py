#!/bin/env python2
'''
Created on 01 Nov 2014

@author: alwynster
'''
import matplotlib.pyplot as pp
import numpy as np
import sys

if len(sys.argv) != 2:
    print "USAGE: plot_diffs.py diffs.npz"
    sys.exit()
    
data = np.load(sys.argv[1])
diffs = data['diffs']

pp.hist(diffs)
pp.show()
