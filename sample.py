from test import LidarX2
import time
import numpy
import cv2
import math
lidar = LidarX2("/dev/ttyUSB0")  # Name of the serial port, can be /dev/tty*, COM*, etc.

def calcPos(posX, posY, rotation, distance):
    y_Offset = math.cos(rotation * 3.14159265359 / 180) * (distance*400)
    x_Offset = math.sin(rotation * 3.14159265359 / 180) * (distance*400)
    posX += x_Offset
    posY += -y_Offset
    return (int(posX)-320, int(posY)-240)
count=0
while True:
    if not lidar.open():
        print("Cannot open lidar")
        exit(1)
    t = time.time()
    lijst=[]
    for i in range(22):
        measures = lidar.getMeasures()  # Get latest lidar measures
        if len(measures)>=270:
            lijst.extend(measures)
        time.sleep(0.015)
    lidar.close()
    distance=[]
    degrees=[]
    img = numpy.ones((480, 640))
    for i in lijst:
        x=str(i).split(":")    
        degrees.append(float(x[0]))
        distance.append(float(x[1].split("mm")[0]))
    for i in range(0, len(distance)-1):
        distance[i] = distance[i] / 10000
    for i in range(0, len(degrees)-1):
        img = cv2.circle(img, calcPos(640, 480, degrees[i], distance[i]), 1, (0, 0, 0), 2)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        count+=1
        # for i in img:
            # print(i)
        cv2.imwrite("test_pictures"+'/'+str(count)+".png",255*img)

    cv2.waitKey(1)