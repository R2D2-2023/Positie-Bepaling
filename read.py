import cv2
import numpy as np

with open('coords.txt', 'w') as f:


    # Load the map image
    image = cv2.imread('location.png')

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the red color range
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])

    # Threshold the image to get only red pixels
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the binary image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the contours
    for contour in contours:
        # Calculate the centroid of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            centroid_x = int(M["m10"] / M["m00"])
            centroid_y = int(M["m01"] / M["m00"])
            
            # Print the centroid coordinates
            f.write("({}, {})".format(centroid_x, centroid_y))