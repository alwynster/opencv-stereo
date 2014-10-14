import os
import numpy as np
import cv2
import matplotlib.pyplot as pp

lib = 'tsukuba'
algs = ['bm', 'var', '']
if __name__ == '__main__':
	for alg in algs:
		files = os.listdir('%s/diff/rotate/%s' % (lib, alg))
		values = dict()
		for f in files:
			fn, ext = os.path.splitext(f)
			if '_' not in f: continue
			angle = fn.split('_')[4]
			
			img = cv2.imread('%s/diff/rotate/%s/%s' % (lib, alg, f))
			if len(img.shape) > 2:
				img = img[:,:,0]

			img[np.where(img == 255)] = 0
			values[angle] = np.count_nonzero(img)

		keys = np.array(values.keys()).astype('int')
		vals = np.array(values.values()).astype('int')
		
		pp.scatter(keys, vals)
		np.savez('%s/diff/rotate/%s_scatter.npz' % (lib, alg), keys=keys, vals=vals)
