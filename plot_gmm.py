from analysis import plot_gmm
import matplotlib.pyplot as pp

__algs__ = ['bm', 'sad', 'hh', 'var', 'sgbm']

bgn = 1
end = 2
for alg in __algs__:
    for i in range(bgn, end+1):
        plot_gmm('kitti', alg, i, draw=True, show=False, draw_hist=True)
pp.show()
