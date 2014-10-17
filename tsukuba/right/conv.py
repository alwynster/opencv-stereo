import cv2
import os

files = os.listdir('color')

for f in files:
    if os.path.splitext(f)[1] != '.png': continue

    img = cv2.imread('color/' + f)
    img = cv2.cvtColor(img, cv2.cv.CV_BGR2GRAY)
    cv2.imwrite(f, img)

