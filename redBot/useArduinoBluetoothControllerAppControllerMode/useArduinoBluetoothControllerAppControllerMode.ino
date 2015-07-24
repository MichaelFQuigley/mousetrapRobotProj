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
      case 'u': // up
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
      case 'd': // down
        motors.drive(-175);
        break;
    }
    delay(100);
  }
  else {
    motors.brake();
  }
}
