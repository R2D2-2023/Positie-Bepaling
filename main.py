import os
import cv2
import numpy as np
from win32api import GetSystemMetrics

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

def SetData(img, begin, end, orig_Img):
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

def GetRoi(img):
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

def ScaleImage(origImg):
    screenWidth = GetSystemMetrics(0)
    screenHeight = GetSystemMetrics(1)

    if origImg is None:
        print("Could not read the image")

    imageAspectRatio = origImg.shape[1] / origImg.shape[0]
    
    maxWidth = screenWidth
    maxHeight = screenHeight
 
    scaledWidth = maxWidth
    scaledHeight = int(scaledWidth / imageAspectRatio)

    if scaledHeight > maxHeight:
        scaledHeight = maxHeight
        scaledWidth = int(scaledHeight * imageAspectRatio)

    posX = (screenWidth - scaledWidth) // 2
    posY = (screenHeight - scaledHeight) // 2

    cv2.namedWindow("Grid Image")
    cv2.moveWindow("Grid Image", posX, posY)
    origImg = cv2.resize(origImg, (scaledWidth, scaledHeight))

    return origImg

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

    return None

def UpdateGridImage(matrix, data):
    grid_color = (0, 0, 255)
    grid_color_green = (0, 255, 0)
    grid_color_checkpoint = (255, 0, 255)
    grid_color_corner = (255, 255, 0)
    grid_img = data.M_Data.orig_Img.copy()
    cell_size = data.M_Data.cell_size

    for i in range(len(matrix)):
        y = data.G_Data.begin_Y + i * cell_size
        for j in range(len(matrix[i])):
            x = data.G_Data.begin_X + j * cell_size
            value = matrix[i][j]
            rect_color = None
            if value == 0:
                rect_color = grid_color
            elif value == 6000:
                rect_color = grid_color_corner
            elif value == 1000:
                rect_color = (255, 0, 0)
            else:
                if value < 0:
                    rect_color = grid_color_checkpoint
                else:
                    rect_color = grid_color_green
            cv2.rectangle(grid_img, (x, y), (x + cell_size, y + cell_size), rect_color, 1 if value == 0 else -1)
    
    cv2.imshow("Grid Image", grid_img)

def ReadTxt(filename):
    # Read the contents of the text file
    with open(filename, "r") as file:
        data = file.read()

    # Split the data into separate arrays
    lines = data.split("\n")
    array1 = lines[0].split(",")
    array2 = lines[1].split(",")
    array3 = lines[2].split(",")
    
    return array1, array2, array3

def MakeGridCoords(pixel_x, pixel_y, data, matrix):
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
    UpdateGridImage(matrix, data)
    
    return grid_cell_coordinates

def LoadArray(arr1, arr2, arr3, matrix, u_Data):
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
    
    UpdateGridImage(matrix, u_Data)

def CreateGridImage(filename, coords):
    
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

    cv2.namedWindow("Grid Image")
    cv2.moveWindow("Grid Image", posX, posY)
    orig_Img = cv2.resize(orig_Img, (scaledWidth, scaledHeight))
    
    
    img, begin, end = GetRoi(orig_Img)

    matrix, u_Data = SetData(img, begin, end, orig_Img)
    
    UpdateGridImage(matrix, u_Data)
    
    arr1, arr2, arr3 = ReadTxt("arrays.txt")
    LoadArray(arr1, arr2, arr3, matrix, u_Data)
    
    grid_coordinates = MakeGridCoords(coords[1], coords[0], u_Data, matrix)
    print(grid_coordinates)
    # x en y kunnen soms verkeerd staan ༼ つ ◕_◕ ༽つ
    # idiot sandwich chinese boi xx Tom
    cv2.waitKey(0)
    
    return matrix

def main():
    image_og = cv2.imread('map_new_new_edited.png')
    position = GetPosition('location.png')

    if position is not None:
        dot_x, dot_y = position
        coords = (dot_x, dot_y)
        img = cv2.imread('map_new_new_edited.png')
        mask, start, end = GetRoi(img)
        matrix = CreateGridImage("map_new_new_edited.png", coords)
    else:
        print("No valid position found.")


if __name__ == '__main__':
    main()# Load the image