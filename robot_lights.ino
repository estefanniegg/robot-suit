/* I used the third Arduino for the RGB LEDs, instead of combining them with the servo Arduino, because the multiple analogWrites to change the color of the LEDs caused timing conflicts with the servos.*/

const int buttonPin = 12;     // the number of the pushbutton pin
const int r1 = 3;     // the number of the pushbutton pin
const int g1 = 9;     // the number of the pushbutton pin
const int b1 = 10;     // the number of the pushbutton pin

//const int ledPin =  13;      // the number of the LED pin

void setup()
{
  Serial.begin(9600);

    pinMode(buttonPin, INPUT);

    pinMode(r1, OUTPUT);
    pinMode(g1, OUTPUT);
    pinMode(b1, OUTPUT);
    pinMode(ledPin, OUTPUT);
}

int ledButton = 0;
int ledState = 0;
bool opening = true;

void loop()
{
  ledButton = digitalRead(buttonPin);
// light button pressed
  if (ledButton == HIGH) 
  {
        if (ledState == 0) 
        {
          analogWrite(r1, 500);
          analogWrite(g1, 10);
          analogWrite(b1, 30);
          ledState = 1;
        }
        else if (ledState == 1)
        {
          analogWrite(r1, 0);
          analogWrite(g1, 500);
          analogWrite(b1, 0);
          ledState = 2;
        }
        else if (ledState == 2)
        {
          analogWrite(r1, 0);
          analogWrite(g1, 0);
          analogWrite(b1, 30);
          ledState = 0;
        }
// wait for button to release/avoid bounce

        delay(100);
    }
}

