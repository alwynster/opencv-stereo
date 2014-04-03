import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pp


base_base = "tsukuba_disparity_L_"

img = cv2.imread(base_base + "00001.png")
shape = (int(np.shape(img)[1]), int(np.shape(img)[0]))

print "starting..."
writer = cv2.VideoWriter()
writer.open(base_base + ".avi", cv2.cv.CV_FOURCC('I', 'Y', 'U', 'V'), 25.0, shape)

for i in range(1, 1801):
    img = cv2.imread(base_base + "%05d" % i + ".png")
    writer.write(img)

print "done"

