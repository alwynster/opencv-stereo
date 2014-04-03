import subprocess
import os

#base = 'C:\\Users\\15685500\\Dropbox\\Masters\\Implementation\\Stereo\\OpenCV stereo\\output\\'
for i in range(1, 1801):
    os.system("ren " + "\"SAD 11 - tsukuba - %d.png\"" % i + " disp_tsukuba_%s_%05d.png" % ("sad", i))
