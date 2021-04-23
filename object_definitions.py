import infrastructure

house = infrastructure.house()
fireplace_right = infrastructure.hue_light(house,2)
fireplace_left = infrastructure.hue_light(house,3)
fireplace_left = infrastructure.hue_light(house,3)
tv_lamp = infrastructure.hue_light(house,4)
bathroom_lamp = infrastructure.hue_light(house,5)
kitchen_cabinets_left = infrastructure.hue_light(house,6)
kitchen_cabinets_right = infrastructure.hue_light(house,7)
stove_1 = infrastructure.hue_light(house,8)
stove_2 = infrastructure.hue_light(house,9)
vanity_right = infrastructure.hue_light(house,10)
vanity_left = infrastructure.hue_light(house,11)
vanity_middle = infrastructure.hue_light(house,12)
laundry_light = infrastructure.hue_light(house,13)
dining_room_ceiling_1 = infrastructure.hue_light(house,14)
dining_room_ceiling_2 = infrastructure.hue_light(house,15)

kitchen_button = infrastructure.hue_switch(house,6)
tv_lamp_button = infrastructure.hue_switch(house,23)
fireplace_dimmer = infrastructure.hue_switch(house,32)
bathroom_dimmer = infrastructure.hue_switch(house,35)
dining_room_dimmer = infrastructure.hue_switch(house,38)
house.update_state()