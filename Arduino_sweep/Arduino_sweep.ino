/* Sweep
  by BARRAGAN <http://barraganstudio.com>
  This example code is in the public domain.

  modified 8 Nov 2013
  by Scott Fitzgerald
  http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
const int stopBtn = 8; // STOP BTN pin is P6

void setup() {
  //Serial.begin(115200);  // open serial connection to USB Serial
  Serial1.begin(57600);  // open internal serial connection to MT7688
  myservo.attach(5);  // attaches the servo on pin 5 to the servo object
  pinMode(stopBtn, INPUT);
}

void loop() {

  int c = Serial1.read();      // read from MT7688
  if (c != -1) {
    switch (c) {
      case '0':
        for (int i = 0 ; i < 23 ; i++) {
          if (digitalRead(stopBtn)) {
            myservo.write(69);
            delay(100);
          } else {
            break;
          }
        }
        break;
      case '1':
        for (int i = 0 ; i < 20 ; i++) {
          if (digitalRead(stopBtn)) {
            myservo.write(101);
            delay(100);
          } else {
            break;
          }
        }
        break;
    }
  } else {
    myservo.write(88);
  }

}
