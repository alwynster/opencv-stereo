import cv2
import numpy as np
import images
import random
import datetime

lib = 'tsukuba'
algs = 'bm', 'sgbm', 'hh', 'var', 'sad'

begin = 750
end = 750

p = 0.95
v = 0.4
m = 3
N = int(np.log(1 - p)/np.log(1-(1-v)**m))
thres = 3

pyrdwn = False

def _ransac(values):
    values = np.array(values)
    values = values[np.where(values != 0)]

    if len(values) < m:
        return 0
    
    average = np.average(values)
    for k in range(N):
        selected = random.sample(values, m)
        
        avg = np.average(np.array(selected))
        
        inl = (np.abs(values - avg) < thres)
        
        if np.sum(inl) >= m:
            values = np.array(values)
            a = np.average(values[np.where(inl)])
            return int(a)
    return 0
    
def invert(arr):
    return np.ones_like(np.array(arr)) * 255 - arr

def ransac(images, keys):
    print 'starting ransac'
    n = 3

    output = np.zeros_like(images[keys[0]])
    shape = output.shape
    print 'shape', shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            dat = list()
            for key in keys:
                dat.append(images[key][i, j])

            output[i, j] = _ransac(dat)

    return output

if __name__ == '__main__':
    for frame in range(begin, end+1):
        print 'frame %d' % frame
        img = dict()
        sample = images.fetch_disp(algs[0], 1, lib=lib)
        if pyrdwn:
            sample = cv2.pyrDown(sample)
        avg = np.zeros_like(np.average(sample, axis=2))
        for alg in algs:
            disp = images.fetch_disp(alg, frame, lib=lib)
            if pyrdwn: disp = cv2.pyrDown(disp)
            img[alg] = np.average(disp, axis=2)
            if img[alg] is None:
                raise Exception("Could not open frame %d of alg %s in library %s" % (frame, alg, lib))
            
            avg += img[alg] / len(algs)

        print "processing output"

        output = ransac(img, algs)

#        cv2.imshow('bm', images.drawable(img['bm']))
#        cv2.imshow('output', images.drawable(output))
#        cv2.waitKey(1)

        one = img[algs[0]]
        two = img[algs[1]]
        thr = img[algs[2]]
        fou = img[algs[3]]
        fiv = img[algs[4]]
        left =  images.top_and_bottom(images.top_and_bottom(one,two),  thr)
        right = images.top_and_bottom(images.top_and_bottom(fou, fiv), output)
        full = images.side_by_side(left, right)
        full = cv2.resize(full, (1920, 1080))

        print "displaying"
        cv2.imshow('disp', invert(full))
        cv2.waitKey()
       
    print 'done'
        
