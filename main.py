import cv2 as cv
import numpy as np
import os

img_dir = "images"
floor_img = "image.png"
floor = cv.imread(floor_img, cv.IMREAD_UNCHANGED)

for file in os.listdir(img_dir):
    image_name = os.path.join(img_dir, file)
    if not os.path.exists(image_name):

        print(f"{image_name} does not exist")
        continue
    img = cv.imread(image_name, cv.IMREAD_UNCHANGED)
    img = img[275:250+300, 250:250+250]

    mask = img[:,:,3] == 0
    img[mask] = [0,0,0,255]

    w,h = img.shape[+1::-1]
    res = cv.matchTemplate(floor, img, cv.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where( res>=threshold )

    floor_copy = floor.copy()
    for pt in zip(*loc[::-1]):
        match_area = floor[pt[1]:pt[1]+h, pt[0]:pt[0]+w]
        match_gray = cv.cvtColor(match_area, cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, match_thresh = cv.threshold(match_gray, 0, 255, cv.THRESH_BINARY_INV)
        _, img_thresh = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY_INV)

        match_cont, _ = cv.findContours(match_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        img_cont, _ = cv.findContours(img_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        match_rect = cv.minAreaRect(match_cont[0])
        match_box = cv.boxPoints(match_rect)
        match_box = np.intp(match_box)

        img_rect = cv.minAreaRect(img_cont[0])
        img_box = cv.boxPoints(img_rect)
        img_box = np.intp(img_box)

        affaine = cv.getAffineTransform( img_box[:3].astype(np.float32).reshape(3,2), match_box[:3].astype(np.float32).reshape(3,2))
        warped = cv.warpAffine(img, affaine, (w,h), borderMode=cv.BORDER_CONSTANT, borderValue=(0,0,0,0))

        floor_copy[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = cv.addWeighted(warped, 1, match_area, 1 ,0)

        cv.drawContours(floor_copy, [match_box], 0, (0,0,255), 1)

        cv.rectangle(floor_copy, pt, (pt[0]+w, pt[1]+h), (0,0,255), 1)
        break

    cv.imshow(f'floor', floor_copy)
    cv.imshow(f'{image_name}', img)
    key = cv.waitKey(0) & 0xFF
    if key == 27:
        break
    elif key == 13:
        cv.destroyWindow(f'{image_name}')
        cv.destroyWindow(f'floor')


cv.destroyAllWindows()