from test import LidarX2
import time
import numpy as np
import cv2
import math
from matplotlib import pyplot as plt

count=0
lidar = LidarX2("/dev/ttyUSB0")  # Name of the serial port, can be /dev/tty*, COM*, etc.
def calcPos(posX, posY, rotation, distance):
    y_Offset = math.cos(rotation * 3.14159265359 / 180) * (distance*200)
    x_Offset = math.sin(rotation * 3.14159265359 / 180) * (distance*200)
    posX += x_Offset
    posY += -y_Offset
    return (int(posX)-300, int(posY)-300)


lijst=[]

while lidar.open():
    #starts the lidar
    #reads the lidar data and saves it in a list
    for i in range(20):
        measures = lidar.getMeasures()  # Get latest lidar measures
        #if len(measures)>=270:
        lijst.extend(measures)
        measures=[]
        time.sleep(0.015)
    lidar.close()
    distance=[]
    degrees=[]
    img = np.ones((600, 600))
    img*=0.392
    
    #this makes 2 seperate lists, one with the degrees and one with the distance
    for i in lijst:
        x=str(i).split(":")
        if float(x[0])>0 :    
            degrees.append(float(x[0]))
            distance.append(float(x[1].split("mm")[0]))
    #this makes mm to pixels between the middle and points
    for i in range(0, len(distance)-1):
        if distance[i]== 0:
            distance[i] = 2 # 4000/2000 = 4 meter 
        else:
            distance[i] = distance[i] / 2000
    #this draws the lines and points    

    for i in range(0, len(degrees)-1):
        img = cv2.line(img, (300, 300), calcPos(600, 600, degrees[i], distance[i]), (1, 1, 1), 3)
        img = cv2.circle(img, calcPos(600, 600, degrees[i], distance[i]), 1, (0, 0, 0), 4)

    def rotateImage(image, angle):
        row, col = image.shape
        center = tuple(np.array([col, row]) / 2)  # Corrected order of dimensions
        rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
        new_image = cv2.warpAffine(image, rot_mat, (col, row))
        return new_image

    img_map = cv2.imread('map/Map_West.png', cv2.IMREAD_GRAYSCALE)
    assert img_map is not None, "file could not be read, check with os.path.exists()"
    img2 = img_map.copy()

    template = img.copy()
    template = cv2.resize(template, (int(template.shape[1] * 1.45), int(template.shape[0] * 1.35)))

    assert template is not None, "file could not be read, check with os.path.exists()"
    w, h = template.shape[::-1]

    # All the 6 methods for comparison in a list
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED']

    threshold = 0.45

    for rotation in range(0, 1):
        rotated_template = rotateImage(template, rotation)
        for meth in methods:
            img_map = img2.copy()
            method = eval(meth)
            # Apply template Matching
            res = cv2.matchTemplate(img_map, rotated_template, method)
            loc = np.where(res >= threshold)
            print(loc)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img_map, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), 2)
            # If statement vorige code terug zetten.

    # for meth in methods:
    #     img = img2.copy()
    #     method = eval(meth)
    #     # Apply template Matching
    #     res = cv.matchTemplate(img,template,method)
    #     print(res)
    #     min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    #     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    #     if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
    #         top_left = min_loc
    #     else:
    #         top_left = max_loc
    #     bottom_right = (top_left[0] + w, top_left[1] + h)
    #     cv.rectangle(img,top_left, bottom_right, 0, 2)
            
    plt.subplot(2, 1)
    plt.imshow(img_map, cmap='gray')
    plt.title('Detected Point')

    #this shows the image
    plt.subplot(1, 1)
    plt.imshow("Image", img)
    plt.title('Live LIDAR Image')
    plt.show()
    lijst.clear()

    #this saves the image if a button is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        count+=1
        img = cv2.resize(img, (90,90))
        cv2.imwrite("rechtsonder"+'/'+str(count)+".png",255*img)

    if cv2.waitKey(1) & 0xFF == ord('e'):
        resized = cv2.resize(img, (90,90))

    cv2.waitKey(1)