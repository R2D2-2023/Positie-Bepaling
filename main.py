import cv2
import numpy as np
from matplotlib import pyplot as plt

image1 = cv2.imread("image.png")
image2 = cv2.imread("image4.png")
print(image2.shape[+1::-1])
w,h = image2.shape[+1::-1]

res = cv2.matchTemplate(image1,image2,cv2.TM_CCOEFF_NORMED)
threshold = 0.5
loc = np.where( res>=threshold)
for pt in zip(*loc[::1]):
    cv2.rectangle(image1, pt, (pt[0] +w, pt[1] +h), (0,0,255), 2)

cv2.imshow('res.png', image1)
cv2.waitKey(0)