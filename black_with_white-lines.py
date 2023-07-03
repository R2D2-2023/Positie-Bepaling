from Library import LidarX2
import time
import numpy as np
import cv2
import math

 # Name of the serial port, can be /dev/tty*, COM*, etc.
def calcPos(posX, posY, rotation, distance):
    y_Offset = math.cos(rotation * 3.14159265359 / 180) * (distance*200)
    x_Offset = math.sin(rotation * 3.14159265359 / 180) * (distance*200)
    posX += x_Offset
    posY += -y_Offset
    return (int(posX)-300, int(posY)-300)

def listSplitter(list):
    distance=[]
    degrees=[]
    for i in list:
        x=str(i).split(":")
        if float(x[0])>0 :    
            degrees.append(float(x[0]))
            distance.append(float(x[1].split("mm")[0]))
    return degrees, distance

def rotateImage(image, angle):
        row, col = image.shape
        center = tuple(np.array([col, row]) / 2)  # Corrected order of dimensions
        rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
        new_image = cv2.warpAffine(image, rot_mat, (col, row))
        return new_image

def main():
    lidar = LidarX2("/dev/ttyUSB0") 
    lijst=[]

    if( args.MapSide == "N"):
        img_map = cv2.imread('./Mappen_zijdes/North_side.png', cv2.IMREAD_GRAYSCALE)
        map=cv2.imread('./mappen_zijdes/Mapping_map_noord.png', cv2.IMREAD_GRAYSCALE)

    elif( args.MapSide == "E"):
        img_map = cv2.imread('./Mappen_zijdes/East_side.png', cv2.IMREAD_GRAYSCALE)
        map=cv2.imread('./mappen_zijdes/Mapping_map_east.png', cv2.IMREAD_GRAYSCALE)

    elif( args.MapSide == "S"):
        img_map = cv2.imread('./Mappen_zijdes/South_side.png', cv2.IMREAD_GRAYSCALE)
        map=cv2.imread('./mappen_zijdes/Mapping_map_zuid.png', cv2.IMREAD_GRAYSCALE)

    elif( args.MapSide == "W"):
        img_map = cv2.imread('./Mappen_zijdes/West_side.png', cv2.IMREAD_GRAYSCALE)
        map=cv2.imread('./mappen_zijdes/Mapping_map_west.png', cv2.IMREAD_GRAYSCALE)

    while lidar.open():
        #starts the lidar
        #reads the lidar data and saves it in a list
        lijst.clear()
        for i in range(15):
            measures = lidar.getMeasures()  # Get latest lidar measures
            lijst.extend(measures)
            measures=[]
            time.sleep(0.010)
        lidar.close()
    
        img = np.ones((600, 600))
        img*=0
        
        #this makes 2 seperate lists, one with the degrees and one with the distance
        degrees, distance = listSplitter(lijst)

        #this makes mm to pixels between the middle and points
        for i in range(0, len(distance)-1):
            if distance[i]== 0:
                distance[i] = 3 # 4000/2000 = 4 meter 
            else:
                distance[i] = distance[i] / (2000*2)
            
        #this draws the lines and points    

        for i in range(0, len(degrees)-1):
            if distance[i]>0:
                img = cv2.circle(img, calcPos(600, 600, degrees[i], distance[i]), 1, (1, 1, 1), 5)
        
        img = cv2.resize(img, (200,200)) #----------------------------------------------------------------------------------------------------------------------
        uint_img = np.array(img*255).astype('uint8')
        template = uint_img.copy()
            
        assert img_map is not None, "file could not be read, check with os.path.exists()"
        img2 = img_map.copy()

        assert template is not None, "file could not be read, check with os.path.exists()"
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_map, template, cv2.TM_CCOEFF) #TM_CCOEFF_NORMED
        loc = np.where(res == np.max(res))
    
        img_map_cpy = map.copy()
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_map_cpy, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)
            x=int(round(pt[0]+(w/2)))
            y=int(round(pt[1]+(h/2)))
            cv2.circle(img_map_cpy, (x,y),2, (255, 0, 0), 4)
        lastPos = pt

        cv2.imshow("LIDAR Image", template)

        cv2.imshow("Check Image", img_map_cpy)

        cv2.waitKey(1)

if __name__ == '__main__':
    main()