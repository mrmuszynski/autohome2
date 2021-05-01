import pdb
import json
from requests import get, put, post, Session, adapters
from time import sleep
from datetime import datetime, timedelta
from glob import glob
from os import remove
import asyncio
import kasa

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
	def __init__(self, parent_strip, id_within_strip):
		self.parent_strip = parent_strip
		self.id_within_strip = id_within_strip

	def turn_on(self):
		asyncio.run(self.parent_strip.strip.children[self.id_within_strip].turn_on())
		return 1

	def turn_off(self):
		asyncio.run(self.parent_strip.strip.children[self.id_within_strip].turn_off())
		return 1

class hue_light():
	def __init__(self, parent, hue_id, name):
		self.name = name
		self.hue_id = str(hue_id)
		parent.hue_lights[self.hue_id] = self
		self.parent = parent
		self.hue_state_file_path = self.parent.config['hue_light_states_path'] + self.hue_id + '.json'
		self.hue_state = None

	def turn_on(self):
		print("Turning on " + self.name)
		url =  self.parent.config['hue_api_base_url'] + 'lights/' + str(self.hue_id) + '/state'
		payload = {"on": True}
		# if hue is not None: payload['hue'] = hue
		# if bri is not None: payload['bri'] = bri
		# if sat is not None: payload['sat'] = sat
		put(url, data = json.dumps(payload))
		return 1

	def turn_off(self):
		print("Turning off " + self.name)
		url =  self.parent.config['hue_api_base_url'] + 'lights/' + str(self.hue_id) + '/state'
		payload = {"bri_inc": False}
		# if hue is not None: payload['hue'] = hue
		# if bri is not None: payload['bri'] = bri
		# if sat is not None: payload['sat'] = sat
		put(url, data = json.dumps(payload))
		return 1

	def turn_up(self):
		print("Turning up " + self.name)
		url =  self.parent.config['hue_api_base_url'] + 'lights/' + str(self.hue_id) + '/state'
		payload = {
			"bri_inc": 25,
			"transitiontime": 10,
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
			"transitiontime": 10,
			}
		# if hue is not None: payload['hue'] = hue
		# if bri is not None: payload['bri'] = bri
		# if sat is not None: payload['sat'] = sat
		put(url, data = json.dumps(payload))
		return 1

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



class group:
	def __init__(self, hue_lights, subgroups, name):
		self.hue_lights = hue_lights
		self.subgroups = subgroups
		self.name = name
		self.state = "NONE"
		self.next_subgroup = 0
		self.actions = {
			'ON': {
				'on.short': self.do_nothing,
				'on.hold': self.do_nothing,
				'on.release': self.do_nothing,
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
		# self.state = 'ON'
		# print('State is ' + self.state)
		return 1

	def turn_off(self):
		print('Turning off lights assosciated with group ' + self.name + ': ')
		for hue_light in self.hue_lights: 
			print(hue_light.name)
			hue_light.turn_off()
		# print('State was ' + self.state)
		# self.state = 'OFF'
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





