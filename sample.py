from test import LidarX2
import time

lidar = LidarX2("/dev/ttyUSB0")  # Name of the serial port, can be /dev/tty*, COM*, etc.

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
    time.sleep(0.015)
    if len(measures)>=270:
        lijst.extend(measures)
        measures=[]
print(lijst)
print(len(lijst))
lidar.close()

for i in lijst:
    x=str(i).split(":")    
    degree=float(x[0])
    distance=float(x[1].split("mm")[0])
    print(f"afstand is {distance} en degree is {degree} \n")

