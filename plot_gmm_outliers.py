import matplotlib.pyplot as pp
import numpy as np
from gmm import gmm
import images

__algs__    = ['sgbm'] 
save        = True
lib         = 'tsukuba'
if lib == 'kitti':
    limits      = {'bm': (-25,25), 'sgbm': (-25,25), 'hh': (-50, 50), 'var':(-150,100), 'sad':(-75,75)}
else:
    limits      = {'bm': (-5,5), 'sgbm': (-80,100), 'hh': (-50, 50), 'var':(-150,50), 'sad':(-75,75)}


def plot_gmm(lib, alg=__algs__[0], G=1, draw=True, show=True, draw_hist=True, save=False, xlim=None, print_result=True):
    if G == 0:
        model = gmm(texts = True, gmm_txt='%s/gmm_%s_%d.npz' % (lib, alg, G+1), hist_txt=('%s/hist_%s_%d.npz' % (lib, alg, G+1)))
    else:
        model = gmm(texts = True, gmm_txt='%s/gmm_%s_%d.npz' % (lib, alg, G), hist_txt=('%s/hist_%s_%d.npz' % (lib, alg, G)))
    x = model.bins
    
    model.count[range(np.where(x == -5)[0][0], np.where(x == 5)[0][0]+1)] = 0
    bin_width = x[1] - x[0]
    x = np.linspace(model.bins[0], model.bins[-1], num=10000)

    y = None        
    if G != 0:
        y = [model.pdf_integral(xi - bin_width/2., xi + bin_width/2.) for xi in x]
    
    abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    G_code = abc[G]
    if G != 0:
        leg = ['Error hist', 'GMM'][::-1]
    else:
        leg = ['Error hist']
    if save:
        leg = ['\ss{%s}' % l for l in leg]
#         if G == 0: leg = None
        images.save_latex(x, y, leg, '%s_gmm_%s_%s_outliers' % (lib, alg, G_code), 'Error', 'Relative weight', 0.48, xlim=xlim, model=model, ylim=None)
    if draw:
        if draw_hist:
            pp.figure()
            pp.bar(model.bins[:-1], model.count)
            pp.hold(True)
        if xlim is not None:
            pp.xlim(xlim)
        
        # pp.stem(x, y, markerfmt='xr', linefmt='r-')
        if G != 0:
            pp.plot(x, y, color='r', linewidth=3)

#         if draw_hist:
#             model.draw_hist(fig=True, limit_hist=False)
#         pp.hold()
#         pp.title("%s - %d gmm" % (alg, G))
#         model.draw_gmm_hist(fig=False)
#         
#         if draw_hist:
#             pp.legend(['Histogram', 'GMM'])
            
    print lib, alg, G
    if print_result: model.print_results()
    if show:
        pp.show()
        
if __name__ == '__main__':
    bgn = 1
    end = -1
    for alg in __algs__:
        plot_gmm(lib, alg, G=0, draw=not save, show=False, draw_hist=True, xlim=limits[alg], save=save, print_result=False)
    if not save:
        pp.show()
