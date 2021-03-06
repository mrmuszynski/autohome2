import infrastructure, pdb, os
from kasa.exceptions import SmartDeviceException
try:
	os.mkdir('payloads')
except:
	pass
try:
	os.mkdir('payloads/buttons')
except:
	pass

########################################################################
#
#	init house
#
########################################################################
house = infrastructure.house()

########################################################################
#
#	init Hue lights
#
########################################################################
print("Initalizing Hue Lights")
fireplace_right = infrastructure.hue_light(house,2,'Fireplace Right')
fireplace_left = infrastructure.hue_light(house,3,'Fireplace Left')
tv_lamp = infrastructure.hue_light(house,4,'TV Lamp')
bathroom_lamp = infrastructure.hue_light(house,5,'Bathroom Lamp')
kitchen_cabinets_left = infrastructure.hue_light(house,6,'Kitchen Cabinets Left')
kitchen_cabinets_right = infrastructure.hue_light(house,7,'Kitchen Cabinets Right')
stove_1 = infrastructure.hue_light(house,8, 'Stove 1')
stove_2 = infrastructure.hue_light(house,9, 'Stove 2')
vanity_right = infrastructure.hue_light(house,10, 'Vanity Right')
vanity_left = infrastructure.hue_light(house,11, 'Vanity Left')
vanity_middle = infrastructure.hue_light(house,12, 'Vanity Middle')
laundry_light = infrastructure.hue_light(house,13, 'Laundry')
dining_room_ceiling_1 = infrastructure.hue_light(house,14, 'Dining Room Ceiling 1')
dining_room_ceiling_2 = infrastructure.hue_light(house,15, 'Dining Room Ceiling 2')
bedroom_ceiling_2 = infrastructure.hue_light(house,15, 'Dining Room Ceiling 2')
wall_lamp = infrastructure.hue_light(house,22, 'TV Room Wall')
kitchen_sink = infrastructure.hue_light(house,24, 'Kitchen Sink')
hallway = infrastructure.hue_light(house,23, 'Hallway')
tv_room_fan_1 = infrastructure.hue_light(house,18, 'Craftsman Fan 1')
tv_room_fan_2 = infrastructure.hue_light(house,19, 'Craftsman Fan 2')

########################################################################
#
#	init Kasa strips and plugs
#
########################################################################
print("Initalizing Kasa Stips")

# try:
# 	grow_house_strip = infrastructure.kasa_strip("192.168.0.188", "Grow House")
# 	grow_0 = infrastructure.kasa_strip_outlet(house, 'Grow Light 1', grow_house_strip, 0)
# 	grow_1 = infrastructure.kasa_strip_outlet(house, 'Grow Light 2', grow_house_strip, 1)
# except SmartDeviceException as e:
# 	# to do... move this exception into the grow house class
# 	# grow_house_strip is not defined if this error is excepted
# 	# it should still get defined so if it gets commanded elsewhere
# 	# it will fail gracefully
# 	print("Grow House Stip failed to initialize! Is it plugged in?")
# 	print(e)

living_room_strip = infrastructure.kasa_strip("192.168.0.106", "Living Room Power Strip")
living_room_strip0 = infrastructure.kasa_strip_outlet(house, 'Garland', living_room_strip, 0)
living_room_strip1 = infrastructure.kasa_strip_outlet(house, 'Living Room Strip 1', living_room_strip, 1)
garland = infrastructure.kasa_strip_outlet(house, 'Living Room Strip 2', living_room_strip, 2)



#single plug not implemented, but its IP is 192.168.0.192

########################################################################
#
#	init Decora dimmers
#
########################################################################
print("Initalizing Decora Dimmers")

decora_session = infrastructure.decora_session("mrmuszynski@gmail.com", "ZB248dCdNYzQ!cZ4")
garage_string = infrastructure.decora_dimmer(house, "Garage String Lights", decora_session, "192.168.0.198")

########################################################################
#
#	init mysensors
#
########################################################################
print("Initalizing MySensors")

mySensorsGateway = infrastructure.mySensorsGateway(house)
bookcaseLights = infrastructure.bookcaseLights(house, "Office Bookcase Lights", 2, 1)

########################################################################
#
#	init Venstar Thermostat
#
########################################################################
print("Initalizing Venstar Thermostat")

thermostat = infrastructure.venstar_thermostat(house, "Thermostat", "192.168.0.159")

#########################################################################
#
#	init groups
#
#########################################################################
print("Initalizing Groups")
fireplace = infrastructure.group([fireplace_left, fireplace_right], [[0,1]], "Fireplace", True)
stove = infrastructure.group([kitchen_cabinets_left, kitchen_cabinets_right, stove_1, stove_2], [[2,3],[0,1,2,3],[]], "Stove", False)

#########################################################################
#
#	init Hue switches and dimmers
#
#########################################################################
print("Initalizing Hue Switches and Dimmers")
fireplace_dimmer = infrastructure.hue_switch(house,32, fireplace)
stove_button = infrastructure.hue_switch(house,6, stove)
# bathroom_dimmer = infrastructure.hue_switch(house,35, None)
# dining_room_dimmer = infrastructure.hue_switch(house,38, None)
# kitchen_button = infrastructure.hue_switch(house,6, None)
# tv_lamp_button = infrastructure.hue_switch(house,23, None)


#########################################################################
#
#	Schedule Actions
#
#########################################################################
print("Initalizing Schedule")
# house.schedule_event("11:01:00",grow_0.turn_on)
# house.schedule_event("11:01:00",grow_1.turn_on)
# house.schedule_event("11:00:00",grow_0.turn_off)
# house.schedule_event("11:00:00",grow_1.turn_off)
# house.schedule_event("10:51:00",fireplace.turn_off)
# house.schedule_event("10:50:00",fireplace.turn_on)

#house.schedule_event("06:00:00",grow_0.turn_on)
#house.schedule_event("06:00:00",grow_1.turn_on)
#house.schedule_event("20:00:00",grow_0.turn_off)
#house.schedule_event("20:00:00",grow_1.turn_off)

#######################################################################################
#
#	EVENING TURN ON EVENTS
#
#######################################################################################

#TV Room
house.schedule_event("17:36:00",tv_lamp.turn_on,  {"bri": 177, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})
house.schedule_event("17:36:00",wall_lamp.turn_on,  {"bri": 177, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})
house.schedule_event("17:36:00",tv_room_fan_1.turn_on,  {"bri": 177, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})
house.schedule_event("17:36:00",tv_room_fan_2.turn_on,  {"bri": 177, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})
#glass lamp

#living room
house.schedule_event("17:36:00",fireplace_left.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})
house.schedule_event("17:36:00",fireplace_right.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})

#dining room
house.schedule_event("17:36:00",dining_room_ceiling_1.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})
house.schedule_event("17:36:00",dining_room_ceiling_2.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})

#kitchen
house.schedule_event("17:36:00",kitchen_cabinets_left.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})
house.schedule_event("17:36:00",kitchen_cabinets_right.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})
house.schedule_event("17:36:00",stove_1.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})
house.schedule_event("17:36:00",stove_2.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})
house.schedule_event("17:36:00",kitchen_sink.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})

#misc
house.schedule_event("17:36:00",hallway.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*60*10})
house.schedule_event("18:00:00",garland.turn_on, {})

#######################################################################################
#
#	EVENING BRIGHTENING EVENTS
#
#######################################################################################

#TV Room
house.schedule_event("18:00:00",tv_lamp.turn_on,  {"bri": 222, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})
house.schedule_event("18:00:00",wall_lamp.turn_on,  {"bri": 222, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})
house.schedule_event("18:00:00",tv_room_fan_1.turn_on,  {"bri": 222, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})
house.schedule_event("18:00:00",tv_room_fan_2.turn_on,  {"bri": 222, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})
#glass lamp

#living room
house.schedule_event("18:00:00",fireplace_left.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})
house.schedule_event("18:00:00",fireplace_right.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})

#dining room
house.schedule_event("18:00:00",dining_room_ceiling_1.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})
house.schedule_event("18:00:00",dining_room_ceiling_2.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})

#kitchen
house.schedule_event("18:00:00",kitchen_cabinets_left.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})
house.schedule_event("18:00:00",kitchen_cabinets_right.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})
house.schedule_event("18:00:00",stove_1.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})
house.schedule_event("18:00:00",stove_2.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})
house.schedule_event("18:00:00",kitchen_sink.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})

#misc
house.schedule_event("18:00:00",hallway.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})

#######################################################################################
#
#	EVENING DIMMING EVENTS
#
#######################################################################################

#TV Room
house.schedule_event("22:00:00",tv_lamp.turn_on,  {"bri": 100, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})
house.schedule_event("22:00:00",wall_lamp.turn_on,  {"bri": 100, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})
house.schedule_event("22:00:00",tv_room_fan_1.turn_on,  {"bri": 100, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})
house.schedule_event("22:00:00",tv_room_fan_2.turn_on,  {"bri": 100, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})
#glass lamp

#living room
house.schedule_event("22:00:00",fireplace_left.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})
house.schedule_event("22:00:00",fireplace_right.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})

#dining room
house.schedule_event("22:00:00",dining_room_ceiling_1.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})
house.schedule_event("22:00:00",dining_room_ceiling_2.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})

#kitchen
house.schedule_event("22:00:00",kitchen_cabinets_left.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})
house.schedule_event("22:00:00",kitchen_cabinets_right.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})
house.schedule_event("22:00:00",stove_1.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})
house.schedule_event("22:00:00",stove_2.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})
house.schedule_event("22:00:00",kitchen_sink.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})

#misc
house.schedule_event("22:00:00",hallway.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*60*10})

#######################################################################################
#
#	EVENING TURN OFF EVENTS
#
#######################################################################################

#turn off
house.schedule_event("01:00:00",house.goodnight, {})


#########################################################################
#
#	Debug stuff
#
#########################################################################


house.schedule_event("09:45:00",fireplace_left.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*10})
house.schedule_event("09:45:00",fireplace_right.turn_on, {"bri": 77, "hue": 8401, "sat": 140, "transitiontime": 30*10})

house.schedule_event("09:45:30",fireplace_left.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*10})
house.schedule_event("09:45:30",fireplace_right.turn_on, {"bri": 185, "hue": 8401, "sat": 140, "transitiontime": 120*10})

house.schedule_event("09:47:00",fireplace_left.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*10})
house.schedule_event("09:47:00",fireplace_right.turn_on, {"bri": 75, "hue": 8401, "sat": 140, "transitiontime": 180*10})

# house.schedule_event("15:27:04",tv_lamp.turn_off, {})
# house.schedule_event("15:27:06",tv_lamp.turn_on,  {"bri": 222, "hue": 8401, "sat": 140, "transitiontime": 120*60*10})
# house.schedule_event("15:27:08",tv_lamp.turn_off, {})

# new_payload = {"ON":True, "bri": 150, "ct": 200}
# fireplace_left.set_new_state(new_payload)
# fireplace_right.set_new_state(new_payload)
# fireplace.state = "ON"
# fireplace.cycle_mode()
# pdb.set_trace()
