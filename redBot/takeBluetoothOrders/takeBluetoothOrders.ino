#include <RedBot.h>

// Instantiate the motors.
RedBotMotors motors;

// Instantiate the sensors.
RedBotSensor leftSensor = RedBotSensor(A3);
RedBotSensor middleSensor = RedBotSensor(A2);
RedBotSensor rightSensor = RedBotSensor(A7);

String leftWheel = "0";
char delimeter(',');
String rightWheel = "0";
char endOrders('$');

int waitBetweenOrders = 1000; // milliseconds
const int sensorThreshold = 600;
bool obeyBlindly = true;

void setup() {
  // Start serial port at 9600 bps
  Serial.begin(9600);
  Serial.println("Setup complete");
}

void loop() {
  // If we run into a mousetrap or line, stop and tell the brain
  if (obeyBlindly && (leftSensor.read() < sensorThreshold || middleSensor.read() < sensorThreshold || rightSensor.read() < sensorThreshold)) {
    motors.brake();
    obeyBlindly = false;
    Serial.println("YOU LIED TO ME!!!");
    Serial.write("DANGER");
  }
  
  // If there are orders from the brain, do them (most of the time)
  if (Serial.available() > 0) {
    leftWheel = Serial.readStringUntil(delimeter);
    rightWheel = Serial.readStringUntil(endOrders);
    if (obeyBlindly || (leftWheel.toInt() <= 0 && rightWheel.toInt() <= 0)) {
      obeyBlindly = true;
      Serial.println("Left wheel: " + leftWheel + "    Right wheel: " + rightWheel);
      motors.leftDrive(leftWheel.toInt());
      motors.rightDrive(rightWheel.toInt());
      delay(waitBetweenOrders);
    }
    else {
      Serial.println("I'm not listening to you . . . ");
    }
  }
}
