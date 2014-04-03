import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pp
import images
import time
import datetime
from timer import timer
import os
from hist import hist

__analysis__ = True
__library__ = 'tsukuba'
__begin__ = 1
__end__ = 1800
__bin__ = {'var': 150, "bm": 50, "hh": 50, "sad": 96, "sgbm": 50 }
__fps__ = {'kitti': 10.0, 'tsukuba': 25.0}

def execute(algs):
    # fetch shape of images
    img = images.fetch_disp("bm", 1, __library__)
    sh = (int(np.shape(img)[0]), int(np.shape(img)[1]))
    print sh
    shape = (1080, 1920)

    # check if ground is available
    img = images.fetch_ground(1, __library__)
    ground_avail = img is not None

    if ground_avail:
        # shape = list(np.array(shape) * 2)
        shape = (shape[0], shape[1])
    else:
        shape = (shape[0], shape[1] * 2)

    # for last in np.concatenate((np.array(range(100, __end__, 100)), [__end__])):

    
    print "starting..."
    writer = dict()
    overalls = dict()
    completeness = dict()
    ymax = dict()
    
    for alg in algs:
        bins = range(-__bin__[alg],__bin__[alg])
    
        writer[alg] = cv2.VideoWriter()
        overalls[alg] = np.zeros((__bin__[alg]*2-1,), dtype='float32')
        completeness[alg] = 0.
        ymax[alg] = -1
        if __analysis__:
            shape = shape[1], shape[0]
            fn = __library__ + "/video/analysis %s.avi" % alg
            if True:#not os.path.exists(fn):
                writer[alg].open(fn, cv2.cv.CV_FOURCC('I', 'Y', 'U', 'V'), __fps__[__library__], shape)
            else:
                writer[alg] = None
        else:
            writer[alg].open(__library__ + "/video/output %s.avi" % alg, cv2.cv.CV_FOURCC('I', 'Y', 'U', 'V'), __fps__[__library__], shape)

    global __begin__
    global __end__

    tm = timer(__begin__, __end__)
    mx = 0

    for i in range(__begin__, __end__+1):
        left = images.fetch_orig(i, __library__)
        ground = images.fetch_ground(i, __library__)
        #if ground is not None:
        #    top = images.side_by_side(orig, ground)
        #else:
        #    top = orig
        for alg in algs:
            disp = images.fetch_disp(alg, i, __library__)
            bins = range(-__bin__[alg],__bin__[alg])
            
            #if writer[alg] is None:
            #    continue
        
            if disp is not None and ground_avail:
                if len(disp.shape) == 3:
                    disp = disp[:,:,0]
                if len(ground.shape) == 3:
                    ground = ground[:,:,0]
                diff = ((ground * 1.) - (disp * 1.))

                # exclude not calculated
                # diff[disp == 0]     = 0
                # diff[ground == 0]   = 0
                # exclude incalculable values
                diff_flat = diff[np.where(ground < __bin__[alg])]
                disp_flat = disp[np.where(ground < __bin__[alg])]
                flat_ground = ground[np.where(ground < __bin__[alg])]

                diff_flat = diff_flat[np.where(disp_flat != 0)]
                flat_ground = flat_ground[np.where(disp_flat != 0)]
                diff_flat = diff_flat[np.where(flat_ground != 0)]
                
                top = images.side_by_side(left, np.abs(disp).astype('uint8'))
                
                if __analysis__:
                    flat = disp.flatten()
                    
                    p = np.size(np.nonzero(flat)) / float(np.size(flat)) * 100.
                    pp.figure(figsize=(sh[1]/80, sh[0]/80), dpi=80)
                    pp.title('Histogram of errors (%d%% completeness)' % (p))
                    pp.xlabel('Error')
                    pp.ylabel('Norm occurances')
                    # diff_flat = diff.flatten()
                    # count, bins = np.histogram(diff, bins=bins, normed=True)
                    # n, bins, patches = pp.hist(diff, bins=range(-96, 96, 10), normed=True)

                    neg_c, neg_b, pos_c, pos_b = hist(diff_flat.astype('int32'))
                    bns = np.concatenate((neg_b[::-1], pos_b))
                    cnt = np.concatenate((neg_c[::-1], pos_c))
                    cnt = (cnt / float(np.sum(cnt))).astype('float32')
                    
                    count = np.zeros(np.array(bins[:-1]).shape, dtype='float32')
                    offset = bns[0] - bins[0]
                    try:
                        if offset < 0:
                            cnt = cnt[-offset:]
                            bns = bns[-offset:]
                            count[:len(cnt)] = cnt
                        else:
                            if (len(bins) - len(bns) - offset -1) > 0:
                                count[offset:-(len(bins) - len(bns) - offset - 1)] = cnt
                            else:
                                count[offset:] = cnt
                        
                    except ValueError:
                        print 'alg', alg
                        print 'frame', i
                        print 'Skip frame'
                        print bins
                        print bns
                        raw_input()
                    

                    if ymax[alg] == -1: ymax[alg] = np.max(count) * 1.75

                    if np.average(count) == 0.0:
                        print "no count"
                        print cnt
                        print count
                        print bns
                        print bins
                        print offset
                        # raw_input()
                    # count[np.where(count == neg_b)] = neg_c
                    # count[np.where(count == pos_c)] = pos_c
                    pp.bar(bins[:-1], count, width=1.0)

                    # overalls[alg] = np.concatenate((overalls[alg], diff_flat))
                    overalls[alg] = (i * overalls[alg] + count) / (i+1)

                    pp.xlim([-__bin__[alg], __bin__[alg]])
                    pp.ylim([0, ymax[alg]])
                    pp.gray()
                    pp.savefig('tmp/tmp.png', bbox_inches=0)
                    pp.cla()
                    pp.close()
                    diff_img = cv2.imread('tmp/tmp.png')
                    diff_img = images.resize(diff_img, np.shape(diff))

                    completeness[alg] = (i * completeness[alg] + p) / (i+1)
                    
                    pp.figure(figsize=(sh[1]/80, sh[0]/80), dpi=80)
                    pp.title('Overall histogram of errors (%d%% completeness)' % int(completeness[alg]))
                    pp.xlabel('Error')
                    pp.ylabel('Norm occurances')
                    
                    #neg_c, neg_b, pos_c, pos_b = hist(overalls[alg].astype('int32'))
                    #bins = np.concatenate((neg_b, pos_b))
                    #count = np.concatenate((neg_c, pos_c))
                    pp.bar(bins[:-1], overalls[alg], width=1.0)
                    # n, bins, patches = pp.hist(images.remove_zero(overalls[alg]), bins=range(-96, 96, 10), normed=True)
                    
                    pp.xlim([-__bin__[alg], __bin__[alg]])
                    pp.ylim([0, ymax[alg]])
                    pp.gray()
                    pp.savefig('tmp/tmp.png', bbox_inches=0)
                    pp.cla()
                    pp.close()
                    overall_diff_img = cv2.imread('tmp/tmp.png')
                    overall_diff_img = images.resize(overall_diff_img, np.shape(diff))
                    
                    bottom = images.side_by_side(diff_img, overall_diff_img)
                else:
                    bottom = images.side_by_side(disp, diff)

            else:
                bottom = disp

            
            '''
            top = images.side_by_side(left, disp)
        
            diff = np.array(np.abs(((ground * 1.) - (disp * 1.))), dtype=ground.dtype)

            # exclude not calculated
            diff[disp == 0] = 0
            diff[ground == 0] = 0
            # exclude incalculable values
            # diff[ground > 16*6] = 0

            bottom = images.side_by_side(ground, diff)
            '''
            
            output = images.top_and_bottom(top, bottom)
            newi = images.resize(output, (1080, 1920))
            writer[alg].write(images.drawable(newi, inv=False)) 
        tm.progress(i)

    pp.close('all')
    print "done"

if __name__ == "__main__":
    algs = ["hh", "var", "bm", "sad", "sgbm"] # "var", "bm", "hh", "sad", "sgbm"
    execute(["hh", "var", "bm", "sad", "sgbm"])
    execute(["var"])
    execute(["sad"])
    
