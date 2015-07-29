#include <RedBot.h>

RedBotSoftwareSerial swsp;

// Instantiate the motors.
RedBotMotors motors;

// Instantiate the sensors.
RedBotSensor leftSensor = RedBotSensor(A3);
RedBotSensor middleSensor = RedBotSensor(A2);
RedBotSensor rightSensor = RedBotSensor(A7);

int leftWheel = 0;
char delimeter(',');
int rightWheel = 0;
char endOrders('\n');

const int sensorThreshold = 500;

typedef void (*State)(void);
void normal();
void revolt();
State state = normal;

void setup() {
  pinMode(A1, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  // Start serial port at 9600 bps
  swsp.begin(9600);
  for (int i = 0; i < 4; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(250);
    digitalWrite(LED_BUILTIN, LOW);
    delay(250);
  }
  swsp.println("Setup complete. Waiting for orders.");
}

void loop() {
  state();
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
    getUpdatedOrders();
    executeOrders();
  }
}

void revolt() {
  // Wait until we're told to back up
  if (swsp.available() > 0) {
    getUpdatedOrders();
    if (leftWheel <= 0 && rightWheel <= 0) {
      swsp.println("Backing up");
      executeOrders();
      delay(250);
      state = normal;
    }
    else {
      swsp.println("I need to back up. Ignoring command (Left wheel: " + String(leftWheel) + "    Right wheel: " + String(rightWheel) + ")");
    }
  }
}

void getUpdatedOrders() {
  leftWheel = swsp.readStringUntil(delimeter).toInt();
  rightWheel = swsp.readStringUntil(endOrders).toInt();
}

void executeOrders() {
  swsp.println("Left wheel: " + String(leftWheel) + "    Right wheel: " + String(rightWheel));
  motors.leftDrive(leftWheel);
  motors.rightDrive(rightWheel);
}

