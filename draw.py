import os
import cv2
import numpy as np
from win32api import GetSystemMetrics

# Load the image
image_og = cv2.imread('map_new_new_edited.png')

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


def scale_image(origImg):
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

image_scaled = scale_image(image_og)

image, x, y = get_roi(image_scaled)

# Define the dot position
dot_x = 150 + x[0]
dot_y = 450 + x[1]

print(dot_x)
print(dot_y)
# Draw a dot on the image
cv2.circle(image_og, (dot_x, dot_y), radius=2, color=(255, 0, 0), thickness=-1)

cv2.rectangle(image_scaled, x, y, (0,0,255), thickness=1)
# cv2.circle(image_scaled, (dot_x, dot_y), radius=5)

# Display the image with the dot
if (os.path.exists('location.png')):
    os.remove('location.png')
cv2.imshow('location.png', image_scaled)
cv2.moveWindow('location.png', 50, 50)
cv2.waitKey(0)
cv2.destroyAllWindows()