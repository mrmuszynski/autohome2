/**
 * The MySensors Arduino library handles the wireless radio link and protocol
 * between your home built sensors/actuators and HA controller of choice.
 * The sensors forms a self healing radio network with optional repeaters. Each
 * repeater and gateway builds a routing tables in EEPROM which keeps track of the
 * network topology allowing messages to be routed to nodes.
 *
 * Created by Henrik Ekblad <henrik.ekblad@mysensors.org>
 * Copyright (C) 2013-2015 Sensnology AB
 * Full contributor list: https://github.com/mysensors/Arduino/graphs/contributors
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
 * DESCRIPTION
 *
 * Simple binary switch example 
 * Connect button or door/window reed switch between 
 * digitial I/O pin 3 (BUTTON_PIN below) and GND.
 * http://www.mysensors.org/build/binary
 */


// Enable debug prints to serial monitor
// #define MY_DEBUG 

// Enable and select radio type attached
#define MY_RADIO_RF24
#define MY_NODE_ID 1
#define MY_PARENT_NODE_ID 0
#define MY_PARENT_NODE_IS_STATIC
//#define MY_RADIO_RFM69

#include <MySensors.h>
#include <Bounce2.h>

#define CHILD_ID_1 3
#define CHILD_ID_2 4
#define CHILD_ID_3 5
#define CHILD_ID_4 6
#define BUTTON_PIN_1  3  // Arduino Digital I/O pin for button/reed switch
#define BUTTON_PIN_2  4  // Arduino Digital I/O pin for button/reed switch
#define BUTTON_PIN_3  5  // Arduino Digital I/O pin for button/reed switch
#define BUTTON_PIN_4  6  // Arduino Digital I/O pin for button/reed switch

Bounce debouncer_1 = Bounce(); 
Bounce debouncer_2 = Bounce(); 
Bounce debouncer_3 = Bounce(); 
Bounce debouncer_4 = Bounce(); 
int oldValue_1=-1;
int oldValue_2=-1;
int oldValue_3=-1;
int oldValue_4=-1;

// Change to V_LIGHT if you use S_LIGHT in presentation below
MyMessage msg_1(CHILD_ID_1,V_TRIPPED);
MyMessage msg_2(CHILD_ID_2,V_TRIPPED);
MyMessage msg_3(CHILD_ID_3,V_TRIPPED);
MyMessage msg_4(CHILD_ID_4,V_TRIPPED);

void setup()  
{  
  // Setup the button
  pinMode(BUTTON_PIN_1,INPUT);
  pinMode(BUTTON_PIN_2,INPUT);
  pinMode(BUTTON_PIN_3,INPUT);
  pinMode(BUTTON_PIN_4,INPUT);
  // Activate internal pull-up
  digitalWrite(BUTTON_PIN_1,HIGH);
  digitalWrite(BUTTON_PIN_2,HIGH);
  digitalWrite(BUTTON_PIN_3,HIGH);
  digitalWrite(BUTTON_PIN_4,HIGH);
  
  // After setting up the button, setup debouncers
  debouncer_1.attach(BUTTON_PIN_1);
  debouncer_2.attach(BUTTON_PIN_2);
  debouncer_3.attach(BUTTON_PIN_3);
  debouncer_4.attach(BUTTON_PIN_4);
  debouncer_1.interval(5);
  debouncer_2.interval(5);
  debouncer_3.interval(5);
  debouncer_4.interval(5);
  
}

void presentation() {
  // Register binary input sensor to gw (they will be created as child devices)
  // You can use S_DOOR, S_MOTION or S_LIGHT here depending on your usage. 
  // If S_LIGHT is used, remember to update variable type you send in. See "msg" above.
  present(CHILD_ID_1, S_DOOR);  
  present(CHILD_ID_2, S_DOOR);  
  present(CHILD_ID_3, S_DOOR);  
  present(CHILD_ID_4, S_DOOR);  
}


//  Check if digital input has changed and send in new value
void loop() 
{
  debouncer_1.update();
  debouncer_2.update();
  debouncer_3.update();
  debouncer_4.update();
  // Get the update value
  int value_1 = debouncer_1.read();
  int value_2 = debouncer_2.read();
  int value_3 = debouncer_3.read();
  int value_4 = debouncer_4.read();
  if (value_1 != oldValue_1) {
     // Send in the new value
     send(msg_1.set(value_1==HIGH ? 1 : 0));
     Serial.println("Button 1:");
     Serial.println(value_1);
     oldValue_1 = value_1;
  }  
  if (value_2 != oldValue_2) {
     // Send in the new value
     send(msg_2.set(value_2==HIGH ? 1 : 0));
     Serial.println("Button 2:");
     Serial.println(value_2);
     oldValue_2 = value_2;
  }  
   if (value_3 != oldValue_3) {
     // Send in the new value
     send(msg_3.set(value_3==HIGH ? 1 : 0));
     Serial.println("Button 3:");
     Serial.println(value_3);
     oldValue_3 = value_3;
  }  
   if (value_4 != oldValue_4) {
     // Send in the new value
     send(msg_4.set(value_4==HIGH ? 1 : 0));
     Serial.println("Button 4:");
     Serial.println(value_4);
     oldValue_4 = value_4;
  }  
} 
