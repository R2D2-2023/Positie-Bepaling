# from Library import LidarX2
import time
import numpy as np
import cv2
import math
import argparse
from matplotlib import pyplot as plt
import os
#count=16
#lidar = LidarX2("/dev/ttyUSB0")  # Name of the serial port, can be /dev/tty*, COM*, etc.
def calcPos(posX, posY, rotation, distance):
    y_Offset = math.cos(rotation * 3.14159265359 / 180) * (distance*200)
    x_Offset = math.sin(rotation * 3.14159265359 / 180) * (distance*200)
    posX += x_Offset
    posY += -y_Offset
    return (int(posX)-300, int(posY)-300)


def rotateImage(image, angle):
        row, col = image.shape
        center = tuple(np.array([col, row]) / 2)  # Corrected order of dimensions
        rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
        new_image = cv2.warpAffine(image, rot_mat, (col, row))
        return new_image


def ParseLocation(inputText):
    try:
        x, y = map(int, inputText.split(','))
        return x, y
    except:
        raise argparse.ArgumentTypeError("Input format must be 'x, y'")


parser = argparse.ArgumentParser()
parser.add_argument('MapSide')
parser.add_argument('-c,--previous-coordinates', type=ParseLocation, nargs=2)

args = parser.parse_args()


lijst=[]

lastPos = (0,0)
img_map = cv2.imread("./Mappen_zijdes/Map_Zuid3.png", cv2.IMREAD_GRAYSCALE)
img_map = cv2.rotate(img_map, cv2.ROTATE_90_CLOCKWISE)
mapDimensions = img_map.shape
# img_map = cv2.resize(img_map, (int(mapDimensions[0]/2),int(mapDimensions[1]/2)))


print("done contrast")


map_oost=cv2.imread('./mappen_zijdes/Mapping_map_east.png',cv2.IMREAD_GRAYSCALE)

if( args.MapSide == "N"):
    img_map = cv2.imread('./Mappen_zijdes/North_side.png', cv2.IMREAD_GRAYSCALE)
    # img_map = cv2.rotate(img_map, cv2.ROTATE_90_CLOCKWISE)
elif( args.MapSide == "E"):
    img_map = cv2.imread('./Mappen_zijdes/East_side.png', cv2.IMREAD_GRAYSCALE)
    # img_map = cv2.resize(img_map, (100,img_map.shape[0]))
elif( args.MapSide == "S"):
    img_map = cv2.imread('./Mappen_zijdes/South_side.png', cv2.IMREAD_GRAYSCALE)
elif( args.MapSide == "W"):
    img_map = cv2.imread('./Mappen_zijdes/West_side.png', cv2.IMREAD_GRAYSCALE)
   
mapDimensions = img_map.shape
print("done Resizing")

for filename in os.listdir("./test"):
    f = os.path.join("./test", filename)
    print(f)
    assert img_map is not None, "file could not be read, check with os.path.exists()"
    img2 = img_map.copy()
    template = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
    mapDimensions = template.shape
    assert template is not None, "file could not be read, check with os.path.exists()"
    w, h = template.shape[::-1]
    
    res = cv2.matchTemplate(img_map, template, cv2.TM_CCOEFF_NORMED)
    
    amount = 0 # of matches
    step = 10
    threshold = 1 
    loc = []
    cycles = 0
    loc = np.where(res == np.max(res))
    
    img_map_cpy = map_oost.copy()
    # print(threshold) 
    img_map_cpy = cv2.cvtColor(img_map_cpy,cv2.COLOR_GRAY2RGB)
       
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_map_cpy, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), 2)
        x=int(round(pt[0]+(w/2)))
        y=int(round(pt[1]+(h/2)))
        cv2.circle(img_map_cpy, (x,y),2, (255, 0, 0), 4)

    lastPos = pt
    # If statement vorige code terug zetten.


    template = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)

    cv2.imshow("LIDAR Image", template)
    img_rotated = cv2.rotate(img_map_cpy, cv2.ROTATE_90_CLOCKWISE)

    cv2.imshow("Check Image", img_rotated)

    lijst.clear()

    

    cv2.waitKey()

    # time.sleep(50000000)