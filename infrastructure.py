import pdb
import json
from requests import get, put, post, Session, adapters
from time import sleep
from datetime import datetime
from glob import glob
from os import remove

def get_unix_time():
	return (datetime.now() - datetime.fromtimestamp(0)).total_seconds()

class house():
	def __init__(self):
		self.name = None
		self.config = json.load(open("config.json"))
		self.hue_light_states = None
		self.hue_sensor_states = None
		self.hue_lights = {}
		self.hue_sensors = {}
		self.session = Session()
		self.adapter = adapters.HTTPAdapter(
		    pool_connections=100,
		    pool_maxsize=100)
		self.session.mount('http://', self.adapter)


	def update_state(self):
		for x in self.hue_lights:
			self.hue_lights[x].update_state()
		for x in self.hue_sensors:
			self.hue_sensors[x].update_state()

	def read_sensors(self):
		button_payload_paths = glob(self.config['button_payload_path']+'*')
		for button_payload_path in button_payload_paths:
			payload_dict = json.load(open(button_payload_path))
			self.hue_sensors[payload_dict['button_id']].process_payload(payload_dict, button_payload_path)

	def read_payloads(self):
		self.read_sensors()

class hue_light():
	def __init__(self, parent, hue_id):
		self.hue_id = str(hue_id)
		parent.hue_lights[self.hue_id] = self
		self.parent = parent
		self.hue_state_file_path = self.parent.config['hue_light_states_path'] + self.hue_id + '.json'
		self.hue_state = None

	def update_state(self):
		while 1:
			try:
				self.hue_state = json.load(open(self.hue_state_file_path))
				break
			except ValueError:
				pass

class hue_switch():
	def __init__(self, parent, hue_id):
		self.hue_id = str(hue_id)
		parent.hue_sensors[self.hue_id] = self
		self.parent = parent
		self.hue_state_file_path = self.parent.config['hue_sensor_states_path'] + self.hue_id + '.json'
		self.hue_state = None
		self.state = 'NONE'
		self.last_buttonevent = None
		self.last_lastupdated = None
		self.this_buttonevent = None
		self.url = parent.config['hue_api_base_url'] + 'sensors/' + self.hue_id + '/'
		self.button_off_payload = json.dumps({"config":{"on":False}})
		self.button_on_payload = json.dumps({"config":{"on":True}})
		self.actions = {
			'ON': {
				'on.short': self.do_nothing,
				'on.hold': self.do_nothing,
				'on.release': self.do_nothing,
				'up.short': self.turn_up,
				'up.hold': self.do_nothing,
				'up.release': self.turn_up,
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
				'up.hold': self.do_nothing,
				'up.release': self.turn_up,
				'down.short': self.turn_down,
				'down.hold': self.do_nothing,
				'down.release': self.turn_down,
				'off.short': self.turn_off,
				'off.hold': self.turn_off,
				'off.release': self.turn_off
			},

		}



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

	def update_state(self):
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

	def do_nothing(self):
		print('Taking no action with lights assosciated with hue_id ' + self.hue_id)
		print('State was ' + self.state)
		print('State is ' + self.state)
		return 1

	def turn_on(self):
		print('Turning on lights assosciated with hue_id ' + self.hue_id)
		print('State was ' + self.state)
		self.state = 'ON'
		print('State is ' + self.state)
		return 1

	def turn_off(self):
		print('Turning off lights assosciated with hue_id ' + self.hue_id)
		print('State was ' + self.state)
		self.state = 'OFF'
		print('State is ' + self.state)
		return 1

	def turn_up(self):
		print('Turning up lights assosciated with hue_id ' + self.hue_id)
		print('State was ' + self.state)
		print('State is ' + self.state)
		return 1

	def turn_down(self):
		print('Turning down lights assosciated with hue_id ' + self.hue_id)
		print('State was ' + self.state)
		print('State is ' + self.state)
		return 1

	def process_payload(self, payload_dict, button_payload_path):
		print(self.state)
		print(payload_dict)
		if self.actions[self.state][payload_dict['button'] + '.' + payload_dict['action']]():
			remove(button_payload_path)
		else:
			print('Oh fuck, your payload action failed!')



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




