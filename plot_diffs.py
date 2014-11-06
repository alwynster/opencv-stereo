#!/bin/env python2
'''
Created on 01 Nov 2014

@author: alwynster
'''
import matplotlib.pyplot as pp
import numpy as np
import sys
import images

def plot_diffs(diffs, outfile=None, ylim=None, yticks=None):
    
    print diffs.shape
    # diffs = diffs[np.where(diffs != 0)]
    # print diffs.shape
    bns = np.linspace(-1, 1, 20)
    
    count, x, patches = pp.hist(diffs, bins=bns)
    
    count = count / float(diffs.shape[0])
    
    if outfile is None:
        pp.bar(x[:-1] + (x[1]-x[0])*0, count, width=x[1]-x[0])
        pp.show()
    else:
        images.save_latex(x[:-1] - (x[1]-x[0])/2.0*0, count, None, outfile, xlabel='difference in \pmizt', ylabel='histogram', ylim=ylim, bar=True, xlim=(x[0], x[-1]), width=0.25, yticks=yticks, yfactor=1.5)


if __name__ == '__main__':
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        print "USAGE: plot_diffs.py diffs.npz [outfile]"
        sys.exit()
    
    data = np.load(sys.argv[1])
    diffs = data['diffs']
    if len(sys.argv) > 2:
        plot_diffs(diffs, outfile=sys.argv[2])
    else:
        plot_diffs(diffs)
