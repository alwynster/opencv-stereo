#! /bin/env python2

import numpy as np
import cv2
import matplotlib.pyplot as pp

left_img = 'kitti/left/L_%010d.png'
right_img = 'kitti/right/R_%010d.png'
disp_sgbm_img = 'kitti/output/disp_kitti_sgbm_%05d.png'
disp_bm_img = 'kitti/output/disp_kitti_bm_%05d.png'

top_img = left_img
bot_img = disp_sgbm_img
invert = True
fps = 10.0
start = 0
finish = 150
video = False
limit = 100
fn = 'kitti/video/left_disp_sgbm_crop.%s'

# def top_bottom(top, bottom):
# 	sh1 = top.shape
# 	sh2 = bottom.shape
# 	assert top.dtype == bottom.dtype
# 	assert sh1[1] == sh2[1]
# 	assert sh1[2] == sh2[2]
# 	output = np.zeros((sh1[0]+sh2[0], sh1[1], sh1[2]), dtype=top.dtype)
# 	output[:sh1[0]] = top
# 	output[sh1[0]:] = bottom
# 	return output

if __name__ == '__main__':
	print 'test'
	mx = 255


	if video:
		sh = cv2.imread(top_img % start).shape
		sh = (sh[0] - limit)*2, sh[1], sh[2] 
		writer = cv2.VideoWriter(fn % 'avi', cv2.cv.FOURCC(*'divx'), fps, (sh[1], sh[0]))
		print 'created writer', fn % 'avi'


	for i in range(start, finish+1):
		# print 'frame', i
		top = cv2.imread(top_img % i)

		top = top[limit:]
		bottom = cv2.imread(bot_img % i)
		bottom = bottom[limit:]

		bottom[np.where(bottom == 0)] = 255

		if invert:
			bottom_inv = np.zeros_like(bottom, dtype='float32')
			bottom_inv = 1 - bottom / 255.
			bottom = (bottom_inv * 255).astype(top.dtype)
			
		if video:
			writer.write(np.vstack((top, bottom)))
		else:
			cv2.imshow('img', np.vstack((top, bottom)))
			if cv2.waitKey(int(1000./fps)) == 1048603:
				break
