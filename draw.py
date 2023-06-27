import cv2

# Load the image
image = cv2.imread('map_new_new_edited.png')

# Define the dot position
dot_x = 650
dot_y = 900

# Draw a dot on the image
cv2.circle(image, (dot_x, dot_y), radius=2, color=(0, 0, 255), thickness=-1)

# Display the image with the dot
cv2.imwrite('location.png', image)
cv2.waitKey(0)
cv2.destroyAllWindows()