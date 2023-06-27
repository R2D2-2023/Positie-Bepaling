#include <Wire.h>
#include <MPU6050.h>
#include <math.h>

MPU6050 mpu; // Maak nieuw MPU opbject aan.

// Timers, gebruikt om snelheid van gyro over tijd te bepalen (aanpassen bij andere delays).
float timeStep = 0.01; // Zet de timer.

// Alle standaard waardes instellen.
float pitch = 0.0; // Rotatie X-as.
float roll = 0.0; // Rotatie Y-as.
float yaw = 0.0; // Rotatie Z-as.
float result = 0.0; // Gyro waarde omgezet naar graden.
double posX = 320.0; // X-positie op de map.
double posY = 240.0; // Y-positie van de map.
double angle = 0.0; // Gyro waarde in graden.
bool moving = false; // Bool voor als de gyro beweegt.
float calibration_number = 1.125; // Kalibratiegetal voor gyro.
double speed = 0.03; // Standaard snelheid robot.
const int buttonPin = 7; // Pin voor test knop om rijden te simuleren.
int loops; // Aantal loops dat gyro data is geüpdated.

// Setup code.
void setup() 
{
  Serial.begin(9600); // Begin serial monitor.

  pinMode(buttonPin, INPUT); // Stel rij knop in.

  // Initialiseer de gyro sensor.
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  
  // Calibreer gyro om drift te voorkomen.
  mpu.calibrateGyro();

  // Stel de sensitiviteit van de gyro in.
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

// Reset alle waarden naar de standaard waarden.
void reset() {
  pitch = 0; // Reset X-as.
  roll = 0; // Reset Y-as.
  yaw = 0; // Reset Z-as.
  posX = 320; // Reset X positie.
  posY = 240; // Reset Y positie.
}

// Update de positie van de gyro.
void updatePosition( float rotation ) {
    double y_Offset = cos(rotation * 3.14159265359 / 180) * speed; // Bereken de Y offset van het middenpunt van de gyro op basis van de angle van de gyro.
    double x_Offset = sin(rotation * 3.14159265359 / 180) * speed;// Bereken de X offset van het middenpunt van de gyro op basis van de angle van de gyro.
    posX += x_Offset; // Update de X positie.
    posY += -y_Offset;// Update de Y positie.
}

// Stuur de positie data via de serial monitor.
void sendPosition() {
  Serial.print((int)posX); // Stuur de X positie via serial.
  Serial.print(',');
  Serial.print((int)posY); // Stuur de Y positie via serial.
  Serial.print(',');
  Serial.println((int)angle); // Stuur de angle via serial.
}

// Stuur de rauwe Yaw data via de serial monitor.
void sendYaw() {
  Serial.println(yaw); // Stuur de yaw waarde.
}

// Stuur de angle waarde die de geconverteerde Yaw waarde naar 0-360 graden is.
void sendAngle() {
  Serial.println(angle);
}

// Stuur een kompas waarde op basis van de angle waarde.
void sendCompass( float rotation ) {
    if( angle < 45 || angle > 315 ) { // Kijk of de angle naar het noorden wijst.
      Serial.println("N"); // Stuur de letter N via de serial monitor.
    }
    else if(angle > 45 && angle < 135 ) { // Kijk of de angle naar het oosten wijst.
      Serial.println("E"); // Stuur de letter E via de serial monitor.
    }
    else if(angle > 135 && angle < 225 ) { // Kijk of de angle naar het zuiden wijst.
      Serial.println("S"); // Stuur de letter S via de serial monitor.
    }
    else if(angle > 225 && angle < 315 ) { // Kijk of de angle naar het westen wijst.
      Serial.println("W"); // Stuur de letter W via de serial monitor.
    }
}

void updateRotation() {
  // Vraag de mpu waardes op en geef ze genormaliseerd terug.
  Vector norm = mpu.readNormalizeGyro();

  // Bereken de Pitch, Roll en Yaw (X, Y en Z) waarden op basis van de draaisnelheid van de sensor en de timestep waarde.
  pitch = pitch + norm.YAxis * timeStep; // Bereken de pitch (X).
  roll = roll + norm.XAxis * timeStep; // Bereken de pitch (Y).
  yaw = yaw + norm.ZAxis * timeStep; // Bereken de pitch (Z).
    
  // Serial.println( (yaw*-1)*0.625 );
  // Serial.print(", ");
  // Serial.println(inDegrees((yaw*-1)*0.625));

  angle = inDegrees((yaw*-1)*calibration_number); // Geef de geïnverteerde Yaw waarde mee aan de inDegrees functie om 0-360 graden terug te krijgen en dit in de angle waarde te zetten.
  // Move(angle);
}

// Vraag positie data op.
double getPosition() {
  return posX, posY, angle;
}

// Main loop.
void loop()
{
  updateRotation(); // Vraag nieuwe rotatie waarden op van de gyro sensor.

  // Check of de rij knop wordt ingedrukt.
  if( digitalRead(buttonPin) == HIGH ){
    updatePosition(angle);
  }

  // Check of er 10 update loops (100ms) voorbij zijn gegaan.
  if( loops == 10 ) {
    // sendPosition();
    // sendAngle();
    sendCompass(angle); // Stuur de kompas waarden.
    loops = 0; // Zet de loops weer terug naar 0.
  }

  // Update de loops.
  loops += 1;
  delay(10); // Wacht 10 ms met updaten.
}