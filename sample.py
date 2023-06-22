from test import LidarX2
import time
import numpy
import cv2
import math
count=0
lidar = LidarX2("/dev/ttyUSB0")  # Name of the serial port, can be /dev/tty*, COM*, etc.
def calcPos(posX, posY, rotation, distance):
    y_Offset = math.cos(rotation * 3.14159265359 / 180) * (distance*1000)
    x_Offset = math.sin(rotation * 3.14159265359 / 180) * (distance*1000)
    posX += x_Offset
    posY += -y_Offset
    return (int(posX)-150, int(posY)-150)


while True:
    #starts the lidar
    if not lidar.open():
        print("Cannot open lidar")
        exit(1)

    lijst=[]
    #reads the lidar data and saves it in a list

    for i in range(15):
        measures = lidar.getMeasures()  # Get latest lidar measures
        if len(measures)>=270:
            lijst.extend(measures)
            measures=[]
        time.sleep(0.015)
    lidar.close()


    distance=[]
    degrees=[]
    img = numpy.ones((300, 300))
    img*=0.7
    #this makes 2 seperate lists, one with the degrees and one with the distance
    for i in lijst:
        x=str(i).split(":")
        if float(float(x[1].split("mm")[0]))!=0:    
            degrees.append(float(x[0]))
            distance.append(float(x[1].split("mm")[0]))
    #this makes mm to pixels between the middle and points
    for i in range(0, len(distance)-1):
        distance[i] = distance[i] / 30000
    #this draws the lines and points
    for i in range(0, len(degrees)-1):
        img = cv2.line(img, (150, 150), calcPos(300, 300, degrees[i], distance[i]), (1, 1, 1), 6)
        img = cv2.circle(img, calcPos(300, 300, degrees[i], distance[i]), 1, (0, 0, 0), 6)
    #this shows the image
    cv2.imshow("Image", img)
    #this saves the image if a button is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        count+=1
        cv2.imwrite("test_pictures"+'/'+str(count)+".png",255*img)

    cv2.waitKey(1)