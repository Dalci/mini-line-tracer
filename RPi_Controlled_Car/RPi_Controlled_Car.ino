/* 
 *  RPi Controlled Car
 *  
 *  Components:
 *     motors: RN, RP, LN, LP with moter driver L9110s
 *       each moter pin are mapped at 5, 6, 7, 10
 *     RX: (pno. 0)
 * *Caution* RX pin should be removed during uploading the sketch.
 *     TX: (pno. 1)
 *     
 *  The circuit:
 *  
 *  
 *  Created 2020-11-11
 *  By Sangjun Jeong(Dalci)
 *  Modified 2020-12-03
 *  By Sangjun Jeong(Dalci)
 */
#include <SoftwareSerial.h>
SoftwareSerial mySerial(7,8);   // RX(7), TX(8)

/* Constants */
// setting moter pin
const int motorRN = 5;
const int motorRP = 6;
const int motorLN = 9;
const int motorLP = 10;

// the speed of turning side wheel
const unsigned int unmove = 60;

// permitted time to no command 
const long no_command = 1000;

/* Function Declaration */
// base function to drive
void turnLeft(unsigned int spd);
void turnRight(unsigned int spd);
void rearLeft(unsigned int spd);
void rearRight(unsigned int spd);
void goForward(unsigned int spd);
void goBackward(unsigned int spd);
void Halt();

int Drive(char ctl, int spd);

// to parsing the command from RPi
byte digit2Num(byte digit);
int byteArray2Speed(const byte *btArr, int len);
void resetWord(byte *Word, int len);

/* Variables */
// Variables to receive
byte Word[5];   // before parsing the command
String Speed;   // before change to uint
char ctrl;      // 
int spd;

int ck;
unsigned int t_read = 0;
long last_order = 0;      // save the time of order at last
byte on_drive = 0;        // check whether on drive
byte input;               // check RPi input

void setup() {most lately
  // set up Serial
  Serial.begin(115200);
  pinMode(7, INPUT);additional
  pinMode(8, OUTPUT);
  mySerial.begin(115200);
  Serial.println("Ready.");

  // set up motors
  pinMode(motorRP, OUTPUT);
  pinMode(motorRN, OUTPUT);
  pinMode(motorLP, OUTPUT);
  pinMode(motorLN, OUTPUT);
  
  last_order = millis();

  // Motor Test
  Drive('B',250);
  delay(300);
  Drive('b',250);
  delay(300);
}

void loop() {
  while(!on_drive) {
    Halt();
    last_order = millis();
    if(mySerial.available()>0) {
      input = mySerial.peek();
    }
    
    if(input>0) { // if something is inputted
       on_drive = 1;
       Serial.println("Let's Go!");
       break;
    }
    else {   // if there is no input, waiting for signal
      Serial.println("Waiting for the signal...");
      delay(1000);
    }
  }
  
  // if time with no command is longer than time 'no_command',
  // stop the car and wait for the additional signal
  if(millis() - last_order > no_command) {
    resetWord(Word, 5);
    on_drive = 0;
    input = 0;
  }
  
  Word[4] = '\n';   // set escape sequence
  if(mySerial.available()>0) {
      t_read = mySerial.readBytesUntil(char(13), Word, 5);
      if(t_read) last_order = millis();      // update time
  }
  

  // parse the word
  ctrl = Word[0];
  spd = byteArray2Speed(Word, 5);

  ck = Drive(ctrl, spd);
  if(ck==-1) {  // Error occured
    Serial.print("Error (");
  }
  else if (spd == 0) {
    Halt();  // stop
    Serial.println("Stop");
  }
  else { // drive
    Serial.print("Run ");
    Serial.print(char(ctrl));
    Serial.println(spd);
    //mySerial.println(ctrl);
  }
  delay(200);
}

// to drive
void turnLeft(unsigned int spd) {
  analogWrite(motorRP, unmove);  analogWrite(motorRN, unmove);
  analogWrite(motorLP, spd);  analogWrite(motorLN, 0);
}
void turnRight(unsigned int spd) {
  analogWrite(motorRP, spd);  analogWrite(motorRN, 0);
  analogWrite(motorLP, unmove);  analogWrite(motorLN, unmove);
}
void rearLeft(unsigned int spd) {
  analogWrite(motorRP, unmove);  analogWrite(motorRN, unmove);
  analogWrite(motorLP, 0);  analogWrite(motorLN, spd);
}
void rearRight(unsigned int spd) {
  analogWrite(motorRP, 0);  analogWrite(motorRN, spd);
  analogWrite(motorLP, unmove);  analogWrite(motorLN, unmove);
}
void goForward(unsigned int spd) {
  analogWrite(motorRP, spd);  analogWrite(motorRN, 0);
  analogWrite(motorLP, spd);  analogWrite(motorLN, 0);
}
void goBackward(unsigned int spd) {
  analogWrite(motorRP, 0);  analogWrite(motorRN, spd);
  analogWrite(motorLP, 0);  analogWrite(motorLN, spd);
}
void Halt() {
  analogWrite(motorRP, 0);  analogWrite(motorRN, 0);
  analogWrite(motorLP, 0);  analogWrite(motorLN, 0);
}

int Drive(char ctl, int spd) {
  // spd error
  if(spd < 0 || spd > 255) return -1; 
  // drive
  switch(ctl) {
    case 'R':
      turnRight(spd);
      return 1;
    case 'r':
      rearRight(spd);
      return 1;  
    case 'L':
      turnLeft(spd);
      return 1;
    case 'l':
      rearLeft(spd);
      return 1;
    //  control Both wheels
    case 'B':
      goForward(spd);
      return 1;
    case 'b':
      goBackward(spd);
      return 1;
    default:
      Halt();
      return 0;
  }
}

// to parsing the command from RPi
byte digit2Num(byte digit) {
  if((digit<'0')||(digit>'9')) return -1;
  return digit - '0';
//  switch(digit) {
//    case '0': return 0;
//    case '1': return 1;
//    case '2': return 2;
//    case '3': return 3;
//    case '4': return 4;
//    case '5': return 5;
//    case '6': return 6;
//    case '7': return 7;
//    case '8': return 8;
//    case '9': return 9;
//  }
}
int byteArray2Speed(const byte *btArr, int len) {
  int idx;
  byte tmp, spd=0;
  
  if(len>5 || btArr[0] == 0) return 0;
  for(idx=1; idx<len; idx++) {
    if(btArr[idx]=='\n') break;
    tmp = digit2Num(btArr[idx]);
    spd = 10*spd + tmp;
  }
  return spd;
}
void resetWord(byte *Word, int len) {
  int i;
  for(i=0; i<len; i++) {
    Word[i] = 0;
  }
}
