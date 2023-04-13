#test 1
import cv2
import numpy as np
from matplotlib import pyplot as plt

image1 = cv2.imread("image.png")
image2 = cv2.imread("images/image7.png")
print(image2.shape[+1::-1])
image2 = image2[275:250+300, 250:250+250]
w,h = image2.shape[+1::-1]

res = cv2.matchTemplate(image1,image2,cv2.TM_CCORR_NORMED)
threshold = 0.5
loc = np.where( res>=threshold)
for pt in zip(*loc[::-1]):
    print(pt)
    cv2.rectangle(image1, pt, (pt[0] +w, pt[1] +h), (0,0,255), 2)
    break

cv2.imshow('res.png', image1)
cv2.imshow('search.png', image2)
cv2.waitKey(0)

#test 2
# import numpy as np
# import cv2 as cv
# from mss import mss

# b_box = {'top':350, 'left':600, 'width':350, 'height':350}

# sct = mss()

# while True:
#     sct_img = sct.grab(b_box)
#     cv.imshow('screen', np.array(sct_img))

#     if (cv.waitKey(1) & 0xFF) == ord('q'):
#         cv.destroyAllWindows()
#         break

#test 3
# from PIL import Image, ImageGrab
# import numpy as np
# import cv2 as cv
# import time

# screenshot = ImageGrab.grab()
# screenshot = np.array(screenshot)
# screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

# cv.imshow("screenshot", screenshot)
# cv.waitKey(0)


#test 4
# import cv2 as cv
# import numpy as np
# from matplotlib import pyplot as plt
# import os

# image1 = cv.imread("image.png")
# for i in os.listdir("images"):
#     hsv_img = cv.cvtColor(i, cv.COLOR_BGR2HSV)
#     s_hc = hsv_img[:,:,1]
#     thesh = cv.threshold(s_hc, 5, 255, cv.THRESH_BINARY)[1]
#     thesh = cv.morphologyEx(thesh, cv.MORPH_OPEN, cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7)))

#     cv.floodfill(thesh, None, seedPoint=(0,0), newVal=128, loDiff=1, upDiff=1)
    
#     i[thesh == 128] = (255,255,255)

#     cv.imshow("i", i)
#     cv.waitKey(0)

#     image2 = i
#     cropped = image2[90:280, 150:330]
#     print(image2.shape[+1::-1])
#     w,h = image2.shape[+1::-1]

#     res = cv.matchTemplate(image1,image2,cv.TM_CCOEFF_NORMED)
#     threshold = 0.5
#     loc = np.where( res>=threshold)
#     for pt in zip(*loc[::1]):
#         print(pt)
#         cv.rectangle(image1, pt, (pt[0] +w, pt[1] +h), (0,0,255), 2)
#         break

#     cv.imshow('res.png', image1)
#     cv.imshow('search.png', image2)
#     cv.waitKey(0)

# test 5
# import cv2 as cv
# import numpy as np

# img = cv.imread("images/image3.png", cv.IMREAD_UNCHANGED)
# mask = img[:,:,3] == 0
# img[mask] = [0,0,0,255]

# cv.imshow('img', img)
# cv.waitKey(0)