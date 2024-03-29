#!/usr/bin/env python2
from analysis import plot_gmm
import matplotlib.pyplot as pp
import Params

__algs__    = ['sad'] # ['bm', 'sad', 'hh', 'var', 'sgbm'] # 'bm',
__algs__    = ['sgbm'] 
save        = False
lib         = 'tsukuba'
training    = None
Params.__article__ = True
if lib == 'kitti':
    limits      = {'bm': (-25,25), 'sgbm': (-25,25), 'hh': (-50, 50), 'var':(-150,100), 'sad':(-75,75)}
else:
    limits      = {'bm': (-5,5), 'sgbm': (-20,20), 'hh': (-50, 50), 'var':(-150,50), 'sad':(-75,75)}

bgn = 1
end = 3
for alg in __algs__:
#    plot_gmm(lib, alg, G=0, draw=not save, show=False, draw_hist=True, xlim=limits[alg], save=save, print_result=False, training=training)
    for i in range(bgn, end+1):
        plot_gmm(lib, alg, i, draw=not save, show=False, draw_hist=True, xlim=limits[alg], save=save)
if not save:
    pp.show()
