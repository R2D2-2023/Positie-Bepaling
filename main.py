from Library import LidarX2
import time
import numpy as np
import cv2
import math
import argparse
from matplotlib import pyplot as plt

count=16
lidar = LidarX2("COM3")  # Name of the serial port, can be /dev/tty*, COM*, etc.
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

while lidar.open():
    #starts the lidar
    #reads the lidar data and saves it in a list
    for i in range(20):
        measures = lidar.getMeasures()  # Get latest lidar measures
        lijst.extend(measures)
        measures=[]
        time.sleep(0.015)
    lidar.close()
    distance=[]
    degrees=[]
    img = np.ones((600, 600))
    img*=0.8
    
    #this makes 2 seperate lists, one with the degrees and one with the distance
    for i in lijst:
        x=str(i).split(":")
        if float(x[0])>0 :    
            degrees.append(float(x[0]))
            distance.append(float(x[1].split("mm")[0]))
    #this makes mm to pixels between the middle and points
    for i in range(0, len(distance)-1):
        if distance[i]== 0:
            distance[i] = 3 # 4000/2000 = 4 meter 
        else:
            distance[i] = distance[i] / (2000*2)
        
    #this draws the lines and points    

    for i in range(0, len(degrees)-1):
        img = cv2.line(img, (300, 300), calcPos(600, 600, degrees[i], distance[i]), (1, 1, 1), 3)       
        img = cv2.circle(img, calcPos(600, 600, degrees[i], distance[i]), 1, (0, 0, 0), 5)
        # if distance[i]== 0:


    #this chooses which map to use for the matching
    if( args.MapSide == "N"):
        img_map = cv2.imread('./Mappen_zijdes/Map_Noord.png', cv2.IMREAD_GRAYSCALE)
        img_map = cv2.rotate(img_map, cv2.ROTATE_90_CLOCKWISE)
    elif( args.MapSide == "E"):
        img_map = cv2.imread('./Mappen_zijdes/Map_Oost.png', cv2.IMREAD_GRAYSCALE)
        print(img_map.shape)
        print(img.shape)
        img_map = cv2.resize(img_map, (100,img_map.shape[0]))
    elif( args.MapSide == "S"):
        img_map = cv2.imread('./Mappen_zijdes/Map_Zuid3.png', cv2.IMREAD_GRAYSCALE)
        img_map = cv2.rotate(img_map, cv2.ROTATE_90_CLOCKWISE)
    elif( args.MapSide == "W"):
        img_map = cv2.imread('./Mappen_zijdes/Map_West.png', cv2.IMREAD_GRAYSCALE)
        img_map = cv2.rotate(img_map, cv2.ROTATE_90_CLOCKWISE)
        img_map = cv2.rotate(img_map, cv2.ROTATE_90_CLOCKWISE)



    mapDimensions = img_map.shape
    print("done Resizing")


    for x in range(mapDimensions[0]):
        for y in range(mapDimensions[1]):
            if img_map[x][y] < 50:
                img_map[x][y] = 0
            else:
                img_map[x][y] = 255    

    


        
    assert img_map is not None, "file could not be read, check with os.path.exists()"
    img2 = img_map.copy()

    img = cv2.resize(img, (100,200))
    uint_img = np.array(img*255).astype('uint8')
    template = uint_img.copy()
    scanDimensions = template.shape

    for x in range(scanDimensions[0]):
        for y in range(scanDimensions[1]):
            if template[x][y] < 50:
                template[x][y] = 0
            else:
                template[x][y] = 255

    assert template is not None, "file could not be read, check with os.path.exists()"
    w, h = template.shape[::-1]
    print(img_map.shape)
    print(img.shape)
    # Apply template Matching
    res = cv2.matchTemplate(img_map, template, cv2.TM_CCOEFF_NORMED)
    # cv2.imshow("Map", img_map)
    
    # cv2.imshow("Res prior", res)

    # if lastPos != (0,0):
    #     dimensions = res.shape
    #     for x in range(dimensions[0]):
    #         for y in range(dimensions[1]):
    #             pos = (x,y)
    #             dist = math.dist(lastPos, pos)
    #             dist *= 0.05
    #             newValue = res[x][y] / (dist+1)
    #             res[x][y] = (newValue + res[x][y]*2)/3
    amount = 0 # of matches
    step = 10
    threshold = 1 
    loc = []
    cycles = 0
    loc = np.where(res == np.max(res))
    # cv2.imshow("Res After", res)
    print(lastPos)

    
    # loc = np.where(res >= threshold)
    # while(amount != 1): #aslong as amount is above or beneath 1
    #     loc = np.where( res>=threshold ) #look where the image matches the map
    #     amount = len(loc[0]) #store how many are matching
    #     if amount < 1:
    #         threshold -= step
    #     elif amount > 1:
    #         threshold += step
    #     step *= 0.9
    #     cycles +=1
    #     if cycles > 100:
    #         break
    img_map_cpy = img_map.copy()
    print(threshold)        
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_map_cpy, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), 2)

    lastPos = pt
    # If statement vorige code terug zetten.


    # img = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow("LIDAR Image", template)
    # img_rotated = cv2.rotate(img_map, cv2.ROTATE_90_CLOCKWISE)

    cv2.imshow("Check Image", img_map_cpy)

    lijst.clear()

    #this saves the image if a button is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        count+=1
        img = cv2.resize(img, (90,90))
        cv2.imwrite('./'+str(count)+".png",255*img)

    if cv2.waitKey(1) & 0xFF == ord('e'):
        resized = cv2.resize(img, (90,90))

    cv2.waitKey(1)

    # time.sleep(50000000)