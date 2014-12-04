#!/usr/bin/env python2

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

__library__ = 'kitti'
__algs__ = ['var'] #var bm sgbm sad hh
__G__ = range(4,10)
__timer__ = True
__dbg__ = False
__begin__ = 1
__end__ = 101
__dtype__ = 'float32'
__save_data_only__ = False
limit = None

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
        # print shape
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

        found_count = 0
        full_count = 0
#        cv2.imshow('1',  images.fetch_disp(alg, 1, __library__))
#        cv2.imshow('1b', (images.fetch_ground(1, __library__).astype('float') - images.fetch_disp(alg, 1, __library__)[:,:,0].astype('float')).astype('uint8'))
#        cv2.imshow('2',  images.fetch_disp(alg, 2, __library__))
#        cv2.imshow('2b', (images.fetch_ground(2, __library__).astype('float') - images.fetch_disp(alg, 2, __library__)[:,:,0].astype('float')).astype('uint8'))
        cv2.waitKey()
        if __save_data_only__:
            print 'fetching data'
	    print __library__
            for i in range(__begin__, __end__ + 1):
                orig = images.fetch_orig(i, __library__)
                ground = images.fetch_ground(i, __library__)
                disp = images.fetch_disp(alg, i, __library__)
                
#                cv2.imshow('disp', disp)
#                cv2.imshow('diff', (ground.astype('float') - disp[:,:,0].astype('float')).astype('uint8'))
#                cv2.waitKey()

		if orig is None: print 'orig is None'
		if ground is None: print 'ground is None'
		if disp is None: print 'disp is None'
		
                if disp is not None and ground_avail:
                    if len(disp.shape) == 3: disp = disp[:,:,0]
                    
                    diff = ((ground.astype(__dtype__)) - (disp.astype(__dtype__))).astype(__dtype__)
                    full_count += np.product(diff.shape)
		    

                    # exclude not calculated
                    flat = diff[np.where(disp != 0)]
                    flat_ground = ground[np.where(disp != 0)]
                    flat = flat[np.where(flat_ground != 0)]

		    found_count += len(np.nonzero(flat.flatten())[0])
                    
                    # exclude incalculable values
                    # diff[ground > 16*6] = 0

                    diff = np.array(diff, dtype=__dtype__)

                    overall_diff = np.concatenate((overall_diff, flat))

                    if file_count == max_count:
			print 'saving', '%s/data/data_%s_%d.npz' % (lib, alg, file_num), i
                        np.savez('%s/data/data_%s_%d.npz' % (lib, alg, file_num), data=overall_diff)
                        overall_diff = np.array([], dtype=__dtype__)
                        
                        file_count = 1
                        file_num += 1
                    else:
                        file_count += 1
        
                if __timer__:
                    tm.progress(i)
        
            print 'found', found_count, 'of', full_count
	    
        if full_count != 0:
	            print float(found_count) / full_count * 100.0 
#             np.savez('%s/data/data_%s_%d.npz' % (lib, alg, file_num), data=overall_diff)
            
    if __save_data_only__: return

    data_files = list()
    total = __end__ - __begin__ + 1
    # range(int(math.ceil(total / float(max_count))))
    
    for g in __G__:
        print
        print 'calculating for G =', g
        for alg in __algs__:
            print 'Calculating for alg', alg

            data_files = ['%s/data/data_%s_%d.npz' % (lib, alg, i) for i in range(0, int(math.floor((__end__ - __begin__) / 10.)))]
            print data_files
            # data_files = ['%s/data/data_%s_%d.npz' % (lib, alg, i) for i in range(int(__begin__ / 10.), int(math.ceil(__end__ / 10.)))]
        #if __library__ == 'tsukuba': # data_files=data_files[:-1]
            print 'creating model'
            model = gmm(data_files, debug=__dbg__, history=True, timer=__timer__, limit=limit)
            model.fit_model(g)
            model.save_results(library=__library__, alg=alg, hist=True)
            # model.draw_results()
            print "END TIME ", str(datetime.datetime.now())
            print "TIME PASSED", str(datetime.datetime.now() - start)
            print
            # pp.show()

        print "done"

def plot_gmm(lib=__library__, alg=__algs__[0], G=1, draw=True, show=True, draw_hist=True, save=False, xlim=None, print_result=True, training=True):
#    part = 'training' if training else 'testing'
#    if G == 0:
#        model = gmm(texts = True, gmm_txt='%s/%s/gmm_%s_%d.npz' % (lib, part, alg, G+1), hist_txt=('%s/%s/hist_%s_%d.npz' % (lib, part, alg, G+1)))
#    else:
#        model = gmm(texts = True, gmm_txt='%s/%s/gmm_%s_%d.npz' % (lib, part, alg, G), hist_txt=('%s/%s/hist_%s_%d.npz' % (lib, part, alg, G)))

    if G == 0:
        model = gmm(texts = True, gmm_txt='%s/gmm_%s_%d.npz' % (lib, alg, G+1), hist_txt=('%s/hist_%s_%d.npz' % (lib, alg, G+1)))
    else:
        model = gmm(texts = True, gmm_txt='%s/gmm_%s_%d.npz' % (lib, alg, G), hist_txt=('%s/hist_%s_%d.npz' % (lib, alg, G)))
    x = model.bins
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
#        images.save_latex(x, y, leg, '%s_%s_gmm_%s_%s' % (lib, part, alg, G_code), 'Error', 'Relative weight', 0.48, xlim=xlim, model=model, ylim=None)
        images.save_latex(x, y, leg, '%s_tmp_gmm_%s_%s' % (lib, alg, G_code), 'Error', 'Relative weight', 0.48, xlim=xlim, model=model, ylim=None)
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
 
if __name__ == "__main__":
    __save_data_only__ = True    
    execute()
    __save_data_only__ = False    
    execute()
