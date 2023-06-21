from test import LidarX2
import time
import numpy
import cv2
import math
lidar = LidarX2("/dev/ttyUSB0")  # Name of the serial port, can be /dev/tty*, COM*, etc.
def calcPos(posX, posY, rotation, distance):
    y_Offset = math.cos(rotation * 3.14159265359 / 180) * (distance*1000)
    x_Offset = math.sin(rotation * 3.14159265359 / 180) * (distance*1000)
    posX += x_Offset
    posY += -y_Offset
    return (int(posX)-100, int(posY)-100)
count=0
while True:
    if not lidar.open():
        print("Cannot open lidar")
        exit(1)
    t = time.time()
    lijst=[]
    for i in range(15):
        measures = lidar.getMeasures()  # Get latest lidar measures
        if len(measures)>=270:
            lijst.extend(measures)
            measures=[]
        time.sleep(0.015)
    lidar.close()
    distance=[]
    degrees=[]
    img = numpy.ones((200, 350))
    img*=0.7
    for i in lijst:
        x=str(i).split(":")
        if float(float(x[1].split("mm")[0]))!=0:    
            degrees.append(float(x[0]))
            distance.append(float(x[1].split("mm")[0]))
    for i in range(0, len(distance)-1):
        distance[i] = distance[i] / 30000
    for i in range(0, len(degrees)-1):
        img = cv2.line(img, (100, 100), calcPos(200, 200, degrees[i], distance[i]), (1, 1, 1), 2)
        img = cv2.circle(img, calcPos(200, 200, degrees[i], distance[i]), 1, (0, 0, 0), 2)


    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        count+=1
        cv2.imwrite("test_pictures"+'/'+str(count)+".png",255*img)

    cv2.waitKey(1)