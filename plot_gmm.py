from analysis import plot_gmm
import matplotlib.pyplot as pp

__algs__    = ['sad'] # ['bm', 'sad', 'hh', 'var', 'sgbm'] # 'bm',
__algs__    = ['sgbm'] 
save        = True
limits      = {'bm': (-50,50), 'sgbm': (-50,50), 'hh': (-50, 50), 'var':None, 'sad':(-75,75)}

bgn = 1
end = 3
for alg in __algs__:
    plot_gmm('kitti', alg, G=0, draw=not save, show=False, draw_hist=True, xlim=limits[alg], save=save, print_result=False)
    for i in range(bgn, end+1):
        plot_gmm('kitti', alg, i, draw=not save, show=False, draw_hist=True, xlim=limits[alg], save=save)
if not save:
    pp.show()