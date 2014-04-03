import cv2
import numpy as np

img = cv2.imread('disp_tsukuba_bm_00001.png')
print 'max:', np.max(img)
