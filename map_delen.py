import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def rotateImage(image, angle):
    row, col = image.shape
    center = tuple(np.array([col, row]) / 2)  # Corrected order of dimensions
    rot_mat = cv.getRotationMatrix2D(center, angle, 1.0)
    new_image = cv.warpAffine(image, rot_mat, (col, row))
    return new_image

img = cv.imread('map/map.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
img2 = img.copy()

template = cv.imread('map/linksonder2.png', cv.IMREAD_GRAYSCALE)
template = cv.resize(template, (int(template.shape[1] * 1), int(template.shape[0] * 1)))

assert template is not None, "file could not be read, check with os.path.exists()"
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
           'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

threshold = 0.5

for rotation in range(0, 360, 180):
    rotated_template = rotateImage(template, rotation)
    for meth in methods:
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img, rotated_template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        
plt.imshow(img, cmap='gray')
plt.title('Detected Point')
plt.show()