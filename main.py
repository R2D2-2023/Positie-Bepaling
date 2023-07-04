import cv2
import os
import numpy as np
# from win32api import GetSystemMetrics
from Library import LidarX2
import time
import math
import serial


class MouseData:
    """!
    @brief [Description de la classe]


    """
    """!
    @brief [Description of the class]


    """
    def __init__(self):
        """!
        @brief Initializes 

        Paramètres : 
            @param self => initialization parameter

        """
        self.matrix = None
        self.cell_size = 0
        self.img = None
        self.orig_Img = None
        self.counter = 0
        self.checkpoint_counter = -5
        self.before = None

class GridData:
    """!
    @brief [Description of the class]


    """

    def __init__(self):
        """!
        @brief [Description of the function]

        Paramètres : 
            @param self => initialization parameter

        """
        self.begin_X = 0
        self.begin_Y = 0
        self.start = 0
        self.end = 0

class StoreData:
    """!
    @brief [Description of the class]


    """
    def __init__(self):
        """!
        @brief Initializes grid and mouse parameters 

        Paramètres : 
            @param self => initialization parameter

        """
        self.G_Data = GridData()
        self.M_Data = MouseData()

 # Name of the serial port, can be /dev/tty*, COM*, etc.

def calcPos(posX, posY, rotation, distance):
    """!
    @brief Calculates the position based on x, y values and angle and distance values 

    Paramètres : 
        @param posX => Image width 
        @param posY => Image height
        @param rotation => Lidar angle value
        @param distance => Lidar distance received value

    """
    y_Offset = math.cos(rotation * math.pi / 180) * (distance*200) #distance has been normalized so we mulitply by 200 for scaling
    x_Offset = math.sin(rotation * math.pi / 180) * (distance*200) #distance has been normalized so we mulitply by 200 for scaling
    posX += x_Offset
    posY += -y_Offset
    return (int(posX)-300, int(posY)-300)

def listSplitter(list):
    """!
    @brief Takes a list containing the distance measured on each degree and splits them into separate lists for degrees and distances

    Paramètres : 
        @param list => list of the distance and degrees measured with the lidar

    """
    distance=[]
    degrees=[]
    for i in list:
        x=str(i).split(":")
        if float(x[0])>0 :    
            degrees.append(float(x[0]))
            distance.append(float(x[1].split("mm")[0]))
    return degrees, distance

def GetPosition(location_map):
    """!
    @brief Gets the position of a blue circle in an image, by calculating the centroid of the largest contour in the image and gettting the x and y values from the centroid

    Paramètres : 
        @param location_map => map with the current position of the car

    """
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

    print(centroid_x, centroid_y)

    return (centroid_x, centroid_y)

def readTxt(filename):
    """!
    @brief Reads the data from a textfile containing key points of the grid and separates the data into 3 arrays(route, measure points and corners)  

    Paramètres : 
        @param filename => file with key points on the grid

    """
    # Read the contents of the text file
    with open(filename, "r") as file:
        data = file.read()

    # Split the data into separate arrays
    lines = data.split("\n")
    array1 = lines[0].split(",") # Route data
    array2 = lines[1].split(",") # Measure points data
    array3 = lines[2].split(",") # Corners data
    
    return array1, array2, array3

def setData(img, begin, end, orig_Img):
    """!
    @brief [Description of the function]

    Paramètres : 
        @param img => [description]
        @param begin => [description]
        @param end => [description]
        @param orig_Img => [description]

    """
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
    """!
    @brief [Description of the function]

    Paramètres : 
        @param img => image where the region of interest must be defined

    """
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
    """!
    @brief [Description of the function]

    Paramètres : 
        @param pixel_x => [description]
        @param pixel_y => [description]
        @param data => [description]
        @param matrix => [description]

    """
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

def loadArray(arr1, arr2, arr3, grid_coordinates):
    """!
    @brief [Description of the function]

    Paramètres : 
        @param arr1 => [description]
        @param arr2 => [description]
        @param arr3 => [description]
        @param matrix => [description]
        @param u_Data => [description]

    """

    
    for cell in arr1:
        xy = map(int, cell.split("/"))
        if xy == grid_coordinates:
            print("hij zit in " + xy)
            break
        else:
            print("niet op route")
            break

        
    for cell in arr2:
        xy = map(int, cell.split("/"))
        if xy == grid_coordinates:
            print("hij zit in " + xy)
            break
        else:
            print("niet op een meet punt")
            break

        
    for cell in arr3:
        xy = map(int, cell.split("/"))
        if xy == grid_coordinates:
            print("hij zit in " + xy)
            break
        else:
            print("niet op bij een bocht")
            break

def GetGridCoords(filename):
    """!
    @brief [Description of the function]

    Paramètres : 
        @param filename => image with the image 

    """
    
    screenWidth = 1536
    screenHeight = 864

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
    
    grid_coordinates = makeGridCoords(pixel[1], pixel[0], u_Data, matrix)
    loadArray(arr1, arr2, arr3, grid_coordinates)
    print(grid_coordinates)
    
    return matrix

def main():
    """!
    @brief [Description of the function]


    """
    lidar = LidarX2("/dev/ttyUSB0") 
    lidar_list=[]
   

    #check what way the robot is facing
    # map_
    img_map_N = cv2.imread('./Mappen_zijdes/North_side.png', cv2.IMREAD_GRAYSCALE)
    map_N=cv2.imread('./Mappen_zijdes/Mapping_map_noord.png', cv2.IMREAD_GRAYSCALE)
    img_map_N=cv2.rotate(img_map_N, cv2.ROTATE_90_CLOCKWISE)
    map_N=cv2.rotate(map_N, cv2.ROTATE_90_CLOCKWISE)

    img_map_E = cv2.imread('./Mappen_zijdes/East_side.png', cv2.IMREAD_GRAYSCALE)
    map_E=cv2.imread('./Mappen_zijdes/Mapping_map_oost.png', cv2.IMREAD_GRAYSCALE)
    
    img_map_S = cv2.imread('./Mappen_zijdes/South_side.png', cv2.IMREAD_GRAYSCALE)
    map_S=cv2.imread('./Mappen_zijdes/Mapping_map_zuid.png', cv2.IMREAD_GRAYSCALE)
    map_S=cv2.rotate(map_S, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img_map_S=cv2.rotate(img_map_S, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    img_map_W = cv2.imread('./Mappen_zijdes/West_side.png', cv2.IMREAD_GRAYSCALE)
    map_W=cv2.imread('./Mappen_zijdes/Mapping_map_west.png', cv2.IMREAD_GRAYSCALE)
    map_W=cv2.rotate(map_W, cv2.cv2.ROTATE_180)
    img_map_W=cv2.rotate(img_map_W, cv2.ROTATE_180)

    while lidar.open():
        #remove previous location image
        if os.path.exists("location.png"):
            os.remove("location.png")
        
        #starts the lidar
        #reads the lidar data and saves it in a list
        # direction = ser.readline().decode('utf-8').rstrip()
        direction="E"
        if(direction=="N"):
            img_map=img_map_N
            map_=map_N
        elif(direction=="E"):
            img_map=img_map_E
            map_=map_E
        elif(direction=="S"):
            img_map=img_map_S
            map_=map_S
        elif(direction=="W"):
            img_map=img_map_W
            map_=map_W
        else:
            print(direction)


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
        # print("test")   
        assert map_ is not None, "file could not be read, check with os.path.exists()"
        map_cpy = map_.copy()
        map_cpy=cv2.cvtColor(map_cpy, cv2.COLOR_BGR2RGB)


        # print(map_)
        

        assert template is not None, "file could not be read, check with os.path.exists()"
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_map, template, cv2.TM_CCOEFF) #TM_CCOEFF_NORMED
        loc = np.where(res == np.max(res))
        # map_=map_.read()
        for pt in zip(*loc[::-1]):
            cv2.rectangle(map_cpy, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), 2)
            x=int(round(pt[0]+(w/2)))
            y=int(round(pt[1]+(h/2)))
            cv2.circle(map_cpy, (x,y),2, (255, 0, 0), 4)
        lastPos = pt

        # cv2.imshow("LIDAR Image", map_cpy)
        # cv2.waitKey(1000000000)

        cv2.imwrite("location.png", map_cpy)

        matrix = GetGridCoords("location.png")
        # print(matrix)
        cv2.waitKey(1)

if __name__ == '__main__':
    # ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    # ser.reset_input_buffer()
    main()
