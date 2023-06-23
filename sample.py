from test import LidarX2
import time
import numpy
import cv2
import math
count=0
lidar = LidarX2("/dev/ttyUSB0")  # Name of the serial port, can be /dev/tty*, COM*, etc.
def calcPos(posX, posY, rotation, distance):
    y_Offset = math.cos(rotation * 3.14159265359 / 180) * (distance*200)
    x_Offset = math.sin(rotation * 3.14159265359 / 180) * (distance*200)
    posX += x_Offset
    posY += -y_Offset
    return (int(posX)-300, int(posY)-300)

# if not lidar.open():
#         print("Cannot open lidar")
#         exit(1)
lijst=[]

while lidar.open():
    #starts the lidar

    #reads the lidar data and saves it in a list
    for i in range(20):
        measures = lidar.getMeasures()  # Get latest lidar measures
        #if len(measures)>=270:
        lijst.extend(measures)
        measures=[]
        time.sleep(0.015)
    lidar.close()
    # print(lijst)

    distance=[]
    degrees=[]
    img = numpy.ones((600, 600))
    img*=0.392
    # print(f"{img}")
    #print(len(lijst))
    #this makes 2 seperate lists, one with the degrees and one with the distance
    for i in lijst:
        x=str(i).split(":")
        if float(float(x[1].split("mm")[0]))!=0 and float(x[0])>0 :    
            degrees.append(float(x[0]))
            distance.append(float(x[1].split("mm")[0]))
    #this makes mm to pixels between the middle and points
    for i in range(0, len(distance)-1):
        distance[i] = distance[i] / 2000
    #this draws the lines and points    
    # img = numpy.ones((300, 300))

    for i in range(0, len(degrees)-1):
        img = cv2.line(img, (300, 300), calcPos(600, 600, degrees[i], distance[i]), (1, 1, 1), 3)
        img = cv2.circle(img, calcPos(600, 600, degrees[i], distance[i]), 1, (0, 0, 0), 3)
    #this shows the image
    cv2.imshow("Image", img)
    lijst.clear()
    #this saves the image if a button is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        count+=1
        img = cv2.resize(img, (90,90))
        cv2.imwrite("rechtsonder"+'/'+str(count)+".png",255*img)

    if cv2.waitKey(1) & 0xFF == ord('e'):
        resized = cv2.resize(img, (90,90))

    cv2.waitKey(1)