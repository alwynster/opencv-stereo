import cv2
import numpy as np
import subprocess
import matplotlib.pyplot as pp
from timer import timer

__library__ = 'kitti'
def calculate_disp(min_frame, max_frame, algs):
    block = 5
    base = __library__ + "/"
    digits = 5
    if __library__ == 'tsukuba':
        form = "tsukuba_daylight_%s_%05d"
    elif __library__ == 'kitti':
        form = "%s_%010d"
        
    output_form = "disp_" + __library__ + "_%s_%05d"

    disparities = 16*6

    percent = -1
    total_frames = max_frame - min_frame

    tm = timer(min_frame, max_frame, True)
    for frame in range(min_frame, max_frame+1):
        for alg in algs:
            args = ["OpenCV.exe", base + "left/" + (form % ('L', frame)) + ".png", base + "right/" + (form % ('R', frame)) + ".png", "--algorithm=" + alg, "--max-disparity=" + str(disparities), "--blocksize=" + str(block), "--no-display", "-o", base + "output/" + (output_form % (alg, frame)) + ".png"]
            try:
                subprocess.call(args, shell=True)
            except Error:
                print 'Error in OpenCV program'
                return

        tm.progress(frame)

##    disp = cv2.imread("disp_" + alg + "_" + str(block) + "_" + ("%010d" % frame) + ".png")
##
##    sh = np.shape(disp)
##    print sh, np.shape(disp[:,:,0])
##
##    flat = np.reshape(disp[:, :, 0], (np.product(sh[0:2]))).astype('float')
##    print 'max disp', np.max(flat)
##    pp.subplot(1,2,1)
##    pp.hist(flat)
##
##    factor = (255./(16*3 * 16)) * 16
##    print 'factor', factor
##
##    flat /= factor
##    print 'max disp', np.max(flat)
##    
##    pp.subplot(1,2,2)
##    pp.hist(flat)
##    pp.show()


if __name__ == "__main__":
    start = 0
    end = 394
    calculate_disp(start, end, ["bm", "var", "hh", "sgbm"])
