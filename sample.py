from test import LidarX2
import time
import numpy
import cv2
import math
lidar = LidarX2("/dev/ttyUSB0")  # Name of the serial port, can be /dev/tty*, COM*, etc.

def calcPos(posX, posY, rotation, distance):
    y_Offset = math.cos(rotation * 3.14159265359 / 180) * (distance*200)
    x_Offset = math.sin(rotation * 3.14159265359 / 180) * (distance*200)
    posX += x_Offset
    posY += -y_Offset
    return (int(posX)-320, int(posY)-240)


if not lidar.open():
    print("Cannot open lidar")
    exit(1)

t = time.time()
# while time.time() - t < 0.5:  # Run for 20 seconds
lijst=[]
for i in range(22):
    measures = lidar.getMeasures()  # Get latest lidar measures
    # print(measures)
    # print(len(measures))    
    if len(measures)>=270:
        lijst.extend(measures)
        # measures=[]    
    time.sleep(0.015)

# print(lijst)
# print(len(lijst))
img = numpy.ones((480, 640))
lidar.close()
for i in lijst:
    x=str(i).split(":")    
    degree=float(x[0])
    distance=float(x[1].split("mm")[0])
    print(f"afstand is {distance} en degree is {degree} \n")
    img = cv2.circle(img, calcPos(640, 480, degree, distance), 1, (0, 0, 0), 2)

cv2.imshow("Image", img)
cv2.waitKey(0)

print(degree)
print(distance)
print(img)

