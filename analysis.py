from gmm import gmm
import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pp
import images
import time
import datetime
from timer import timer
import math

__library__ = 'tsukuba'
__algs__ = ['bm', 'sad', 'hh', 'var', 'sgbm'] #var bm sgbm sad hh
__G__ = range(1,4)
__timer__ = True
__dbg__ = False
__begin__ = 1
__end__ = 1800
__dtype__ = 'float32'
__save_data_only__ = True

def execute(lib=__library__):
    start = datetime.datetime.now()
    print "START TIME", str(start)
    
    # fetch shape of images
    img = images.fetch_disp("bm", 1, __library__)
    sh = (int(np.shape(img)[0]), int(np.shape(img)[1]))
    shape = (1080, 1920)

    # check if ground is available
    img = images.fetch_ground(1, __library__)
    ground_avail = img is not None

    if ground_avail:
        # shape = list(np.array(shape) * 2)
        shape = (shape[0], shape[1])
    else:
        print shape
        shape = (shape[0], shape[1] * 2)

    print "starting..."
    
    global __begin__
    global __end__

    for alg in __algs__:
        if __timer__:
            tm = timer(__begin__, __end__)
        mx = 0

        overall_diff = np.array([], dtype=__dtype__)
        file_num = 0
        file_count = 0
        max_count = 10

        
        if __save_data_only__:
            print 'fetching data'
            for i in range(__begin__, __end__ + 1):
                orig = images.fetch_orig(i, __library__)
                ground = images.fetch_ground(i, __library__)

                disp = images.fetch_disp(alg, i, __library__)

                if disp is not None and ground_avail:
                    diff = ((ground.astype(__dtype__)) - (disp.astype(__dtype__))).astype(__dtype__)

                    # exclude not calculated
                    flat = diff[np.where(disp != 0)]
                    flat_ground = ground[np.where(disp != 0)]
                    flat = flat[np.where(flat_ground != 0)]
                    # exclude incalculable values
                    # diff[ground > 16*6] = 0

                    diff = np.array(diff, dtype=__dtype__)

                    # diff = diff[:, :, 0].flatten()
                    # diff = diff[np.where(diff != 0)]
                    overall_diff = np.concatenate((overall_diff, flat))

                    if file_count == max_count:
                        np.savez('%s/data/data_%s_%d.npz' % (lib, alg, file_num), data=overall_diff)
                        overall_diff = np.array([], dtype=__dtype__)
                        
                        file_count = 1
                        file_num += 1
                    else:
                        file_count += 1

                if __timer__:
                    tm.progress(i)

            np.savez('%s/data/data_%s_%d.npz' % (lib, alg, file_num), data=overall_diff)
            
    if __save_data_only__: return

    data_files = list()
    total = __end__ - __begin__ + 1
    # range(int(math.ceil(total / float(max_count))))
    
    for g in __G__:
        print
        print 'calculating for G =', g
        for alg in __algs__:
            print 'Calculating for alg', alg

            data_files = ['%s/data/data_%s_%d.npz' % (lib, alg, i) for i in range(10)]

            print 'creating model'
            model = gmm(data_files, debug=__dbg__, history=True, timer=__timer__)
            model.fit_model(g)
            model.save_results(library=__library__, alg=alg, hist=True)
            # model.draw_results()
            print "END TIME ", str(datetime.datetime.now())
            print "TIME PASSED", str(datetime.datetime.now() - start)
            print
            # pp.show()

        print "done"

def plot_gmm(lib=__library__, alg=__algs__[0], G=1, draw=True, show=True, draw_hist=True):
    model = gmm(texts = True, gmm_txt='%s/gmm_%s_%d.npz' % (lib, alg, G), hist_txt=('%s/hist_%s_%d.npz' % (lib, alg, G)))
    if draw:
        if draw_hist:
            model.draw_hist(fig=True)
        pp.hold()
        pp.title("%s - %d gmm" % (alg, G))
        model.draw_gmm_hist(fig=False)
    model.print_results()
    if show:
        pp.show()
 

if __name__ == "__main__":
    
    execute()
