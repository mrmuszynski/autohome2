import infrastructure, pdb, os

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

########################################################################
#
#	init Kasa strips and plugs
#
########################################################################
# poang_strip = infrastructure.kasa_strip("192.168.0.106", "Poang Corner")
# computer = infrastructure.kasa_strip_outlet(poang_strip, 0)
# nothing = infrastructure.kasa_strip_outlet(poang_strip, 1)
# amp_and_garland = infrastructure.kasa_strip_outlet(poang_strip, 2)

grow_house_strip = infrastructure.kasa_strip("192.168.0.188", "Grow House")
grow_0 = infrastructure.kasa_strip_outlet(grow_house_strip, 0)
grow_1 = infrastructure.kasa_strip_outlet(grow_house_strip, 1)

#single plug not implemented, but its IP is 192.168.0.192


#########################################################################
#
#	init groups
#
#########################################################################
fireplace = infrastructure.group([fireplace_left, fireplace_right], [[0,1]], "Fireplace", True)
stove = infrastructure.group([kitchen_cabinets_left, kitchen_cabinets_right, stove_1, stove_2], [[2,3],[0,1,2,3],[]], "Stove", False)

#########################################################################
#
#	init Hue switches and dimmers
#
#########################################################################
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
# house.schedule_event("11:01:00",grow_0.turn_on)
# house.schedule_event("11:01:00",grow_1.turn_on)
# house.schedule_event("11:00:00",grow_0.turn_off)
# house.schedule_event("11:00:00",grow_1.turn_off)
# house.schedule_event("10:51:00",fireplace.turn_off)
# house.schedule_event("10:50:00",fireplace.turn_on)

house.schedule_event("06:00:00",grow_0.turn_on)
house.schedule_event("06:00:00",grow_1.turn_on)
house.schedule_event("20:00:00",grow_0.turn_off)
house.schedule_event("20:00:00",grow_1.turn_off)
house.schedule_event("18:00:00",tv_lamp.turn_on)
house.schedule_event("01:00:00",tv_lamp.turn_off)
