# Positie-Bepaling
## Description
The Position Determination System is a Python program that uses LiDAR technology to estimate the position of an movign vehicle in a given environment. The system collects data from the LiDAR sensor, applies a position estimation algorithm, and provides the coordinates of the object.

## Requirements
* Python version [3.9.x](https://www.python.org/downloads/release/python-392/) or higher (3.9.2 is the recommended version)
* Installation of [requirements.txt](requirements.txt)
* The [YDLidar Library](https://github.com/nesnes/YDLidarX2_python)

## Hardware requirements
* [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
* [YDLidar X2](https://www.ydlidar.com/products/view/6.html)
* [gyroscope MPU6050](https://www.amazon.nl/ARCELI-versnellingsmeter-gyroscoop-versnellingssensor-gegevensuitgang/dp/B07BVXN2GP/ref=asc_df_B07BVXN2GP/?tag=nlshogostdde-21&linkCode=df0&hvadid=430548884871&hvpos=&hvnetw=g&hvrand=10590259427188414527&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9063545&hvtargid=pla-928293154057&psc=1)

## Installation
1. Download and install raspberry Pi OS using the following guide:
    https://www.raspberrypi.com/documentation/computers/getting-started.html
2. Set resolution to 1536x864
    - using Raspberry Pi OS
        - open a Terminal window using ```Ctrl+Alt+T``` and type in `sudo nano /etc/xdg/autostart/vnc_xrandr.desktop` and edit `1920 1080` to `1536 864`.<br />
        This is the default resolution used for this program and must be set for it to work propperly.
    - using Windows
        - set resolution to 1920x1080 with a scaling of 125%
3. Download and install Python
4. Clone the repository 
```
git clone https://github.com/R2D2-2023/Positie-Bepaling
```
5. install the required libraries
``` 
git clone https://github.com/nesnes/YDLidarX2_python
```
```
pip install -r requirements.txt
```
## Usage
To run the code to determine the position, follow these instructions:
1.  go to the command line( Terminal ). ```Ctrl+Alt+T```
2.  go to the folder where the code is located ```cd **path/to/your/repository**```
3.  Run ```python main.py```

For more code regarding this project see: [M3-S Project](https://github.com/orgs/R2D2-2023/repositories) 

## Authors:
- [@Boehmer2003](https://github.com/Boehmer2003) - Team Lead 
- [@northernlakeNL](https://github.com/northernlakeNL) - Technical Lead
- [@Ilias-a](https://github.com/Ilias-a) - Product Owner
- [@Tjees](https://github.com/Tjees) - Developer
### Contributors:
- [@BasvandenBergh](https://github.com/BasvandenBergh) - Team Lead [Team Mappig](https://github.com/R2D2-2023/Mapping)
- [@jamesonLin](https://www.github.com/jamesonLin) - Technical Lead [Team Mappig](https://github.com/R2D2-2023/Mapping)
- [@Jorismaas](https://github.com/Jorismaas) - Product Owner [Team Mappig](https://github.com/R2D2-2023/Mapping)
- [@JSaurusRex](https://github.com/JSaurusRex) - Developer [Team Mappig](https://github.com/R2D2-2023/Mapping)
- [@LukkenS-HU](https://github.com/LukkenS-HU) - Developer [Team Mappig](https://github.com/R2D2-2023/Mapping)

## License
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## Acknowledgements
- The Lidar library was made by [nesnes](https://github.com/nesnes), this made it possible to do our project the way we wanted to.
- [OpenCV Library](https://docs.opencv.org/3.4/index.html)
- [Numpy Library](https://numpy.org/doc/stable/)
- The project was made possible by [The university of applied science Utrecht](https://www.internationalhu.com/)
- The project was guided by:
    - [Harm Snippe](https://github.com/orgs/R2D2-2023/people/n0harm) (Teacher)
    - [Leo Jenneskens](https://github.com/orgs/R2D2-2023/people/leojenns) (Teacher)
    - [Kevin Patist](https://github.com/orgs/R2D2-2023/people/KevinPatist) (teaching assistant)
    - [Jari Fuijkschot](https://github.com/orgs/R2D2-2023/people/JariKanarie) (teaching assistant)
    - [Gianluca Piccardo](https://github.com/orgs/R2D2-2023/people/Gian1080) (teaching assistant)