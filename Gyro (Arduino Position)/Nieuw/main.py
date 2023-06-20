import numpy as np
import cv2
import time
import serial

posX = 0
posY = 0
Angle = 0

arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.3)

while True:
    data = arduino.readline().decode()
    if data != '':
        posX = int(data.split(",")[0])
        posY = int(data.split(",")[1])
        Angle = int(data.split(",")[2])
        print(str(posX) + ', ' + str(posY) + ', ' + str(Angle))

    img = cv2.imread("./Map.png")

    image = cv2.circle(img, (posX, posY), 3, (255, 0, 0), 2)

    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()