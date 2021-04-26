
/*
   Arduino based SCARA Robot 
   by Dejan, www.HowToMechatronics.com
   AccelStepper: http://www.airspayce.com/mikem/arduino/AccelStepper/index.html

*/
#include <AccelStepper.h>
#include <Servo.h>
#include <math.h>

#define limitSwitch1 11
#define limitSwitch2 10

#define limitSwitch4 A3

// Define the stepper motors and the pins the will use
AccelStepper stepper1(1, 2, 5); // (Type:driver, STEP, DIR)



Servo gripperServo;  // create servo object to control a servo


double x = 10.0;
double y = 10.0;
double L1 = 228; // L1 = 228mm
double L2 = 136.5; // L2 = 136.5mm
double theta1, z;

int stepper1Position, stepper2Position, stepper3Position, stepper4Position;

const float theta1AngleToSteps = 10;


byte inputValue[5];
int k = 0;

String content = "";
int data[100];

int theta1Array[100];
int gripperArray[100];
int positionsCounter = 0;

void setup() {
  Serial.begin(115200);

  pinMode(limitSwitch1, INPUT_PULLUP);


  // Stepper motors max speed
  stepper1.setMaxSpeed(4000);
  stepper1.setAcceleration(2000);

   gripperServo.attach(A0, 600, 2500);
  data[4] = 0;
  gripperServo.write(data[4]);
  delay(3000);

  homing();
}

void loop() {

  if (Serial.available()) {
    content = Serial.readString(); // Read the incomding data from Processing
    Serial.println(content);
    for (int i = 0; i < 100; i++) {
      int index = content.indexOf(","); // locate the first ","
      data[i] = atol(content.substring(0, index).c_str()); //Extract the number from start to the ","
      content = content.substring(index + 1); //Remove the number from the string
    }
    
    if(data[0]!= 1){
      Serial.println(data[8]);
      theta1Array[positionsCounter] = data[1] * theta1AngleToSteps; //store the values in steps = angles * angleToSteps variable
      positionsCounter++;
    }
    if(data[0] == 1){
      gripperServo.write(data[4]);
      theta1Array[positionsCounter] = data[1] * theta1AngleToSteps; //store the values in steps = angles * angleToSteps variable
      positionsCounter++;
      stepper1.setSpeed(data[2]);
      stepper1.setAcceleration(data[3]);

    // execute the stored steps
    for (int i = 0; i <= positionsCounter - 1; i++) {
     
      stepper1.moveTo(theta1Array[i]);
      while (stepper1.currentPosition() != theta1Array[i] ) {
        stepper1.run();

      }
 }
  
      // Clear the array data to 0
      memset(theta1Array, 0, sizeof(theta1Array));
      positionsCounter = 0;
    
    
  }

}
}
void serialFlush() {
  while (Serial.available() > 0) {  //while there are characters in the serial buffer, because Serial.available is >0
    Serial.read();         // get one character
  }
}


void homing() {

  // Homing Stepper1
  while (digitalRead(limitSwitch1) != 1) {
    stepper1.setSpeed(-1100);
    stepper1.runSpeed();
    stepper1.setCurrentPosition(-1662); // When limit switch pressed set position to 0 steps
  }
  delay(20);

  stepper1.moveTo(0);
  while (stepper1.currentPosition() != 0) {
      stepper1.run();
  }
}
