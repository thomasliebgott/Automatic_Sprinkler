#include <FastLED.h>
#include <stdlib.h> 

#define NUM_LEDS 29
#define DATA_PIN 2
//#define CLOCK_PIN 13

// Define the array of leds
CRGB leds[NUM_LEDS];

int bp1 = 0;
void setup() {
     FastLED.addLeds<WS2811, DATA_PIN, GRB>(leds, NUM_LEDS);
     FastLED.setBrightness(200);
     pinMode(bp1, INPUT);
     Serial.begin(9600);
}
void loop(){
    int b1 = digitalRead(bp1);
    if (b1 == HIGH) {
    // code couleur BRG 
    delay(100);
    int i = 0;
        while(i < 10){
          i = i+1;
          int b1 = digitalRead(bp1);
            if(b1 == LOW){
              break;
            }
          fill_solid(leds, NUM_LEDS,CRGB(50,255,50 ));
          FastLED.show(); 
          delay(100);
        }
    }
    else {
        fill_solid(leds, NUM_LEDS,CRGB::Black);
        FastLED.show(); 
        delay(100);  
  delay(100);
}
}
