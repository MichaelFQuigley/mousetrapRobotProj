#include <RedBot.h>

// Instantiate the motors.
RedBotMotors motors;

RedBotSoftwareSerial swsp;

char incomingByte;

void setup() {
  pinMode(A1, INPUT_PULLUP);
  // Start serial port at 9600 bps
  swsp.begin(9600);
}

void loop() {
  if (swsp.available() > 0) {
    incomingByte = swsp.read();
    switch (incomingByte) {
      case 's': // stop
        motors.brake();
        break;
      case 'f': // front
        motors.leftDrive(240); // This tries to compensate for the redbot not driving straight
        motors.rightDrive(255);
        break;
      case 'l': // left
        motors.leftDrive(-100);
        motors.rightDrive(100);
        break;
      case 'r': // right
        motors.leftDrive(100);
        motors.rightDrive(-100);
        break;
      case 'b': // back
        motors.drive(-175);
        break;
      case 'w': // front left
        motors.leftDrive(175);
        motors.rightDrive(255);
        break;
      case 'x': // front right
        motors.leftDrive(240);
        motors.rightDrive(175);
        break;
      case 'y': // back left
        motors.leftDrive(-100);
        motors.rightDrive(-175);
        break;
      case 'z': // back right
        motors.leftDrive(-175);
        motors.rightDrive(-100);
        break;
    }
  }
}
