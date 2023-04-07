#include <Wire.h>
#include <QMC5883L.h>

QMC5883L compass;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  compass.init();
}

void loop() {
  int x, y, z;
  float headingBuf;

  compass.read(&x, &y, &z);

  float headingRadians = atan2(y, x);
  float headingDegrees = headingRadians * 180 / PI;
  float declinationAngle = 2;

  headingDegrees += declinationAngle;

  if (headingDegrees < 0) {
    headingDegrees += 360;
  }

  if ((int)headingDegrees % 10 == 0) {
    headingBuf = headingDegrees;
  }

  // Serial.print("Heading: ");
  // Serial.print(headingDegrees);
  // Serial.print(" ,");
  Serial.println(headingBuf);

  delay(10);
}