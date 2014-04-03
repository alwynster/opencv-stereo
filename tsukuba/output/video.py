import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pp

base_base = "disp_tsukuba_%s_"
algs = ("bm", "sgbm", "var", "hh")

img = cv2.imread(base_base % "bm" + "00001.png")
shape = (int(np.shape(img)[0]), int(np.shape(img)[1]))

max_disp = 16*6
factor = (255.0/(max_disp * 16)) * 16;

print "starting..."
for alg in algs:
    writer = cv2.VideoWriter()
    shape = (640, 480)
    writer.open(base_base % alg + ".avi", cv2.cv.CV_FOURCC('I', 'Y', 'U', 'V'), 25.0, shape)

    for i in range(1, 1801):
        img = cv2.imread(base_base % alg + "%05d" % i + ".png")
        img = (img / factor).astype('uint8')
        
        writer.write(img)

    print "done with " + alg

print "done"

