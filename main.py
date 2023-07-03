import cv2
import os
import numpy as np
from win32api import GetSystemMetrics
from Library import LidarX2
import time
import math

class MouseData:
    def __init__(self):
        self.matrix = None
        self.cell_size = 0
        self.img = None
        self.orig_Img = None
        self.counter = 0
        self.checkpoint_counter = -5
        self.before = None

class GridData:
    def __init__(self):
        self.begin_X = 0
        self.begin_Y = 0
        self.start = 0
        self.end = 0

class StoreData:
    def __init__(self):
        self.G_Data = GridData()
        self.M_Data = MouseData()

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

def GetPosition(location_map):
    img = cv2.imread(location_map)
    if img is None:
        print("No image to search")
        return None
    
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    blue = (255, 0, 0)
    blue = cv2.cvtColor(np.uint8([[blue]]), cv2.COLOR_BGR2HSV)[0][0]

    mask = cv2.inRange(hsv_img, blue, blue)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        M = cv2.moments(largest_contour)
        centroid_x = int(M["m10"] / M["m00"])
        centroid_y = int(M["m01"] / M["m00"])

    return centroid_x, centroid_y

def readTxt(filename):
    # Read the contents of the text file
    with open(filename, "r") as file:
        data = file.read()

    # Split the data into separate arrays
    lines = data.split("\n")
    array1 = lines[0].split(",")
    array2 = lines[1].split(",")
    array3 = lines[2].split(",")
    
    return array1, array2, array3

def setData(img, begin, end, orig_Img):
    longest_dim = max(img.shape[1], img.shape[0])
    cell_size = int(np.ceil(longest_dim / 300))

    u_Data = StoreData()
    u_Data.G_Data.begin_X = begin[0]
    u_Data.G_Data.begin_Y = begin[1]
    u_Data.G_Data.start = begin
    u_Data.G_Data.end = end

    roi = (begin[0], begin[1], end[0] - begin[0], end[1] - begin[1])
    roiImage = img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]

    width = int(np.ceil(roiImage.shape[1] / cell_size))
    height = int(np.ceil(roiImage.shape[0] / cell_size))

    matrix = [[0] * width for _ in range(height)]

    u_Data.M_Data.matrix = matrix
    u_Data.M_Data.cell_size = cell_size
    u_Data.M_Data.img = img
    u_Data.M_Data.orig_Img = orig_Img
    
    return matrix, u_Data

def getRoi(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the black color range
    lower = np.array([0, 0, 0])
    upper = np.array([180, 255, 30])

    # Create a mask to filter out non-black pixels
    mask = cv2.inRange(hsv_img, lower, upper)
    
    # Apply the mask to the original image
    maskImg = cv2.bitwise_and(img, img, mask=mask)

    # Find the coordinates of black pixels
    coords = []
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if mask[y, x] == 255:
                coords.append((x, y))

    # Find the highest, lowest, leftmost, and rightmost points
    highestPoint = coords[0]
    lowestPoint = coords[0]
    leftmostPoint = coords[0]
    rightmostPoint = coords[0]

    for coord in coords:
        if coord[1] < highestPoint[1]:
            highestPoint = coord
        if coord[1] > lowestPoint[1]:
            lowestPoint = coord
        if coord[0] < leftmostPoint[0]:
            leftmostPoint = coord
        if coord[0] > rightmostPoint[0]:
            rightmostPoint = coord

    startPoint = (leftmostPoint[0], highestPoint[1])  # Starting coordinate of the grid
    endPoint = (rightmostPoint[0], lowestPoint[1])  # Ending coordinate of the grid
    
    return maskImg, startPoint, endPoint

def makeGridCoords(pixel_x, pixel_y, data, matrix):
    if data.M_Data.before is not None:
        before = data.M_Data.before
        matrix[before[0]][before[1]] = 0
    
    # Use pixel coordinates as grid cell coordinates
    grid_cell_coordinates = (
        pixel_x // data.M_Data.cell_size,  # Column index
        pixel_y // data.M_Data.cell_size   # Row index
    )

    data.M_Data.before = grid_cell_coordinates
    
    matrix[grid_cell_coordinates[0]][grid_cell_coordinates[1]] = 1000
    
    return grid_cell_coordinates

def loadArray(arr1, arr2, arr3, matrix, u_Data):
    c1 = 1
    c2 = -1
    
    for cell in arr1:
        x, y = map(int, cell.split("/"))
        matrix[x][y] = c1
        c1 += 1
        
    for cell in arr2:
        x, y = map(int, cell.split("/"))
        matrix[x][y] = c2
        c2 -= 1
        
    for cell in arr3:
        x, y = map(int, cell.split("/"))
        matrix[x][y] = 6000

def createGridImage(filename):
    
    screenWidth = GetSystemMetrics(0)
    screenHeight = GetSystemMetrics(1)

    orig_Img = cv2.imread(filename, cv2.IMREAD_COLOR)
    if orig_Img is None:
        print("Could not read the image")

    imageAspectRatio = orig_Img.shape[1] / orig_Img.shape[0]
    
    maxWidth = screenWidth
    maxHeight = screenHeight
 
    scaledWidth = maxWidth
    scaledHeight = int(scaledWidth / imageAspectRatio)

    if scaledHeight > maxHeight:
        scaledHeight = maxHeight
        scaledWidth = int(scaledHeight * imageAspectRatio)

    posX = (screenWidth - scaledWidth) // 2
    posY = (screenHeight - scaledHeight) // 2

    orig_Img = cv2.resize(orig_Img, (scaledWidth, scaledHeight))
    
    img, begin, end = getRoi(orig_Img)

    position = GetPosition('location.png')
    if position is not None:
        dot_x, dot_y = position
        pixel = (dot_x - begin[0], dot_y - begin[1])
        print(pixel)
    else:
        print("No valid position found.")

    matrix, u_Data = setData(img, begin, end, orig_Img)
    
    arr1, arr2, arr3 = readTxt("arrays.txt")
    loadArray(arr1, arr2, arr3, matrix, u_Data)
    
    grid_coordinates = makeGridCoords(pixel[1], pixel[0], u_Data, matrix)
    print(grid_coordinates)
    
    return matrix

def main():
    lidar = LidarX2("/dev/ttyUSB0") 
    lidar_list=[]
    MapSide = "N"

    #check what way the robot is facing
    if( MapSide == "N"):
        img_map = cv2.imread('./Mappen_zijdes/North_side.png', cv2.IMREAD_GRAYSCALE)
        map=cv2.imread('./mappen_zijdes/Mapping_map_noord.png', cv2.IMREAD_GRAYSCALE)

    elif( MapSide == "E"):
        img_map = cv2.imread('./Mappen_zijdes/East_side.png', cv2.IMREAD_GRAYSCALE)
        map=cv2.imread('./mappen_zijdes/Mapping_map_east.png', cv2.IMREAD_GRAYSCALE)

    elif( MapSide == "S"):
        img_map = cv2.imread('./Mappen_zijdes/South_side.png', cv2.IMREAD_GRAYSCALE)
        map=cv2.imread('./mappen_zijdes/Mapping_map_zuid.png', cv2.IMREAD_GRAYSCALE)

    elif( MapSide == "W"):
        img_map = cv2.imread('./Mappen_zijdes/West_side.png', cv2.IMREAD_GRAYSCALE)
        map=cv2.imread('./mappen_zijdes/Mapping_map_west.png', cv2.IMREAD_GRAYSCALE)

    while lidar.open():
        #remove previous location image
        if os.path.exists("location.png"):
            os.remove("location.png")

        #starts the lidar
        #reads the lidar data and saves it in a list
        lidar_list.clear()
        for i in range(15):
            measures = lidar.getMeasures()  # Get latest lidar measures
            lidar_list.extend(measures)
            measures=[]
            time.sleep(0.010)
        lidar.close()
    
        img = np.ones((600, 600))
        img*=0
        
        #this makes 2 seperate lists, one with the degrees and one with the distance
        degrees, distance = listSplitter(lidar_list)

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

        # cv2.imshow("LIDAR Image", template)

        cv2.imwrite("location.png", img_map_cpy)

        matrix = createGridImage("location.png")
        
        cv2.waitKey(1)


