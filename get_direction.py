import cv2
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)
method = cv2.TM_SQDIFF_NORMED

map = cv2.imread('laberintiniti.png', 0)
arrow = cv2.imread('Nick.png', 0)

result = cv2.matchTemplate(arrow, map, method)
print(result)
mn, _, mnLoc, _ = cv2.minMaxLoc(result)
MPx, MPy = mnLoc
print(MPx, MPy)
trows, tcols = arrow.shape[:2]
print(MPx + tcols, MPy + trows)
MPx = MPx + 20
MPy = MPy + 20
rectangle = cv2.rectangle(map, (MPx, MPy), (MPx + (tcols - 40), MPy + (trows - 20)), (0, 0, 255), 2)
print(len(rectangle))
# Display the original image with the rectangle around the match.
cv2.imshow('output', map)

# The image is only displayed if we call this
cv2.waitKey(0)
