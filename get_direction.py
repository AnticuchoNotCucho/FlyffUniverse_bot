import cv2
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)
method = cv2.TM_SQDIFF_NORMED

map = cv2.imread('laberintiniti.png')
arrow = cv2.imread('Nick.png')

result = cv2.matchTemplate(arrow, map, method)
mn, _, mnLoc, _ = cv2.minMaxLoc(result)
MPx, MPy = mnLoc
trows, tcols = arrow.shape[:2]
MPx = MPx + 20
MPy = MPy + 20
rectangle = cv2.rectangle(map, (MPx, MPy), (MPx + (tcols - 40), MPy + (trows - 20)), (0, 0, 255), 2)
sub_image = map[MPy:MPy + (trows - 20), MPx:MPx + (tcols - 40)]
gray = cv2.cvtColor(sub_image, cv2.COLOR_BGR2GRAY)
# threshold the grayscale image
ret, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(gray, contours, -1, (0, 255, 0), 3)
img_contours = np.zeros(gray.shape)
cv2.drawContours(img_contours, contours, -1, (255, 255, 255), 1)
cv2.imshow('contours', img_contours)

# The image is only displayed if we call this
cv2.waitKey(0)
