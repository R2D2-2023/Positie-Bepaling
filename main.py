import cv2
import os
import numpy as np
from Library import LidarX2
import time
import math
import serial
import statistics

##
# @file main.py
# @brief Code for determining the position on a map and converting it to a grid position.

##
# @class MouseData
# @brief Represents mouse-related data and properties.
#
# This class encapsulates various attributes and data related to mouse behavior
# and processing. It provides properties for managing the mouse matrix, cell size,
# images, counters, route information, and other variables.
#
class MouseData:
        ##
        # @brief Initializes a new instance of the MouseData class.
        #
        # @param self: Initilazes the MouseData object with default values for the matrix, cell size, images, counters, route, and other variables.
        #
    def __init__(self):
        self.matrix = None
        self.cell_size = 0
        self.img = None
        self.orig_img = None
        self.counter = 0
        self.checkpoint_counter = -5
        self.before = None

##
#@brief Represents a grid data object.
#
#The GridData class manages grid-related data, including the beginning and ending coordinates.
#
class GridData:

    ##
    #@brief Constructs a new GridData object.
    #
    #@param self: Initializes the GridData object with default values for the begin X and Y coordinates.
    #The start and end coordinates represent the beginning and ending coordinates for the Region of interest.
    #
    def __init__(self):
        self.begin_X = 0
        self.begin_Y = 0
        self.start = 0
        self.end = 0

##
#@class StoreData
#@brief Class for storing data.
#
#This class provides a mechanism for storing data using two different data types:
#- GridData: Represents grid-based data.
#- MouseData: Represents mouse-related data.
#
class StoreData:
    ##
    #@brief Constructs a new StoreData object. 
    #
    #@param self: initialization parameter
    #
    def __init__(self):
        self.G_Data = GridData()
        self.M_Data = MouseData()


##
#@brief Calculates the position based on x, y values and angle and distance values 
#
#
#@param posX: Image width 
#@param posY: Image height
#@param rotation: Lidar angle value
#@param distance: Lidar distance received value
#
#@return position X and Y values
def calcPos(posX, posY, rotation, distance):
    
    y_Offset = math.cos(rotation * math.pi / 180) * (distance*200)
    x_Offset = math.sin(rotation * math.pi / 180) * (distance*200) 
    posX += x_Offset
    posY += -y_Offset
    return (int(posX)-300, int(posY)-300)

##
#@brief Takes a list containing the distance measured on each degree and splits them into separate lists for degrees and distances
#
#
#@param list: list of the distance and degrees measured with the lidar
#
#@return splitted values in degrees and distance
def listSplitter(list):
    distance=[]
    degrees=[]
    for i in list:
        x=str(i).split(":")
        if float(x[0])>0 :    
            degrees.append(float(x[0]))
            distance.append(float(x[1].split("mm")[0]))
    return degrees, distance

##
#@brief Gets the position of a blue circle in an image, by calculating the centroid of the largest contour in the image and getting the x and y values from the centroid
#
#@param location_map: map with the current position of the car
#
#@return The position of the blue circle
#@return If there is no blue circle nothing is returned
def getPosition(location_map):

    img = cv2.imread(location_map)
    if img is None:
        print("No image to search")
        return None
    
    roi_x1, roi_y1 = 195, 103
    roi_x2, roi_y2 = 380, 784
    
    roi = img[roi_y1:roi_y2, roi_x1:roi_x2]

    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    blue = (255, 0, 0)
    blue = cv2.cvtColor(np.uint8([[blue]]), cv2.COLOR_BGR2HSV)[0][0]

    mask = cv2.inRange(hsv_roi, blue, blue)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        M = cv2.moments(largest_contour)

        if M["m10"] == 0:
            M["m10"] +=1
        if M["m00"] == 0:
            M["m00"]+=1
        if M["m01"] == 0:
            M["m01"]+=1

        centroid_x = int(M["m10"] / M["m00"])
        centroid_y = int(M["m01"] / M["m00"])
        centroid_x += roi_x1
        centroid_y += roi_y1

        return (centroid_x, centroid_y)

    else:
        print("No blue circle found in the ROI")
        return None


##
#@brief Reads the data from a textfile containing key points of the grid and separates the data into 3 arrays(route, measure points and corners)  
#
#@param filename: file with lists of the key points on the grid
#
#@return a splitted array of key points; route, measure points and corners
def readTxt(filename):

    with open(filename, "r") as file:
        data = file.read()
    lines = data.split("\n")
    array_route = lines[0].split(",") # Route data
    array_measure_location = lines[1].split(",") # Measure points data
    array_turning = lines[2].split(",") # Corners data
    
    return array_route, array_measure_location, array_turning

##
#@brief Sets the data for image processing.
#
#@param img: The input image.
#@param begin: The starting coordinates of the region of interest (ROI).
#@param end: he ending coordinates of the region of interest (ROI).
#@param orig_img: The original image.
#
#@return A tuple containing the matrix and an instance of the StoreData class.
#
def setData(img, begin, end, orig_img):
    longest_dim = max(img.shape[1], img.shape[0])
    cell_size = int(np.ceil(longest_dim / 300))
    

    u_Data = StoreData()
    u_Data.G_Data.begin_X = begin[0]
    u_Data.G_Data.begin_Y = begin[1]
    u_Data.G_Data.start = begin
    u_Data.G_Data.end = end

    roi = (begin[0], begin[1], end[0] - begin[0], end[1] - begin[1])
    roi_image = img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]

    width = int(np.ceil(roi_image.shape[1] / cell_size))
    height = int(np.ceil(roi_image.shape[0] / cell_size))

    matrix = [[0] * width for _ in range(height)]

    u_Data.M_Data.matrix = matrix
    u_Data.M_Data.cell_size = cell_size
    u_Data.M_Data.img = img
    u_Data.M_Data.orig_img = orig_img
    
    return matrix, u_Data

##
#@brief Extracts the ROI from an image.
#    This function takes an image as input and returns the ROI, start point, and end point of the grid.
#
#@param img: The input image.
#
# @return A tuple containing the ROI image, start point, and end point.
def getRoi(img):
    
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 0, 0])
    upper = np.array([180, 255, 30])

    mask = cv2.inRange(hsv_img, lower, upper)
    
    mask_img = cv2.bitwise_and(img, img, mask=mask)

    coords = []
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if mask[y, x] == 255:
                coords.append((x, y))

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

    start_point = (leftmostPoint[0], highestPoint[1]) 
    end_point = (rightmostPoint[0], lowestPoint[1])

    return mask_img, start_point, end_point

##
#@brief This function translates the pixel coordinate to a grid coordinate
#
#@param pixel_x: pixel coordinate X value
#@param pixel_y: pixel coordinate Y value
#@param data: The input data object containing route, measurement points, and corner attributes.
#@param matrix: The matrix containing the values.
#
def makeGridCoords(pixel_x, pixel_y, data, matrix):
    if data.M_Data.before is not None:
        before = data.M_Data.before
        matrix[before[0]][before[1]] = 0
        
    
    grid_cell_coordinates = (
        (pixel_x - data.G_Data.begin_X) // data.M_Data.cell_size,
        (pixel_y - data.G_Data.begin_Y) // data.M_Data.cell_size 
    )

    data.M_Data.before = grid_cell_coordinates

    return grid_cell_coordinates

##
#@brief This function loads an array and checks if the current position is found in the key points of the map and sends them using serial.
#
#@param arr_route: first array list, this is the drawn route
#@param arr_measurement_points: second array list, these are the turning points
#@param arr_turning_points: third array list, these are the measurement points
#@param grid_coordinates: the grid coordinates of the found position
def loadArray(arr_route, arr_measurement_points, arr_turning_points, grid_coordinates):

    for cell in arr_route:
        xy = map(int, cell.split("/"))
        if xy == grid_coordinates:
            blocked = 0
            print("locatie")
            ser.write(b"0\n")
            count2 = 0

    for cell in arr_measurement_points:
        xy = map(int, cell.split("/"))
        if xy == grid_coordinates:
            print("meten")
            ser.write(b"0\n")
            count2 = 0
        
    for cell in arr_turning_points:
        s = str(grid_coordinates[0])+','+str(grid_coordinates[1])
        ser1.write(s.encode())

##
# @brief This function scales the given image to the right size (1536x864 standard set value)
#
#@param orig_img: Scale the image to the correct size.
#
#@return The edited image.
#
def scaleImg(orig_img):
    screen_width = 1536
    screen_height = 864

    image_aspect_ratio = orig_img.shape[1] / orig_img.shape[0]
    
    max_width = screen_width
    max_height = screen_height
 
    scaled_width = max_width
    scaled_height = int(scaled_width / image_aspect_ratio)

    if scaled_height > max_height:
        scaled_height = max_height
        scaled_width = int(scaled_height * image_aspect_ratio)

    orig_img = cv2.resize(orig_img, (scaled_width, scaled_height))
    return orig_img

##
#@brief This function is used to measure the distance between the lidar and an object.
#If an object is detected within 400mm and in an angle of 0-30 and 330-360 degrees, then a 'stop' signal is sent. 
#
#@param distance: distance to where the lidar measures an object 
#@param degrees: the degree of the measured object from the lidar
def drive(distance,degrees):
    blocked = 0
    count = 0
    count2 = 0 
    median = []
    minimum = []
     
    for j in range(len(degrees)):
        if degrees[j] < 30 or degrees[j] > 330:
            count = count + 1
            if distance[j] != 0:
                median.append(distance[j])
            if len(median) != 0:
                if count == 5:
                    minimum.append(statistics.median(median))
                    count2 = count2 + 1
                    count = 0
                    median = []
                    if count2 == 5:
                        if blocked == 1 and min(minimum) > 400:
                            blocked = 0

                            print("drive")
                            ser.write(b"0\n")
                            count2 = 0
                        elif min(minimum) < 400 and blocked == 0:
                            blocked = 1
                            print("plz stop :(")
                            ser.write(b"1\n")
                            count2 = 0

##
#@brief This function is used to get the grid coordinates from a position set in an image.
#This image is updated with every measurment of lidar.
#
#@param filename: image with the image 
#
#@return grid coordinates of the pixel position
def getGridCoords(filename):
       
    orig_img = cv2.imread(filename, cv2.IMREAD_COLOR)
    if orig_img is None:
        print("Could not read the image")

    orig_img = scaleImg(orig_img)
    img, begin, end = getRoi(orig_img)

    position = getPosition('location.png')
    if position is not None:
        dot_x, dot_y = position
        pixel = (dot_x, dot_y)
        roi_x = pixel[0] - begin[0]
        roi_y = pixel[1] - begin[1]
        if 0 <= roi_x <= (end[0] - begin[0]) and 0 <= roi_y <= (end[1] - begin[1]):
            print(f"Pixel: {pixel[0]}, {pixel[1]}")
        else:
            print(f"Pixel: {pixel[0]}, {pixel[1]}")
            print("Pixel is not inside the ROI.")
    else:
        print("No valid position found.")

    matrix, u_Data = setData(img, begin, end, orig_img)
    
    arr_route, arr_measurement_points, arr_turning_points = readTxt("arrays.txt")
    
    grid_coordinates = makeGridCoords(pixel[1], pixel[0], u_Data, matrix)
    loadArray(arr_route, arr_measurement_points, arr_turning_points, grid_coordinates)
    return grid_coordinates

##
#@brief Sets lidar connection and loads map images, generates a live image based on the received lidar data, 
#the live image gets matched with the loaded maps and a blue circle gets drawn on the map indicating the cars position.
#The image will be saved and loaded into a matrix to get the corresponding grid position.
#
def main():
    lidar = LidarX2("/dev/ttyUSB0") 
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser1= serial.Serial('/dev/serial0', 9600, timeout=1)
    ser1.reset_input_buffer()

    lidar_list=[]
    map_full = cv2.imread('./Mappen_zijdes/map_new_new_edited.png', cv2.IMREAD_GRAYSCALE)

    img_map_N = cv2.imread('./Mappen_zijdes/North_side.png', cv2.IMREAD_GRAYSCALE)
    map_N=cv2.imread('./Mappen_zijdes/Mapping_map_noord.png', cv2.IMREAD_GRAYSCALE)
    matching = cv2.matchTemplate(map_full, map_N, cv2.TM_CCOEFF)
    loc_full_N = np.where(matching == np.max(matching))

    img_map_E = cv2.imread('./Mappen_zijdes/East_side.png', cv2.IMREAD_GRAYSCALE)
    map_E=cv2.imread('./Mappen_zijdes/Mapping_map_oost.png', cv2.IMREAD_GRAYSCALE)
    matching = cv2.matchTemplate(map_full, map_E, cv2.TM_CCOEFF)
    loc_full_E = np.where(matching == np.max(matching))

    img_map_S = cv2.imread('./Mappen_zijdes/South_side.png', cv2.IMREAD_GRAYSCALE)
    map_S=cv2.imread('./Mappen_zijdes/Mapping_map_zuid.png', cv2.IMREAD_GRAYSCALE)
    matching = cv2.matchTemplate(map_full, map_S, cv2.TM_CCOEFF)
    loc_full_S = np.where(matching == np.max(matching))   
    
    img_map_W = cv2.imread('./Mappen_zijdes/West_side.png', cv2.IMREAD_GRAYSCALE)
    map_W=cv2.imread('./Mappen_zijdes/Mapping_map_west.png', cv2.IMREAD_GRAYSCALE)
    matching = cv2.matchTemplate(map_full, map_W, cv2.TM_CCOEFF)
    loc_full_W = np.where(matching == np.max(matching))

    while lidar.open():
        if os.path.exists("location.png"):
            os.remove("location.png")

        direction = ser.readline().decode('utf-8').rstrip()
        if(direction=="W"):
            img_map=img_map_N
            map_=map_N
        elif(direction=="N"):
            img_map=img_map_E
            map_=map_E
        elif(direction=="E"):
            img_map=img_map_S
            map_=map_S
        elif(direction=="S"):
            img_map=img_map_W
            map_=map_W
        else:
            print(f"{direction} bestaat niet")


        lidar_list.clear()
        for i in range(15):
            measures = lidar.getMeasures()
            lidar_list.extend(measures)
            measures=[]
            time.sleep(0.010)
        lidar.close()
    
        img = np.ones((600, 600))
        img*=0
        
        degrees, distance = listSplitter(lidar_list)
        drive(distance,degrees)

        for i in range(0, len(distance)-1):
            if distance[i]== 0:
                distance[i] = 3
            else:
                distance[i] = distance[i] / (2000*2)
               
        for i in range(0, len(degrees)-1):
            if distance[i]>0:
                img = cv2.circle(img, calcPos(600, 600, degrees[i], distance[i]), 1, (1, 1, 1), 5)
        
        if(direction=="W"):
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif(direction=="E"):
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif(direction=="S"):
            img = cv2.rotate(img, cv2.ROTATE_180)

        img = cv2.resize(img, (200,200))
        uint_img = np.array(img*255).astype('uint8')
        template = uint_img.copy()

        assert map_full is not None,"file could not be read, check with os.path.exists()"
        map_cpy = map_full.copy()
        map_cpy=cv2.cvtColor(map_cpy, cv2.COLOR_BGR2RGB)

        assert template is not None, "file could not be read, check with os.path.exists()"
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_map, template, cv2.TM_CCOEFF)
        loc = np.where(res == np.max(res))

        if(direction=="W"):
            for pt in zip(*loc[::-1]):
                x=int(round(pt[0]+(w/2)))
                y=int(round(pt[1]+(h/2)))
                cv2.circle(map_cpy, ((x+int(loc_full_N[1])),(y+int(loc_full_N[0]))),2, (255, 0, 0), 4)
         
        elif(direction=="N"):
            for pt in zip(*loc[::-1]):
                x=int(round(pt[0]+(w/2)))
                y=int(round(pt[1]+(h/2)))
                cv2.circle(map_cpy, ((x+int(loc_full_E[1])),(y+int(loc_full_E[0]))),3, (255, 0, 0), 5)

        elif(direction=="E"):
            for pt in zip(*loc[::-1]):
                x=int(round(pt[0]+(w/2)))
                y=int(round(pt[1]+(h/2)))
                cv2.circle(map_cpy, ((x+int(loc_full_S[1])),(y+int(loc_full_S[0]))),2, (255, 0, 0), 4)
                
        elif(direction=="S"):
            for pt in zip(*loc[::-1]):
                x=int(round(pt[0]+(w/2)))
                y=int(round(pt[1]+(h/2)))
                cv2.circle(map_cpy, ((x+int(loc_full_W[1])),(y+int(loc_full_W[0]))),2, (255, 0, 0), 4)
                
        else:
            print(direction)

        map_cpy = scaleImg(map_cpy)
        cv2.imshow("LIDAR Image", map_cpy)
        cv2.imwrite("location.png", map_cpy)
        coords = getGridCoords("location.png")
       
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
