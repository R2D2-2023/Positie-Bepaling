import cv2
import math
import numpy as np
from win32api import GetSystemMetrics

class MouseData:
    def __init__(self):
        self.matrix = None
        self.cell_size = 0
        self.img = None
        self.origImg = None
        self.counter = 0
        self.checkpoint_counter = -5
        self.robotX = 10
        self.robotY = 10
        self.mode = 0

class GridData:
    def __init__(self):
        self.beginX = 0
        self.beginY = 0
        self.endX = 0
        self.endY = 0

class StoreData:
    def __init__(self):
        self.gData = GridData()
        self.MData = MouseData()


def update_grid_image(matrix, data):
    grid_color = (0, 0, 255)
    grid_img = data.MData.origImg.copy()
    cell_size = data.MData.cell_size

    for i in range(len(matrix)):
        y = data.gData.beginY + i * cell_size
        for j in range(len(matrix[i])):
            x = data.gData.beginX + j * cell_size
            value = matrix[i][j]
            rect_color = None
            if value == 0:
                rect_color = grid_color
            cv2.rectangle(grid_img, (x, y), (x + cell_size, y + cell_size), rect_color, 1 if value == 0 else -1)
    cv2.imshow("Grid Image", grid_img)
    


def read_txt(filename):
    # Read the contents of the text file
    with open(filename, "r") as file:
        data = file.read()

    # Split the data into separate arrays
    lines = data.split("\n")
    array1 = lines[0].split(",")
    array2 = lines[1].split(",")
    array3 = lines[2].split(",")
    
    return array1, array2, array3

def setData(img, begin, end, origImg):
    longest_dim = max(img.shape[1], img.shape[0])
    cell_size = int(np.ceil(longest_dim / 300))

    uData = StoreData()
    uData.gData.beginX = begin[0]
    uData.gData.beginY = begin[1]
    uData.gData.endX = end[0]
    uData.gData.endY = end[1]

    roi = (begin[0], begin[1], end[0] - begin[0], end[1] - begin[1])
    roiImage = img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]

    width = int(np.ceil(roiImage.shape[1] / cell_size))
    height = int(np.ceil(roiImage.shape[0] / cell_size))

    matrix = [[0] * width for _ in range(height)]

    uData.MData.matrix = matrix
    uData.MData.cell_size = cell_size
    uData.MData.img = img
    uData.MData.origImg = origImg
    
    return matrix, uData


def get_roi(img):
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


def create_grid_image(filename):
    
    screenWidth = GetSystemMetrics(0)
    screenHeight = GetSystemMetrics(1)

    origImg = cv2.imread(filename, cv2.IMREAD_COLOR)
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
    
    
    img, begin, end = get_roi(origImg)
    

    matrix, uData = setData(img, begin, end, origImg)
    
    update_grid_image(matrix, uData)

    cv2.waitKey(0)
    
    return matrix



def main():
    matrix = create_grid_image("map_new_new_edited.png")

if __name__ == '__main__':
    main()