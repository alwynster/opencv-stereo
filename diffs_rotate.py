import os
import cv2
import numpy as np

library = 'tsukuba'

if __name__ == '__main__':
	gt = cv2.imread('%s/tsukuba_disparity_L_00001.png' % library)
	
	files = os.listdir('%s/rotate/output/' % library)
	# angles = range(-45, 45, 2)
	for f in files:
		print f
		img = cv2.imread('%s/rotate/output/%s' % (library, f)).astype('float')
		if not (('var' in f) or ('sad' in f)):
			factor = 255.0/(16*6*16) * 16
			img /= factor
	
		if img is not None:
			diff = np.abs(img - gt)
			diff[np.where(img == 0)] = 0
			diff[np.where(gt == 0)] = 0
			
			diff = diff.astype('uint8')

			# cv2.imshow('gt', gt)
			# cv2.imshow('img', img.astype('uint8'))
			# cv2.imshow('diff', diff)

			print 'diff/%s' % f
			cv2.imwrite('%s/diff/rotate/%s' % (library, f), np.ones_like(diff) * 255 - diff)
			# cv2.waitKey()