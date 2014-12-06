#include <Adafruit_NeoPixel.h>
#define PIN A0

/* Fun rainbow values
20145,32385,44625,56865,848640,3982080,7115520,10248960,13382400,16515840,13762605,10616925,7471245,4325565,1179885,7905,

9661440,12794880,15928320,14352420,11206740,8061060,4915380,1769700,5610,17850,30090,42330,54570,261120,3394560,6528000,

16121865,12976185,9830505,6684825,3539145,393465,10965,23205,35445,47685,59925,1632000,4765440,7898880,11032320,14165760,

*/
uint32_t rainbow[] = {16121865,12976185,9830505,6684825,3539145,393465,10965,23205,35445,47685,59925,1632000,4765440,7898880,11032320,14165760
};
const int ButtonPin = 2;
const int DBG_PIN = 13;
const long PhotoDelay = 3000;
const int N_PIXEL = 128;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(16, PIN, NEO_GRB + NEO_KHZ800);
bool dbg_val = false;

void setup() {
  Serial.begin(19200);
  pinMode(ButtonPin, INPUT);
  pinMode(DBG_PIN, OUTPUT);
  digitalWrite(ButtonPin, HIGH); //turn on pullups
  strip.begin();
  strip.show();
  
  for(int ii=0; ii < 3; ii++){
    digitalWrite(DBG_PIN, HIGH);
    delay(100);
    digitalWrite(DBG_PIN, LOW);
    delay(100);
  }
  digitalWrite(DBG_PIN, dbg_val);
}

void loop() {
  char command;
  int i, r, g, b;

  if(Serial.available()){
    while(Serial.available()){
      command = Serial.read();
      if(command == 'c'){ // color change command
	// wait for command to complete
	delay(10);
	if(Serial.available() >= 3){
	  r = Serial.read();
	  g = Serial.read();
	  b = Serial.read();
	  dbg_val = !dbg_val;
	  for(i = 0; i < N_PIXEL; i++){
	    strip.setPixelColor(i, r, g, b);
	  }
	  strip.show();
	  digitalWrite(DBG_PIN, dbg_val);
	}
      }
    }
  }
  if (digitalRead(ButtonPin) == LOW)
  {
    Serial.println("snap");// send to Pi
    StartCountdown(PhotoDelay/1000); //Start blinky Lights
    // The Pi will be processing the image for a while. Could add
    // red green ready light/strip
    delay (PhotoDelay); // allow pi to process the previous image
  }

}

void StartCountdown(int PhotoDelay)
{
  // synchronously wait and tick the lights off (they shouldn't be able 
  // to press the button now anyway (maybe check for cancel?)
  for (int x =0; x< 16; x++)
  {  
    strip.setPixelColor(x,rainbow[x]);
  }
  strip.show();

 for (int i = 0; i < PhotoDelay; i++)
  {
    delay(1000);
    strip.setPixelColor(i*3,0);
    strip.setPixelColor(i*3+1,0);
    strip.setPixelColor(i*3+2,0);
    strip.show();
  }
  strip.setPixelColor(15,0);
  strip.show();
}
