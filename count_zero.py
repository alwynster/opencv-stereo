import cv2
import numpy as np
import matplotlib.pyplot as pp

data = list()

for b in range(5, 50, 2):
    img = cv2.imread("disp_bm_" + str(b) + ".png")

    blk =  np.sum(np.array(img) == 0.0)
    total = np.product(np.array(np.shape(img)))

    data.append(float(blk)/total*100.)


pp.plot(range(5,50, 2), data)
pp.grid()
pp.show()
