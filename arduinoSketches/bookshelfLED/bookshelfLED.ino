
// Enable debug prints
#define MY_DEBUG

// Enable and select radio type attached
#define MY_RADIO_RF24
#define MY_NODE_ID 2
#define MY_PARENT_NODE_ID 0
#define MY_PARENT_NODE_IS_STATIC
//#define MY_RADIO_NRF5_ESB
//#define MY_RADIO_RFM69
//#define MY_RADIO_RFM95
//#define MY_PJON
#include <MySensors.h>

//-------------------------------------------------------//
// Initialize FastLED Stuff
//-------------------------------------------------------//

#include "FastLED.h"
#define LED_PIN_LEFT 6
#define LED_PIN_MIDDLE 7
#define LED_PIN_RIGHT 8
#define START_INDEX_FOR_MIDDLE_STRING 30
#define START_INDEX_FOR_RIGHT_STRING 86
#define NUM_LEDS 213

//#define PATTERN_LEN 4
#define BRIGHTNESS  80
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

int INTERRUPT = 0;
//-------------------------------------------------------//


void setup()
{
	//delay( 3000 );
  Serial.begin(115200);
	Serial.println( "Node ready to receive messages..." );
  // start FastLED, tell it about our LEDs
  FastLED.addLeds<LED_TYPE, LED_PIN_LEFT, COLOR_ORDER>(leds, 0, START_INDEX_FOR_MIDDLE_STRING).setCorrection( TypicalLEDStrip );
  FastLED.addLeds<LED_TYPE, LED_PIN_MIDDLE, COLOR_ORDER>(leds, START_INDEX_FOR_MIDDLE_STRING, START_INDEX_FOR_RIGHT_STRING).setCorrection( TypicalLEDStrip );
  FastLED.addLeds<LED_TYPE, LED_PIN_RIGHT, COLOR_ORDER>(leds, START_INDEX_FOR_RIGHT_STRING, NUM_LEDS).setCorrection( TypicalLEDStrip );
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
    delay(100);
  }
}

void test_program() {
  Serial.println("starting loop...");
  //simple_chase();
  set_by_hsv(33, 50, 255);
  wait(500);
  set_by_hsv(33, 100, 255);
  wait(500);
  set_by_hsv(33, 150, 255);
  wait(500);
  set_by_hsv(33, 200, 255);
  wait(500);
  set_by_hsv(33, 250, 255);
  wait(500);
}


void blackout() {
  INTERRUPT = 1;
  for (int ii = 0; ii < NUM_LEDS; ii++) {
    leds[ii] = CHSV( 0, 0, 0);
  }
  FastLED.show();
  if (INTERRUPT == 1 ) { INTERRUPT = 0; }
}

void rainbow_fade(int h, int s, int v) {
  INTERRUPT = 2;
  while (1 == 1) {
    for (int ii = 0; ii < 256; ii++) {
      set_by_hsv( (h + ii)%255 , s, v);
  
      if (INTERRUPT != 2) { return; }
      wait(2000);
      if (INTERRUPT != 2) { return; }
    }
  }
}

void wipe_on(int h, int s, int v) {
  INTERRUPT = 3;
  for (int ii = 0; ii < 6; ii++) {
    leds[5-ii] = CHSV( h, s, v);
    leds[6+ii] = CHSV( h, s, v);
    leds[17-ii] = CHSV( h, s, v);
    leds[18+ii] = CHSV( h, s, v);
    leds[29-ii] = CHSV( h, s, v);
    leds[30+ii] = CHSV( h, s, v);
    FastLED.show();
    
    wait(10);
    if (INTERRUPT != 3) { return; }
  }
  for (int ii = 36; ii < START_INDEX_FOR_RIGHT_STRING + 1; ii++) {
    leds[ii] = CHSV( h, s, v);
    FastLED.show();
    
    wait(10);
    if (INTERRUPT != 3) { return; }
  }
  for (int ii = 1; ii < 21; ii++) {
    leds[START_INDEX_FOR_RIGHT_STRING + ii] = CHSV( h, s, v);
    leds[START_INDEX_FOR_RIGHT_STRING + 21 - ii]  = CHSV( h, s, v);
    leds[START_INDEX_FOR_RIGHT_STRING + 21 + ii]  = CHSV( h, s, v);
    leds[START_INDEX_FOR_RIGHT_STRING + 63 - ii]  = CHSV( h, s, v);
    leds[START_INDEX_FOR_RIGHT_STRING + 63 + ii]  = CHSV( h, s, v);
    //leds[17-ii] = CHSV( h, s, v);
    //leds[18+ii] = CHSV( h, s, v);
    //leds[29-ii] = CHSV( h, s, v);
    //leds[30+ii] = CHSV( h, s, v);
    FastLED.show();
    
    wait(10);
    if (INTERRUPT != 3) { return; }
  }
}

void loop()
{
  
}

void receive(const MyMessage &message)
{
  Serial.println( "I GOT A MESSAGE!" );
  Serial.println( message.type );
  String payload = String(message.data);
  Serial.println( payload );
  String hString = payload.substring(0,3);
  String sString = payload.substring(3,6);
  String vString = payload.substring(6,9);  
  String programString = payload.substring(9,12);  

  int h = hString.toInt();
  int s = sString.toInt();
  int v = vString.toInt();
  int program = programString.toInt();


  if (program == 0) {
    INTERRUPT = -1;
    Serial.println("Setting HSV Value to: ");
    Serial.println( h );
    Serial.println( s );
    Serial.println( v );
    set_by_hsv(h, s, v);

  } else if (program == 1) {
    Serial.println("Beginning Program: Blackout");
    blackout();
    Serial.println("End Program: Rainbow Fade");
  } else if (program == 2) {
    Serial.println("Beginning Program: Rainbow Fade");
    rainbow_fade(h,s,v);
    Serial.println("End Program: Rainbow Fade");
  } else if (program == 3) {
    Serial.println("Beginning Program: Wipe On");
    wipe_on(h,s,v);
    Serial.println("End Program: Wipe On");
  } else {    Serial.println("Program not recognized: ");
    Serial.println( program );
  }
  
}
