#include "Definitions.h"
#include <Servo.h>

//W0S0A0D0Z0C02030X0.1357Y-0.999T-0.5123R;
String userInput;

bool forward, reverse, lift, sink;
bool twistLeft, twistRight, clawOpen, clawClose;
float yaw, pitch, thrustLevel;
float normThrustLevel = 0;

Servo thruster1, thruster2, thruster3, thruster4, thruster5, thruster6;

void setup() {
  Serial.begin(9600);

  //THRUSTER SETUP
  //pulse width in microseconds
  thruster1.attach(esc1,maxReverse,maxForward);
  thruster2.attach(esc2,maxReverse,maxForward);
  thruster3.attach(esc3,maxReverse,maxForward);
  thruster4.attach(esc4,maxReverse,maxForward);
  thruster5.attach(esc5,maxReverse,maxForward);
  thruster6.attach(esc6,maxReverse,maxForward);

  //TWISTER SETUP
  pinMode(twisterPwm,OUTPUT); 
  pinMode(twisterDir,OUTPUT); 

  //CLAW SETUP
  pinMode(clawStep,OUTPUT); 
  pinMode(clawDir,OUTPUT); 
  
  // write stop to all ESC
  thruster1.writeMicroseconds(stopped);
  thruster2.writeMicroseconds(stopped);
  thruster3.writeMicroseconds(stopped);
  thruster4.writeMicroseconds(stopped);
  thruster5.writeMicroseconds(stopped);
  thruster6.writeMicroseconds(stopped);

  delay(1);
}

void loop() {
  //faster to use line ending character instead of readString()
  if(Serial.available() > 0){
     userInput = Serial.readStringUntil(';');
     Serial.println(userInput);
     parseUserInput(userInput);

     if(twistLeft || twistRight) {
        twisterControl(twistLeft, twistRight);
     } else{
        analogWrite(twisterPwm, twisterStop);
     }

     if (clawOpen || clawClose) {
       clawControl(clawOpen, clawClose);
     } else {
       digitalWrite(clawStep, LOW);
     }
     
     thrusterControl(forward, reverse, lift, sink, yaw, pitch, normThrustLevel); 
      
    //allow time to perform action
     delayMicroseconds(250);
  }
}

void parseUserInput(String userInput){
  /* example input: 
   * W0S0A0D0Z0C02030X0.1357Y-0.999Z-0.5123R
   * Check Z (thrust level) for the range of ESC
   */
   //extra character for null terminator
   int userInputLen = userInput.length() + 1;
   char inputArray[userInputLen];

   userInput.toCharArray(inputArray, userInputLen);

   //extract all status values from input array
   
   forward = charToBool(inputArray[forwardStat]);
   reverse = charToBool(inputArray[reverseStat]);
   lift = charToBool(inputArray[liftStat]);
   sink = charToBool(inputArray[sinkStat]);

   twistLeft = charToBool(inputArray[twistLeftStat]);
   twistRight = charToBool(inputArray[twistRightStat]);

   clawOpen = charToBool(inputArray[clawOpenStat]);
   clawClose = charToBool(inputArray[clawCloseStat]);

   yaw = readBetween(userInput, 'X','Y');
   pitch = readBetween(userInput, 'Y','T');
   thrustLevel = readBetween(userInput, 'T','R');
   normThrustLevel = normalizeThrust(thrustLevel);
 
   if (DEBUG){
     Serial.print("Message: ");
     for (int i = 0; i < userInputLen; i++){
        Serial.print(inputArray[i]);
     }
     Serial.println();

     Serial.println("thrustLevel: " + String(thrustLevel) + "  normalized: " + String(normThrustLevel));
     Serial.println("forward: " + String(forward));
     Serial.println("reverse: " + String(reverse));
     Serial.println("lift: " + String(lift));
     Serial.println("sink: " + String(sink));
     Serial.println("twistLeft: " + String(twistLeft));
     Serial.println("twistRight: " + String(twistRight));
     Serial.println("clawOpen: " + String(clawOpen));
     Serial.println("clawClose: " + String(clawClose));
     Serial.println("yaw: " + String(yaw));
     Serial.println("pitch: " + String(pitch));
   }   
}

//==== THRUSTER CONTROL ====
/*
 * THRUSTERS (1-6: 1-4 (SIDE), 5 (FRONT), 6 (REAR)):
 * W = FORWARD
 *    1,2,3,4: forward
 * S = REVERSE
 *    1,2,3,4: reverse
 * 
 * analog
 * X = YAW
 *  X < 0 : left
 *  X > 0 : right
 * 
 * Y = PITCH
 *  Y < 0 : up
 *  Y > 0 : down
 *  
 * Z = thruster level: normalize from [-1,1] to [0,1]
 *  applies to W and S
 * 
 * https://www.bluerobotics.com/store/electronics/besc30-r3/
 * OPTO AFRO ESC (flashed with bluerobotics software)
 * Pulse-width (PWM)
 * Max Reverse: 1100 μs
 * Stopped:       1500 μs
 * Max Forward: 1900 μs 
 * Deadband:   1475-1525 μs
 */

/*
 * Normalize the analog thrust value from [-1,1] to [0,1]
 */
float normalizeThrust(float inputThrust){
  //0 is no thrust, 1 is max thrust
  return (inputThrust + 1.0)/2.0;
}

void thrusterControl(bool forward, bool reverse, bool lift, bool sink, float yaw, float pitch, float normThrustLevel){
  //if W = 1, turn on thruster 1,2,3,4 in the forward direction
  int signal = 1500;
  
  if(forward || reverse){
    thruster5.writeMicroseconds(stopped);
    thruster6.writeMicroseconds(stopped);

    if (forward) {
      signal = normThrustLevel * range + stopped;
    } 
    if (reverse){
      signal = stopped - normThrustLevel * range;
    }   
    
    thruster1.writeMicroseconds(signal);
    thruster2.writeMicroseconds(signal);
    thruster3.writeMicroseconds(signal);
    thruster4.writeMicroseconds(signal);

  } else if (lift || sink) {
    thruster1.writeMicroseconds(stopped);
    thruster2.writeMicroseconds(stopped);
    thruster3.writeMicroseconds(stopped);
    thruster4.writeMicroseconds(stopped);    
    
    if(lift) {
      signal = normThrustLevel * range + stopped;
    } 
    if (sink) {
      signal = stopped - normThrustLevel * range;
    }
    thruster5.writeMicroseconds(signal);
    thruster6.writeMicroseconds(signal);
  }  else {
      if(abs(yaw) > abs(pitch)){
        rovYaw(yaw);
      }
      else{
        rovPitch(pitch);
    }
  }
}


void rovYaw(float yaw){
  int signal = 1500;
  
  thruster5.writeMicroseconds(stopped);
  thruster6.writeMicroseconds(stopped);

  signal = abs(yaw) * range;

  //yaw right: Thruster 1,2 (positive) Thruster 3,4 (negative)
  if (yaw > 0.0) {
    thruster1.writeMicroseconds(stopped + signal);
    thruster2.writeMicroseconds(stopped + signal);
    thruster3.writeMicroseconds(stopped - signal);
    thruster4.writeMicroseconds(stopped - signal);
  } else {
    thruster1.writeMicroseconds(stopped - signal);
    thruster2.writeMicroseconds(stopped - signal);
    thruster3.writeMicroseconds(stopped + signal);
    thruster4.writeMicroseconds(stopped + signal);
  }   
}

void rovPitch(float pitch) {
  int signal = 1500;

  thruster1.writeMicroseconds(stopped);
  thruster2.writeMicroseconds(stopped);
  thruster3.writeMicroseconds(stopped);
  thruster4.writeMicroseconds(stopped);

  signal = abs(pitch) * range;

  //pitch down: thruster5 (pos) thruster6 (neg)
  //if(pitch > 1.0){
  if(pitch > 1.0){
    thruster5.writeMicroseconds(stopped + signal);
    thruster6.writeMicroseconds(stopped - signal);
  } else {
    thruster5.writeMicroseconds(stopped - signal);
    thruster6.writeMicroseconds(stopped + signal);    
  }
}


//==== CLAW CONTROL ====
/*  DRV8825 Stepper Motor Driver Carrier, High Current
 *  https://www.pololu.com/product/2133
 *  
 *  Z = claw open
 *  C = claw close
 */
void clawControl(bool clawOpen, bool clawClose) {
    //reverse direction if needed
    if(clawOpen) {
      digitalWrite(clawDir, HIGH);
    } else {
      digitalWrite(clawDir, LOW);
    }
     for(int i = 0; i < clawCycle; i++){
        digitalWrite(clawStep, HIGH);
        delayMicroseconds(250);
        digitalWrite(clawStep, LOW);
        delayMicroseconds(250);
      }
  }


//==== TWISTER CONTROL ====
/* Enhanced 10Amp DC Motor Driver 
 *  https://www.robotshop.com/media/files/PDF/user-manual-md10c-v2.pdf
 *  A = twister left
 *  D = twister right
 *  
 *  yellow wire: PWM 30
 *  blue wire: PWM 29
 *  Control via SIGN-MAGNITUDE MODE
 *  " For sign-magnitude PWM operation, 2 control signals are used
 *  to control the speed and direction of the motor. PWM is feed to the PWM pin to control
 *  the speed while DIR pin is used to control the direction of the motor."
 */
void twisterControl(bool twistLeft, bool twistRight) {
  //digitalWrite(twisterPwm,HIGH);
  
  if (twistLeft) {
    digitalWrite(twisterDir,LOW);
  } else {
    //twist right
    digitalWrite(twisterDir,HIGH);
  }
    
    analogWrite(twisterPwm, twisterSpeed);
    delayMicroseconds(250);
}

//==== helper methods ====
bool charToBool(char inputChar){
  if (inputChar == '1'){
    return true;
  }
  else{
    return false;
  }
}

float readBetween(String userInput, char a, char b){
  int idx1 = userInput.indexOf(a) + 1;
  int idx2 = userInput.indexOf(b);

  if (DEBUG){
    Serial.println(idx1);
    Serial.println(idx2);
  }

  String numberStr = userInput.substring(idx1, idx2);
  return numberStr.toFloat();
}

