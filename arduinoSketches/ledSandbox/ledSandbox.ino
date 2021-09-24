/*
 * The MySensors Arduino library handles the wireless radio link and protocol
 * between your home built sensors/actuators and HA controller of choice.
 * The sensors forms a self healing radio network with optional repeaters. Each
 * repeater and gateway builds a routing tables in EEPROM which keeps track of the
 * network topology allowing messages to be routed to nodes.
 *
 * Created by Henrik Ekblad <henrik.ekblad@mysensors.org>
 * Copyright (C) 2013-2020 Sensnology AB
 * Full contributor list: https://github.com/mysensors/MySensors/graphs/contributors
 *
 * Documentation: http://www.mysensors.org
 * Support Forum: http://forum.mysensors.org
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * version 2 as published by the Free Software Foundation.
 *
 *******************************
 *
 * REVISION HISTORY
 * Version 1.0 - January 30, 2015 - Developed by GizMoCuz (Domoticz)
 *
 * DESCRIPTION
 * This sketch provides an example how to implement a Dimmable Light
 * It is pure virtual and it logs messages to the serial output
 * It can be used as a base sketch for actual hardware.
 * Stores the last light state and level in eeprom.
 *
 */

// Enable debug prints
// #define MY_DEBUG

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

#define CHILD_ID_LIGHT 1

#define EPROM_LIGHT_STATE 1
#define EPROM_DIMMER_LEVEL 2

#define LIGHT_OFF 0
#define LIGHT_ON 1

#define SN "Dimmable Light"
#define SV "1.0"

// MyMessage lightMsg(CHILD_ID_LIGHT, V_LIGHT);
// V_STATUS = 2
// V_PERCENTAGE = 3
// V_WATT = 17
// V_VAR1 = 24
// V_VAR2 = 25
// V_VAR3 = 26
// V_VAR4 = 27
// V_VAR5 = 28

//-------------------------------------------------------//
//DEFINE LED STUFF
//-------------------------------------------------------//

#include <Adafruit_NeoPixel.h>


#include "FastLED.h"

#define LED_PIN 6
#define NUM_LEDS 29
#define PATTERN_LEN 4
#define BRIGHTNESS  64
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];
CRGB pattern[PATTERN_LEN] = { CRGB::Blue, CRGB::Black, CRGB::Black, CRGB::White };
int last_index = -1;
int led_index = -1;
//-------------------------------------------------------//


void setup()
{
	//delay( 3000 );
	Serial.println( "Node ready to receive messages..." );
  // start FastLED, tell it about our LEDs
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness(  BRIGHTNESS );
}

void presentation()
{
	// Send the Sketch Version Information to the Gateway
	sendSketchInfo(SN, SV);

	present(CHILD_ID_LIGHT, S_DIMMER );
}

void loop()
{
  for (int ii = 0; ii < NUM_LEDS; ii++) {
    leds[ii] -= CRGB( 10, 10, 10);
  }
  
  led_index = random(0,100);
  while (led_index == last_index) {
    led_index = random(0,100);
  }

  last_index = led_index;
  if ( led_index <= 10) {
    leds[led_index] = CRGB(100, 100, 100);
  }
  FastLED.show();
  delay(100);
    
}


//void receive(const MyMessage &message)
//{
//  Serial.println( "I GOT A MESSAGE!" );
//  Serial.println( message.type );
//  String payload = String(message.data);
//  String redString = payload.substring(0,2);
//  String greenString = payload.substring(3,5);
//  String blueString = payload.substring(6,8);

//  int red = redString.toInt();
//  int green = greenString.toInt();
//  int blue = blueString.toInt();
  
//  Serial.println( payload );
  
//  // scale the potentiometer values from 10-bit (0-1023) to 8-bit (0-255)
//  Serial.println( "Setting color..." );
//  for (int ii = 0; ii < NUM_LEDS; ii++) {
//    leds[ii] = CRGB(red, green, blue);
//  }
  
//  FastLED.show(); // apply the function on led strip

  //delay(200);
  //Serial.println( "Setting color..." );
  //for (int ii = 0; ii < NUM_LEDS; ii++) {
  //  leds[ii] = CRGB(random(0,255), random(0,255), random(0,255));
  //}
  
  //FastLED.show(); // apply the function on led strip
//}
