# import numpy as np
# import pyautogui
# import time
# from PIL import ImageGrab
# import cv2 as cv
# import os

# while True:
#     filename = "img.png"
#     for file in os.listdir("./"):
#         if file == "img.png":
#             os.remove(filename)
#             print(f"removed {filename}")
#     time.sleep(10)
#     img = pyautogui.screenshot()
#     img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
#     cv.imwrite(filename, img)
#     print(f"made {filename}")
#     time.sleep(10)


import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os

image1 = cv.imread("image.png")
for i in os.listdir("images"):
    hsv_img = cv.cvtColor(i, cv.COLOR_BGR2HSV)
    s_hc = hsv_img[:,:,1]
    thesh = cv.threshold(s_hc, 5, 255, cv.THRESH_BINARY)[1]
    thesh = cv.morphologyEx(thesh, cv.MORPH_OPEN, cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7)))

    cv.floodfill(thesh, None, seedPoint=(0,0), newVal=128, loDiff=1, upDiff=1)
    
    i[thesh == 128] = (255,255,255)

    image2 = i
    cropped = image2[90:280, 150:330]
    print(image2.shape[+1::-1])
    w,h = image2.shape[+1::-1]

    res = cv.matchTemplate(image1,image2,cv.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where( res>=threshold)
    for pt in zip(*loc[::1]):
        print(pt)
        cv.rectangle(image1, pt, (pt[0] +w, pt[1] +h), (0,0,255), 2)
        break

    cv.imshow('res.png', image1)
    cv.imshow('search.png', image2)
    cv.waitKey(0)