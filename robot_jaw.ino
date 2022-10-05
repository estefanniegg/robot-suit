/*This code controls two servos, which opens and closes the robot jaw, depending on the input of a button.  When the the button is held down, the mouth opens.  When the button is released, the mouth closes.*/

#include <Servo.h>

Servo servo1;  // create servo object to control a servo
Servo servo2;  

int servoPos = 0;
const int buttonPin_1 = 2;
const int servoPin_1 = 9;
const int servoPin_2 = 10;

void setup()
{
  Serial.begin(9600);
    servo1.attach(servoPin_1);  // attaches the servo to pin
    servo2.attach(servoPin_2);

    pinMode(buttonPin_1, INPUT); 
}

int mouthButton = 0;
bool opening = true;
int pos = 0;

void loop()
{
    mouthButton = digitalRead(buttonPin_1);

    // mouth will open as button is held down and close as released
    if (mouthButton == HIGH) // open mouth
    {
        if (servoPos < 45)
        {
            servo1.write(servoPos); 
            servo2.write(45 - servoPos);    
            // waits for the servo to reach the position
            delay(2);                       
            servoPos++;
        }
    }
    else
    {
        if (servoPos > 0)
        {
            servo1.write(servoPos);    
            servo2.write(45 - servoPos);
            delay(2);
            servoPos--;
        }
    }
}
