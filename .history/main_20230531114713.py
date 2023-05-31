import cv2 as cv
import numpy as np
import os

img_dir = "C:\school\Positie-Bepaling\images"
floor_img = "image.png"
floor = cv.imread(floor_img, cv.IMREAD_UNCHANGED)

for file in os.listdir(img_dir):
    # loading the lidar data (now images)
    image_name = os.path.join(img_dir, file)
    if not os.path.exists(image_name):
        print(f"{image_name} does not exist")
        continue
    img = cv.imread(image_name, cv.IMREAD_UNCHANGED) # Load without chaning the image
    img = img[275:250+300,275:250+300] # Image cropping to fit the map

    #set a black background
    mask = img[:,:,3] == 0
    img[mask] = [0,0,0,255]


    w,h = img.shape[+1::-1] #get width and height from the image
    res = cv.matchTemplate(floor, img, cv.TM_CCOEFF_NORMED)
    amount = 0 # of matches
    step = 10
    threshold = 0.1 #
    loc = []
    cycles = 0
    while(amount < 1 or amount > 1): #aslong as amount is above or beneath 1
        loc = np.where( res>=threshold ) #look where the image matches the map
        amount = len(loc[0]) #store how many are matching
        if amount < 1:
            threshold -= step
        elif amount > 1:
            threshold += step
        step *= 0.9
        cycles +=1
        if cycles > 100:
            break

    floor_copy = floor.copy()
    for pt in zip(*loc[::-1]):
        match_area = floor[pt[1]:pt[1]+h, pt[0]:pt[0]+w]
        match_gray = cv.cvtColor(match_area, cv.COLOR_BGR2GRAY) #set image to gray
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
        print(pt)
        # cv.line(floor_copy, (170, 180), (170, 180), (255, 255, 0), 10)
        x=round(((pt[0]+w)+pt[0])/2)
        y=round(((pt[1]+h)+pt[1])/2)

        cv.line(floor_copy, [x,y], [x,y], (255, 255, 0), 10)


        cv.rectangle(floor_copy, pt, (pt[0]+w, pt[1]+h), (0,0,255), 1)
        break

    cv.imshow(f'floor', floor_copy) 
    cv.moveWindow('floor', 600,00)
    cv.imshow(f'{image_name}', img)
    key = cv.waitKey(0) & 0xFF
    if key == 27: #check if escape is pressed
        break
    elif key == 13: #check if enter is pressed
        cv.destroyWindow(f'{image_name}')


cv.destroyAllWindows()