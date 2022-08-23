import cv2

method = cv2.TM_SQDIFF_NORMED

map = cv2.imread('laberintiniti.png', 0)
arrow = cv2.imread('Nick.png', 0)

result = cv2.matchTemplate(arrow, map, method)
print(result)
mn, _, mnLoc, _ = cv2.minMaxLoc(result)
MPx, MPy = mnLoc
trows, tcols = arrow.shape[:2]
cv2.rectangle(map, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 0, 255), 2)

# Display the original image with the rectangle around the match.
cv2.imshow('output', map)

# The image is only displayed if we call this
cv2.waitKey(0)
