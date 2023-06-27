import os
import cv2

# Load the image
image = cv2.imread('map_new_new_edited.png')

# Define the dot position
dot_x = 650
dot_y = 1500

# Draw a dot on the image
cv2.circle(image, (dot_x, dot_y), radius=2, color=(255, 0, 0), thickness=-1)

# Display the image with the dot
if (os.path.exists('location.png')):
    os.remove('location.png')
cv2.imwrite('location.png', image)