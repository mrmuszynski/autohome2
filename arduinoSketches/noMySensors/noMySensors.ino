
#include "FastLED.h"

#define LED_PIN 6
#define NUM_LEDS 22

//#define PATTERN_LEN 4
#define BRIGHTNESS  70
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

//-------------------------------------------------------//


void setup()
{
	//delay( 3000 );
  Serial.begin(115200);
	Serial.println( "Node ready to receive messages..." );
  // start FastLED, tell it about our LEDs
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness( BRIGHTNESS );
  blackout();

  delay(1000);
  set_by_hsv(255,0,255);
  FastLED.show();
}

void change_brightness_by_value( float value ) {
  for (int ii = 0; ii < NUM_LEDS; ii++) {
    float total = leds[ii].r + leds[ii].g + leds[ii].b;
    float reduction_r = value*leds[ii].r/total;
    float reduction_g = value*leds[ii].g/total;
    float reduction_b = value*leds[ii].b/total;
    leds[ii] = CRGB( 
      leds[ii].r + reduction_r, 
      leds[ii].g + reduction_g, 
      leds[ii].b + reduction_b 
      );
  }  
  FastLED.show();
}

void rainbow( int start_color) 
{
  for (int ii = 0; ii < NUM_LEDS; ii++) {
    leds[ii] = CHSV( start_color + ii*10, 255, 100);
  }
  FastLED.show();
}

void change_brightness_by_percent( float percent ) {
  for (int ii = 0; ii < NUM_LEDS; ii++) {
    leds[ii] = CRGB( 
      leds[ii].r*percent, 
      leds[ii].g*percent, 
      leds[ii].b*percent);
  }  
//  FastLED.show();
}

void blackout() {
  for (int ii = 0; ii < NUM_LEDS; ii++) {
    leds[ii] = CHSV( 0, 0, 0);
  }
  FastLED.show();  
}

void set_by_hsv(int h, int s, int v) {
  for (int ii = 0; ii < NUM_LEDS; ii++) {
    leds[ii] = CHSV( h, s, v);
  }
  FastLED.show();  
}

void simple_chase() {
  for (int ii = 0; ii < NUM_LEDS; ii++) {
    change_brightness_by_percent( 0.9 );
    leds[ii] = CRGB(200,200,200);
    FastLED.show();
    delay(25);
  }
}
void loop()
{
  Serial.println("starting loop...");
  set_by_hsv(33, 50, 255);
  delay(3000);
  set_by_hsv(33, 100, 255);
  delay(3000);
  set_by_hsv(33, 150, 255);
  delay(3000);
  set_by_hsv(33, 200, 255);
  delay(3000);
  set_by_hsv(33, 250, 255);
  delay(3000);
  //simple_chase();
  
}
