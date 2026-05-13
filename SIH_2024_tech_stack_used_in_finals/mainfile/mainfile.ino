#include <Servo.h>

// Define pins for the outputs
const int pin3 = 3;
const int pin4 = 4;
const int pin5 = 5;
const int pin6 = 6;

// Servo motor setup
Servo myServo;
int servoAngle = 90; // Start at the middle position (90°)
const int servoPin = 9;

// Variable to store the last command
char lastCommand = '\0';

void setup() {
  Serial.begin(9600); // Initialize serial communication

  // Set pins as outputs
  pinMode(pin3, OUTPUT);
  pinMode(pin4, OUTPUT);
  pinMode(pin5, OUTPUT);
  pinMode(pin6, OUTPUT);

  // Initialize all outputs to LOW
  digitalWrite(pin3, LOW);
  digitalWrite(pin4, LOW);
  digitalWrite(pin5, LOW);
  digitalWrite(pin6, LOW);

  // Attach the servo to the servo pin
  myServo.attach(servoPin);
  myServo.write(servoAngle); // Set the initial servo position
}

void loop() {
  if (Serial.available()) {
    char input = Serial.read(); // Read the input from the serial monitor

    // If the same command is given again, turn off all outputs
    if (input == lastCommand && input != '+' && input != '-') {
      resetOutputs(); // Turn off all outputs
      lastCommand = '\0'; // Reset the last command
    } else {
      // Handle new commands
      resetOutputs(); // Turn off all previous outputs
      lastCommand = input; // Update the last command

      // Handle command 'f': Turn on pins 3 and 4
      if (input == 'f') {
        digitalWrite(pin3, HIGH);
        digitalWrite(pin4, HIGH);
      }
      // Handle command 'b': Turn on pins 5 and 6
      else if (input == 'b') {
        digitalWrite(pin5, HIGH);
        digitalWrite(pin6, HIGH);
      }
      // Handle command 'l': Turn on pin 3
      else if (input == 'l') {
        digitalWrite(pin3, HIGH);
      }
      // Handle command 'r': Turn on pin 4
      else if (input == 'r') {
        digitalWrite(pin4, HIGH);
      }
      // Handle command '+': Rotate servo clockwise by 10°
      else if (input == '+') {
        servoAngle = constrain(servoAngle + 30, 0, 180); // Limit the angle to 0-180°
        myServo.write(servoAngle);
      }
      // Handle command '-': Rotate servo counterclockwise by 10°
      else if (input == '-') {
        servoAngle = constrain(servoAngle - 30, 0, 180); // Limit the angle to 0-180°
        myServo.write(servoAngle);
      }
    }
  }
}

// Function to reset all outputs to LOW
void resetOutputs() {
  digitalWrite(pin3, LOW);
  digitalWrite(pin4, LOW);
  digitalWrite(pin5, LOW);
  digitalWrite(pin6, LOW);
}
