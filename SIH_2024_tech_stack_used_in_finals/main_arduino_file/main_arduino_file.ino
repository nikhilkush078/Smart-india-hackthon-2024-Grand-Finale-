int motor1f = 2;
int motor2f = 3;
int motor1b = 4;
int motor2b = 5;

void setup(){
  pinMode(motor1f, OUTPUT);
  pinMode(motor2f, OUTPUT);
  pinMode(motor1b, OUTPUT);
  pinMode(motor2f, OUTPUT); 
}
void loop(){
  if (Serial.available() > 0){
    char command = Serial.read();
    if (command = 'w'){
      digitalWrite(motor1f, HIGH);
    }else if (command = 's'){
      digitalWrite(motor1b, HIGH);
    }else if (command = 'a'){
      digitalWrite(motor2f, HIGH);
    }else if (command = 'd'){
      digitalWrite(motor2b, HIGH);
    }
  }delay(50);
}