import cv2
import numpy as np
import subprocess
import matplotlib.pyplot as pp
# from timer import timer

__library__ = 'tsukuba'
def calculate_disp(min_frame, max_frame, algs):
    block = 5
    base = __library__ + "/"
    digits = 5
    if __library__ == 'tsukuba':
        form_L = "tsukuba_daylight_%s_%05d_%d"
        form = "tsukuba_daylight_%s_%05d"
    elif __library__ == 'kitti':
        form = "%s_%010d"
        
    output_form = "%s/disp_" + __library__ + "_%s_%05d_%d"

    disparities = 16*6

    percent = -1
    total_frames = max_frame - min_frame

    angles = range(-45, 45, 2)

    for angle in angles:
        for frame in range(min_frame, max_frame+1):
            for alg in algs:
                print "Performing for alg", alg
                args = ["OpenCV.exe", base + "rotate/" + (form_L % ('L', frame, angle)) + ".png", base + "right/" + (form % ('R', frame)) + ".png", "--algorithm=" + alg, "--max-disparity=" + str(disparities), "--blocksize=" + str(block), "--no-display", "-o", base + "rotate/output/" + (output_form % (alg, alg, frame, angle)) + ".png"]
                im1 = cv2.imread(args[1])
                im2 = cv2.imread(args[2])

                print im1
                print im2

                cv2.imshow('im1', im1)
                cv2.imshow('im2', im2)
                cv2.waitKey()

                print args
                try:
                    subprocess.call(args, shell=True)
                except Error:
                    print 'Error in OpenCV program'
                    return

if __name__ == "__main__":
    start = 1
    end = 1
    # calculate_disp(start, end, ["bm", "var", "hh", "sgbm"])
    calculate_disp(start, end, ["var", "sgbm"])
