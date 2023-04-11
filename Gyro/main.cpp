/*
    MPU6050 Triple Axis Gyroscope & Accelerometer. Pitch & Roll & Yaw Gyroscope Example.
    Read more: http://www.jarzebski.pl/arduino/czujniki-i-sensory/3-osiowy-zyroskop-i-akcelerometr-mpu6050.html
    GIT: https://github.com/jarzebski/Arduino-MPU6050
    Web: http://www.jarzebski.pl
    (c) 2014 by Korneliusz Jarzebski
*/

#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// Timers
float timeStep = 0.01;

// Pitch, Roll and Yaw values
float pitch = 0;
float roll = 0;
float yaw = 0;
float result = 0;

void setup() 
{
  Serial.begin(9600);

  // Initialize MPU6050
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  
  // Calibrate gyroscope. The calibration must be at rest.
  // If you don't want calibrate, comment this line.
  mpu.calibrateGyro();

  // Set threshold sensivty. Default 3.
  // If you don't want use threshold, comment this line or set 0.
  mpu.setThreshold(3);
}

float inDegrees( float yaw ) {
  // Result in degrees.
  // 0 % 360 == 0;
  // 1 % 360 == 1;
  // 360 % 360 == 0;
  // 361 % 360 == 1;
  // 720 % 360 == 0;
  // 721 % 360 == 1;
  // etc.
  result = (int)yaw % 360;

  if( result < 0 ) {
    result += 360;
  }
  
  return result;
}

void reset() {
  pitch = 0;
  roll = 0;
  yaw = 0;
}

void loop()
{
  // Read normalized values
  Vector norm = mpu.readNormalizeGyro();

  if( Serial.read() == 'r' ) {
    reset();
    Serial.println(0);
  }

  // Calculate Pitch, Roll and Yaw
  pitch = pitch + norm.YAxis * timeStep;
  roll = roll + norm.XAxis * timeStep;
  yaw = yaw + norm.ZAxis * timeStep;
  
  // Serial.println( (yaw*-1)*0.625 );
  // Serial.print(", ");
  Serial.println(inDegrees((yaw*-1)*0.625));

  delay(10);
}