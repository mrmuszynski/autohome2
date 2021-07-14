import pdb
import json
from requests import get, put, post, Session, adapters
from time import sleep
from datetime import datetime, timedelta
from glob import glob
from os import remove
import asyncio
import kasa
import decora_wifi
from decora_wifi.models import residential_account

def get_unix_time():
	return (datetime.now() - datetime.fromtimestamp(0)).total_seconds()

class house:
	def __init__(self):
		self.name = "NONE"
		self.config = json.load(open("config.json"))
		self.hue_sensors = {}
		self.hue_lights = {}
		self.groups = {}
		self.session = Session()
		self.adapter = adapters.HTTPAdapter(
		    pool_connections=100,
		    pool_maxsize=100)
		self.session.mount('http://', self.adapter)
		self.schedule = []

	def read_button_events(self):
		for x in self.hue_sensors:
			self.hue_sensors[x].read_button_events()

	def read_sensors(self):
		button_payload_paths = glob(self.config['button_payload_path']+'*')
		for button_payload_path in button_payload_paths:
			while 1:
				try:
					payload_dict = json.load(open(button_payload_path))
					break
				except:
					pass
			self.hue_sensors[payload_dict['button_id']].process_payload(payload_dict, button_payload_path)

	def read_payloads(self):
		self.read_sensors()

	def schedule_event(self, time, action):
		YDOY = datetime.strftime(datetime.now(),"%Y-%jT")
		YDOY_time = YDOY + time
		YDOY_datetime = datetime.strptime(YDOY_time, "%Y-%jT%H:%M:%S")
		time_is_in_past = (YDOY_datetime - datetime.now()).total_seconds() < 0
		if time_is_in_past:
			YDOY_datetime += timedelta(days=1)
		self.schedule.append([YDOY_datetime, action])
		self.schedule = sorted(self.schedule, key=lambda x: x[0])

	def run_events(self):
		while 1:
			now = datetime.now()
			for scheduled_event in self.schedule:
				execute_event = (scheduled_event[0] - datetime.now()).total_seconds() < 0
				if execute_event:
					scheduled_event[1]()
					scheduled_event[0] += timedelta(days=1)
					self.schedule = sorted(self.schedule, key=lambda x: x[0])
					print('execute event')
				else:
					break

class kasa_strip:
	def __init__(self, ip, name):
		self.ip = ip
		self.name = name
		self.strip = kasa.SmartStrip(ip)
		asyncio.run(self.strip.update())

class kasa_strip_outlet:
	def __init__(self, parent, name, parent_strip, id_within_strip):
		self.parent_strip = parent_strip
		self.id_within_strip = id_within_strip

	def turn_on(self):
		asyncio.run(self.parent_strip.strip.children[self.id_within_strip].turn_on())
		return 1

	def turn_off(self):
		asyncio.run(self.parent_strip.strip.children[self.id_within_strip].turn_off())
		return 1

	def flash_high(self):
		self.turn_on()
		return 1

	def flash_low(self):
		self.turn_off()
		return 1

	def set_new_state(self, new_payload):
		if new_payload == ON: 
			self.turn_on()
		else:
			seld.turn_off()
		return 1

	def turn_up(self):
		return 1

	def turn_down(self):
		return 1

	def cycle_default(self):
		return 1

	def cycle_mode(self):
		return 1

	def get_state(self):
		if self.parent_strip.strip.children[self.id_within_strip].is_on:
			return "ON"
		else:
			return "OFF"


class decora_session:
	def __init__(self, decora_email, decora_pass):
		self.session = decora_wifi.DecoraWiFiSession()
		self.session.login(decora_email, decora_pass)
		switch_list = []

		perms = self.session.user.get_residential_permissions()
		for permission in perms:
			acct = residential_account.ResidentialAccount(self.session, permission.residentialAccountId)
			residences = acct.get_residences()

		for residence in residences:
			switch_list += residence.get_iot_switches()
		
		self.switches = dict((x.data['localIP'], x) for x in switch_list)

	# flash_high
	# flash_low
	# set_new_state
	# cycle_default
	# cycle_mode
	# turn_on
	# turn_off
	# turn_up
	# turn_down
	# get_state

class decora_dimmer:
	def __init__(self, parent, name, session, ip):
		self.switch = session.switches[ip]


	def turn_on(self, brightness=20):
		self.switch.update_attributes({'power': 'ON', 'brightness': brightness})
		return 1

	def turn_off(self):
		self.switch.update_attributes({'power': 'OFF'})
		return 1

	def flash_high(self, brightness=35):
		turn_on(self, brightness=brightness)
		return 1

	def flash_low(self, brightness=10):
		turn_on(self, brightness=brightness)
		return 1

	def set_new_state(self, new_payload):
		if new_payload['on']: 
			if 'brightness' in new_payload:
				self.turn_on(brightness = new_payload['brightness'])
			else:
				self.turn_on()
		else:
			seld.turn_off()
		return 1

	def turn_up(self):
		return 1

	def turn_down(self):
		return 1

	def cycle_default(self):
		return 1

	def cycle_mode(self):
		return 1

	def get_state(self):
		if self.parent_strip.strip.children[self.id_within_strip].is_on:
			return "ON"
		else:
			return "OFF"

class hue_light():
	def __init__(self, parent, hue_id, name):
		self.name = name
		self.hue_id = str(hue_id)
		parent.hue_lights[self.hue_id] = self
		self.saved_state = None
		self.parent = parent
		self.hue_state_file_path = self.parent.config['hue_light_states_path'] + self.hue_id + '.json'
		self.hue_state = None
		self.last_default = -1
		self.mode_lock = False
		self.defaults = {
			'bri': [
				(None, {'bri':100}),
				(None, {'bri':150}),
				(None, {'bri':200}),
				(None, {'bri':250})
			],
			'ct': [
				(None, {'ct':100}),
				(None, {'ct':150}),
				(None, {'ct':200}),
				(None, {'ct':250})
			],
			'sat': [
				(None, {'sat':100}),
				(None, {'sat':150}),
				(None, {'sat':200}),
				(None, {'sat':250})
			],
			'hue': [
				(None, {'hue':0}),
				(None, {'hue':10000}),
				(None, {'hue':20000}),
				(None, {'hue':30000}),
				(None, {'hue':40000}),
				(None, {'hue':50000})
			],
		}
		self.modes = ['bri', 'ct', 'hue', 'sat']
		self.last_mode = -1

	def flash_high(self):
		if self.mode_lock: return 1
		url =  self.parent.config['hue_api_base_url'] + 'lights/' + str(self.hue_id) + '/state'
		high = 254
		new_mode = self.modes[(self.last_mode + 1)%len(self.modes)]
		if new_mode == 'hue': high = 35000
		high_payload = {new_mode: high}
		put(url, data = json.dumps(high_payload))

		return 1

	def flash_low(self):
		if self.mode_lock: return 1
		url =  self.parent.config['hue_api_base_url'] + 'lights/' + str(self.hue_id) + '/state'
		new_mode = self.modes[(self.last_mode + 1)%len(self.modes)]
		low_payload = {new_mode: 1}
		put(url, data = json.dumps(low_payload))

		return 1

	def set_new_state(self, new_payload):
		url =  self.parent.config['hue_api_base_url'] + 'lights/' + str(self.hue_id) + '/state'
		put(url, data = json.dumps(new_payload))

		return 1


	def cycle_default(self):
		url =  self.parent.config['hue_api_base_url'] + 'lights/' + str(self.hue_id) + '/state'
		self.last_default = (self.last_default + 1)%len(self.defaults)
		payload = self.defaults[self.modes[self.last_mode]][self.last_default][1]
		print(payload)
		put(url, data = json.dumps(payload))
		return 1

	def cycle_mode(self):
		if self.mode_lock: return 1
		self.last_mode = (self.last_mode + 1)%len(self.modes)
		new_mode = self.modes[self.last_mode]
		mode_lock = True
		print("New_mode is " + new_mode)
		return 1

	def turn_on(self):
		print("Turning on " + self.name)
		url =  self.parent.config['hue_api_base_url'] + 'lights/' + str(self.hue_id) + '/state'
		self.last_default = 0
		self.last_mode = 0
		payload = self.defaults[self.modes[self.last_mode]][0][1] #this defaults to a hard coded value. Make it a TOD coded value
		payload["on"] = True
		# if hue is not None: payload['hue'] = hue
		# if bri is not None: payload['bri'] = bri
		# if sat is not None: payload['sat'] = sat
		put(url, data = json.dumps(payload))
		return 1

	def turn_off(self):
		print("Turning off " + self.name)
		url =  self.parent.config['hue_api_base_url'] + 'lights/' + str(self.hue_id) + '/state'
		payload = {"on": False}
		# if hue is not None: payload['hue'] = hue
		# if bri is not None: payload['bri'] = bri
		# if sat is not None: payload['sat'] = sat
		put(url, data = json.dumps(payload))
		return 1

	def turn_up(self):
		print("Turning up " + self.name)
		url =  self.parent.config['hue_api_base_url'] + 'lights/' + str(self.hue_id) + '/state'
		payload = {
			"bri_inc": 50,
			"transitiontime": 15,
			}
		# if hue is not None: payload['hue'] = hue
		# if bri is not None: payload['bri'] = bri
		# if sat is not None: payload['sat'] = sat
		put(url, data = json.dumps(payload))
		return 1

	def turn_down(self):
		print("Turning down " + self.name)
		url =  self.parent.config['hue_api_base_url'] + 'lights/' + str(self.hue_id) + '/state'
		payload = {
			"bri_inc": -25,
			"transitiontime": 15,
			}
		# if hue is not None: payload['hue'] = hue
		# if bri is not None: payload['bri'] = bri
		# if sat is not None: payload['sat'] = sat
		put(url, data = json.dumps(payload))
		return 1

	def get_state(self):
		state_file = open(self.parent.config['hue_light_states_path'] + self.hue_id + '.json')
		while 1:
			try:
				state = json.load(state_file)
				break
			except:
				pass
		
		return state

class hue_switch():
	def __init__(self, parent, hue_id, group):
		self.hue_id = str(hue_id)
		self.group = group
		parent.hue_sensors[self.hue_id] = self
		self.parent = parent
		self.hue_state_file_path = self.parent.config['hue_sensor_states_path'] + self.hue_id + '.json'
		self.hue_state = None
		self.last_buttonevent = None
		self.last_lastupdated = None
		self.this_buttonevent = None
		self.url = parent.config['hue_api_base_url'] + 'sensors/' + self.hue_id + '/'
		self.button_off_payload = json.dumps({"config":{"on":False}})
		self.button_on_payload = json.dumps({"config":{"on":True}})



	def set_null_state_at_hub(self):
		put(self.url, data=self.button_off_payload)
		put(self.url, data=self.button_on_payload)
		req = self.parent.session.get(self.url)
		req = json.loads(req.text)['state']
		with open(self.hue_state_file_path, 'w') as f:
			json.dump(req,f, indent=True)

	def write_button_command_payload(self, action, button):
		unix_time = get_unix_time()
		timestamp = format(unix_time*1e6, '.0f')
		json_data = {
			'button_id': self.hue_id,
			'action': action,
			'button': button,
			'unix_time': unix_time
		}
		json.dump(json_data, open(self.parent.config['button_payload_path'] + '/' + timestamp,'w'))
		

	def button_hold(self):
		self.set_null_state_at_hub()
		if self.this_buttonevent//1000 == 1:
			self.write_button_command_payload('hold', 'on')
		elif self.this_buttonevent//1000 == 2:
			self.write_button_command_payload('hold', 'up')
		elif self.this_buttonevent//1000 == 3:
			self.write_button_command_payload('hold', 'down')
		elif self.this_buttonevent//1000 == 4:
			self.write_button_command_payload('hold', 'off')
		else:
			print('Error! Unrecognized input!')


	def button_short_press(self):
		self.set_null_state_at_hub()
		if self.this_buttonevent//1000 == 1:
			self.write_button_command_payload('short', 'on')
		elif self.this_buttonevent//1000 == 2:
			self.write_button_command_payload('short', 'up')
		elif self.this_buttonevent//1000 == 3:
			self.write_button_command_payload('short', 'down')
		elif self.this_buttonevent//1000 == 4:
			self.write_button_command_payload('short', 'off')
		else:
			print('Error! Unrecognized input!')


	def button_release_after_hold(self):
		self.set_null_state_at_hub()
		if self.this_buttonevent//1000 == 1:
			self.write_button_command_payload('release', 'on')
		elif self.this_buttonevent//1000 == 2:
			self.write_button_command_payload('release', 'up')
		elif self.this_buttonevent//1000 == 3:
			self.write_button_command_payload('release', 'down')
		elif self.this_buttonevent//1000 == 4:
			self.write_button_command_payload('release', 'off')
		else:
			print('Error! Unrecognized input!')

	def read_button_events(self):
		while 1:
			try:
				self.hue_state = json.load(open(self.hue_state_file_path))
				break
			except ValueError:
				pass

		if self.last_buttonevent is None:
			self.last_buttonevent = self.hue_state['buttonevent']
			self.last_lastupdated = self.hue_state['lastupdated']
			return
		if self.hue_state['buttonevent'] is not None:
			self.this_buttonevent = self.hue_state['buttonevent']

			if self.this_buttonevent%1000 == 0:
				pass
			elif self.this_buttonevent%1000 == 1:
				self.button_hold()
			elif self.this_buttonevent%1000 == 2:
				self.button_short_press()
			elif self.this_buttonevent%1000 == 3:
				self.button_release_after_hold()
			else:
				print('Error! Unrecognized input!')

			self.last_buttonevent = self.hue_state['buttonevent']
			self.last_lastupdated = self.hue_state['lastupdated']


	def process_payload(self, payload_dict, button_payload_path):
		print(payload_dict)
		if self.group.actions[self.group.state][payload_dict['button'] + '.' + payload_dict['action']]():
			remove(button_payload_path)
		else:
			print('Oh fuck, your payload action failed!')

class venstar_thermostat:
	def __init__(self, name, session, ip):
		self.name = name
		self.session = session
		selp.ip = ip



class group:
	def __init__(self, hue_lights, subgroups, name, dimmer_control):
		self.dimmer_control = dimmer_control
		self.hue_lights = hue_lights
		self.subgroups = subgroups
		self.name = name
		self.state = "NONE"
		self.next_subgroup = 0
		self.actions = {
			'ON': {
				'on.short': self.cycle_default,
				'on.hold': self.cycle_mode,
				'on.release': self.unlock_mode,
				'up.short': self.turn_up,
				'up.hold': self.turn_up,
				'up.release': self.do_nothing,
				'down.short': self.turn_down,
				'down.hold': self.do_nothing,
				'down.release': self.turn_down,
				'off.short': self.turn_off,
				'off.hold': self.turn_off,
				'off.release': self.turn_off
			},
			'OFF': {
				'on.short': self.turn_on,
				'on.hold': self.turn_on,
				'on.release': self.turn_on,
				'up.short': self.do_nothing,
				'up.hold': self.do_nothing,
				'up.release': self.do_nothing,
				'down.short': self.do_nothing,
				'down.hold': self.do_nothing,
				'down.release': self.do_nothing,
				'off.short': self.do_nothing,
				'off.hold': self.do_nothing,
				'off.release': self.do_nothing
			},
			'NONE': {
				'on.short': self.turn_on,
				'on.hold': self.turn_on,
				'on.release': self.turn_on,
				'up.short': self.turn_up,
				'up.hold': self.turn_up,
				'up.release': self.turn_up,
				'down.short': self.turn_down,
				'down.hold': self.turn_down,
				'down.release': self.turn_down,
				'off.short': self.turn_off,
				'off.hold': self.turn_off,
				'off.release': self.turn_off
			},

		}
	def do_nothing(self):
		print('Taking no action with lights assosciated with group ' + self.name + ': ')
		for hue_light in self.hue_lights: print(hue_light.name)
		# print('State was ' + self.state)
		# print('State is ' + self.state)
		return 1

	def turn_on(self):
		print('Turning on lights assosciated with group ' + self.name + ': ')
		for light_id in range(len(self.hue_lights)):
			if light_id in self.subgroups[self.next_subgroup]:
				print(self.hue_lights[light_id].name)
				self.hue_lights[light_id].turn_on()
			else:
				print(self.hue_lights[light_id].name)
				self.hue_lights[light_id].turn_off()

		self.next_subgroup += 1
		self.next_subgroup = self.next_subgroup%len(self.subgroups)

		# print('State was ' + self.state)
		if self.dimmer_control: self.state = 'ON'
		# print('State is ' + self.state)
		return 1

	def cycle_mode(self):
		if sum([x.mode_lock for x in self.hue_lights]): return 1
		for hue_light in self.hue_lights: 
			hue_light.saved_state = hue_light.get_state()
			sleep(0.1)
		for hue_light in self.hue_lights: 
			hue_light.flash_high()
		sleep(1)

		for hue_light in self.hue_lights:
			hue_light.flash_low()
		sleep(1)
		
		for hue_light in self.hue_lights:
			state = hue_light.saved_state['state']
			if state['colormode'] == 'hs':
				new_payload = {
					'on': state['on'], 
					'bri': state['bri'], 
					'hue': state['hue'],
					'hue': state['sat']
					}

			else:
				new_payload = {
					'on': state['on'], 
					'bri': state['bri'], 
					state['colormode']: state[state['colormode']]
					}
				hue_light.set_new_state(new_payload)
		for hue_light in self.hue_lights: 
			hue_light.cycle_mode()
		
		return 1

	def unlock_mode(self):
		for hue_light in self.hue_lights: 
			hue_light.mode_lock = False
		return 1

	def cycle_default(self):
		for hue_light in self.hue_lights: 
			print(hue_light.name)
			hue_light.cycle_default()
		return 1

	def turn_off(self):
		print('Turning off lights assosciated with group ' + self.name + ': ')
		for hue_light in self.hue_lights: 
			print(hue_light.name)
			hue_light.turn_off()
		# print('State was ' + self.state)
		self.state = 'OFF'
		# print('State is ' + self.state)
		return 1

	def turn_up(self):
		print('Turning up lights assosciated with group ' + self.name + ': ')
		for hue_light in self.hue_lights: 
			print(hue_light.name)
			hue_light.turn_up()
		# print('State was ' + self.state)
		# print('State is ' + self.state)
		return 1

	def turn_down(self):
		print('Turning down lights assosciated with group ' + self.name + ': ')
		for hue_light in self.hue_lights: 
			print(hue_light.name)
			hue_light.turn_down()
		# print('State was ' + self.state)
		# print('State is ' + self.state)
		return 1


# Required methods for items
	# flash_high
	# flash_low
	# set_new_state
	# cycle_default
	# cycle_mode
	# turn_on
	# turn_off
	# turn_up
	# turn_down
	# get_state

#required args for item constructors
	# parent
	# name

#requred attributes for items
	# self.name = name
	# self.hue_id = str(hue_id)
	# parent.hue_lights[self.hue_id] = self
	# self.saved_state = None
	# self.parent = parent
	# self.hue_state_file_path = self.parent.config['hue_light_states_path'] + self.hue_id + '.json'
	# self.hue_state = None
	# self.last_default = -1
	# self.mode_lock = False
	# self.defaults = {}
	# self.modes = ['bri', 'ct', 'hue', 'sat']
	# self.last_mode = -1

#stuff to do
	#default state per tod
	#full control of state
	#revert to default

#available button states
	#short press X002
	#long press X001
	#release after long press x003

#unreliable button states
	#initial press x000





