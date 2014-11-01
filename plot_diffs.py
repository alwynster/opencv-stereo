#!/bin/env python2
'''
Created on 01 Nov 2014

@author: alwynster
'''
import matplotlib.pyplot as pp
import numpy as np
import sys
import images

if len(sys.argv) != 3 and len(sys.argv) != 2:
    print "USAGE: plot_diffs.py diffs.npz [outfile]"
    sys.exit()
    
data = np.load(sys.argv[1])
diffs = data['diffs']
print diffs.shape
# diffs = diffs[np.where(diffs != 0)]
# print diffs.shape
bns = np.linspace(-1, 1, 20)

count, x, patches = pp.hist(diffs, bins=bns)

count = count / float(diffs.shape[0])

if len(sys.argv) == 2:
    pp.bar(x[:-1] + (x[1]-x[0])*0, count, width=x[1]-x[0])
    pp.show()
else:
    images.save_latex(x[:-1] - (x[1]-x[0])/2.0*0, count, None, sys.argv[2], xlabel='difference in \pmizt', ylabel='histogram', ylim=(0,1), bar=True, xlim=(x[0], x[-1]), width=0.3, yticks=None)
