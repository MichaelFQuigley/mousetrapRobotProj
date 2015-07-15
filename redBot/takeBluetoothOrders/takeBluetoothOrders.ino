#define    L_CTRL1   2
#define    L_CTRL2   4
#define    L_PWM     5

#define    R_CTRL1   7
#define    R_CTRL2   8
#define    R_PWM     6

String leftWheel = "0";
char delimeter(',');
String rightWheel = "0";
char endOrders('$');
int waitBetweenOrders = 1000; // milliseconds

void setup() {
  // Start serial port at 9600 bps
  Serial.begin(9600);
  pinMode(L_CTRL1, OUTPUT);
  pinMode(L_CTRL2, OUTPUT);
  pinMode(L_PWM, OUTPUT);
  pinMode(R_CTRL1, OUTPUT);
  pinMode(R_CTRL2, OUTPUT);
  pinMode(R_PWM, OUTPUT);
}

void loop() {
  // If there are updated orders from the brain, do them
  if (Serial.available() > 0) {
    leftWheel = Serial.readStringUntil(delimeter);
    rightWheel = Serial.readStringUntil(endOrders);
    Serial.println("Left wheel: " + leftWheel + "    Right wheel: " + rightWheel);
    leftMotor(leftWheel.toInt());
    rightMotor(rightWheel.toInt());
    delay(waitBetweenOrders);
  }
}

void leftMotor(int motorPower)
{
  motorPower = constrain(motorPower, -255, 255);   // constrain motorPower to -255 to +255
  if(motorPower >= 0)
  {
    digitalWrite(L_CTRL1, HIGH);
    digitalWrite(L_CTRL2, LOW);
    analogWrite(L_PWM, abs(motorPower));
  }
  else
  {
    digitalWrite(L_CTRL1, LOW);
    digitalWrite(L_CTRL2, HIGH);
    analogWrite(L_PWM, abs(motorPower));
  }
}

void rightMotor(int motorPower)
{
  motorPower = constrain(motorPower, -255, 255);   // constrain motorPower to -255 to +255
  if(motorPower <= 0)
  {
    digitalWrite(R_CTRL1, HIGH);
    digitalWrite(R_CTRL2, LOW);
    analogWrite(R_PWM, abs(motorPower));
  }
  else
  {
    digitalWrite(R_CTRL1, LOW);
    digitalWrite(R_CTRL2, HIGH);
    analogWrite(R_PWM, abs(motorPower));
  }
}
