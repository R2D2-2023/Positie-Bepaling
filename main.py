# import cv2
# import numpy
# import math
#
# def calcPos(posX, posY, rotation, distance):
#     y_Offset = math.cos(rotation * 3.14159265359 / 180) * (distance*200)
#     x_Offset = math.sin(rotation * 3.14159265359 / 180) * (distance*200)
#     posX += x_Offset
#     posY += -y_Offset
#     return (int(posX)-320, int(posY)-240)
#
# data = []
#
# with open("./mock_data_lidar.txt",'r') as file:
#     for line in file:
#         data = line
#
# data = data.replace(" ", "")
# data = data.replace("m", "")
# data = data.split(",")
# print(len(data))
#
# angle = []
# distance = []
#
# for i in data:
#     d = i.split(":")
#     angle.append(float(d[0]))
#     distance.append(float(d[1]))
#
# for i in range(0, len(distance)-1):
#     distance[i] = distance[i] / max(distance)
#
# img = numpy.ones((480, 640))
#
# for i in range(0, len(angle)-1):
#     img = cv2.circle(img, calcPos(640, 480, angle[i], distance[i]), 1, (0, 0, 0), 2)
#
# cv2.imshow("Image", img)
# cv2.waitKey(0)
#
# print(data)
# print(angle)
# print(distance)
# print(img)

import cv2
import numpy
import math

def calcPos(posX, posY, rotation, distance):
    y_Offset = math.cos(rotation * 3.14159265359 / 180) * (distance*400)
    x_Offset = math.sin(rotation * 3.14159265359 / 180) * (distance*400)
    posX += x_Offset
    posY += -y_Offset
    return (int(posX)-320, int(posY)-240)

data = []

with open("./mock_data_lidar.txt",'r') as file:
    for line in file:
        data = line

data = data.replace(" ", "")
data = data.replace("m", "")
data = data.split(",")
print(len(data))

angle = []
distance = []

for i in data:
    d = i.split(":")
    angle.append(float(d[0]))
    distance.append(float(d[1]))

for i in range(0, len(distance)-1):
    distance[i] = distance[i] / 10000

img = numpy.ones((480, 640))
img *= 0.7

for i in range(0, len(angle)-1):
    img = cv2.line(img, (320, 240), calcPos(640, 480, angle[i], distance[i]), (1, 1, 1), 2)
    img = cv2.circle(img, calcPos(640, 480, angle[i], distance[i]), 1, (0, 0, 0), 2)

print(img.shape)
cv2.imshow("Image", img)
# opencv_rgb_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
img *= 255
cv2.imwrite("img.png", img)
cv2.waitKey(0)

print(data)
print(angle)
print(distance)
print(img)