#test 1
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
    print(pt)
    cv2.rectangle(image1, pt, (pt[0] +w, pt[1] +h), (0,0,255), 2)
    break

cv2.imshow('res.png', image1)
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