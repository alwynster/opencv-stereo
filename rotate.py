import os
import cv2
import numpy as np

library = 'tsukuba'

if __name__ == '__main__':
	files = os.listdir('%s/left' % library)

	angles = range(-45, 45, 2)

	for f in files:
		fn, ext = os.path.splitext(f)
		
		for a in angles:
			img = cv2.imread('%s/left/%s' % (library, f))
			if img is None: continue
			
			rows, cols, depth = img.shape

			M = cv2.getRotationMatrix2D((cols/2, rows/2), a, 1)
			img2 = cv2.warpAffine(img, M, (cols, rows))
			cv2.imwrite('%s/rotate/%s_%d%s' % (library, fn, a, ext), img2)