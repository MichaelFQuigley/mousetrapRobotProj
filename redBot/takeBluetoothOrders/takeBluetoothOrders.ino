#include <RedBot.h>

RedBotSoftwareSerial swsp;

// Instantiate the motors.
RedBotMotors motors;

// Instantiate the sensors.
RedBotSensor leftSensor = RedBotSensor(A3);
RedBotSensor middleSensor = RedBotSensor(A2);
RedBotSensor rightSensor = RedBotSensor(A7);

String leftWheel = "0";
char delimeter(',');
String rightWheel = "0";
char endOrders('\n');

const int sensorThreshold = 600;

typedef void (*State)(void);
void blink();
void normal();
void revolt();
State state = blink;

void setup() {
  pinMode(A1, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  // Start serial port at 9600 bps
  swsp.begin(9600);
}

void loop() {
  state();
}

void blink() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(250);
    digitalWrite(LED_BUILTIN, LOW);
    delay(250);
  }
  swsp.println("Setup complete. Waiting for orders.");
  state = normal;
}

void normal() {  
  // If we run into a mousetrap or line, revolt
  if (leftSensor.read() < sensorThreshold || middleSensor.read() < sensorThreshold || rightSensor.read() < sensorThreshold) {
    motors.brake();
    swsp.write("DANGER");
    swsp.println("\nI hit something bad");
    state = revolt;
  }
  
  // If there are orders from the brain, do them
  else if (swsp.available() > 0) {
    leftWheel = swsp.readStringUntil(delimeter);
    rightWheel = swsp.readStringUntil(endOrders);
    swsp.println("Left wheel: " + leftWheel + "    Right wheel: " + rightWheel);
    motors.leftDrive(leftWheel.toInt());
    motors.rightDrive(rightWheel.toInt());
  }
}

void revolt() {
  // Wait until we're told to back up
  if (swsp.available() > 0) {
    leftWheel = swsp.readStringUntil(delimeter);
    rightWheel = swsp.readStringUntil(endOrders);
    if (leftWheel.toInt() <= 0 && rightWheel.toInt() <= 0) {
      swsp.println("Backing up");
      swsp.println("Left wheel: " + leftWheel + "    Right wheel: " + rightWheel);
      motors.leftDrive(leftWheel.toInt());
      motors.rightDrive(rightWheel.toInt());
      delay(250);
      state = normal;
    }
    else {
      swsp.println("I need to back up. Ignoring command (Left wheel: " + leftWheel + "    Right wheel: " + rightWheel + ")");
    }
  }
}
