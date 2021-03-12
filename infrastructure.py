import pdb
import json
from requests import get, put, post, Session, adapters
from time import sleep

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



class hue_light():
	def __init__(self, parent, hue_id):
		self.hue_id = str(hue_id)
		parent.hue_lights[self.hue_id] = self
		self.parent = parent
		self.state_file_path = self.parent.config['hue_light_states_path'] + self.hue_id + '.json'
		self.state = None

	def update_state(self):
		while 1:
			try:
				self.state = json.load(open(self.state_file_path))
				break
			except json.JSONDecodeError:
				pass

class hue_dimmer():
	def __init__(self, parent, hue_id):
		self.hue_id = str(hue_id)
		parent.hue_sensors[self.hue_id] = self
		self.parent = parent
		self.state_file_path = self.parent.config['hue_sensor_states_path'] + self.hue_id + '.json'
		self.state = None
		self.last_buttonevent = None
		self.last_lastupdated = None
		self.this_buttonevent = None
		self.url = house.config['hue_api_base_url'] + 'sensors/' + self.hue_id + '/'
		self.button_off_payload = json.dumps({"config":{"on":False}})
		self.button_on_payload = json.dumps({"config":{"on":True}})


	def set_null_state_at_hub(self):
		put(self.url, data=self.button_off_payload)
		put(self.url, data=self.button_on_payload)
		req = self.parent.session.get(self.url)
		req = json.loads(req.text)
		with open(self.state_file_path, 'w') as f:
			json.dump(req,f, indent=True)


	def button_hold(self):
		self.set_null_state_at_hub()
		if self.this_buttonevent//1000 == 1:
			print('You are holding the on button')
		elif self.this_buttonevent//1000 == 2:
			print('You are holding the up button')
		elif self.this_buttonevent//1000 == 3:
			print('You are holding the down button')
		elif self.this_buttonevent//1000 == 4:
			print('You are holding the off button')
		else:
			print('Error! Unrecognized input!')


	def button_short_press(self):
		self.set_null_state_at_hub()
		if self.this_buttonevent//1000 == 1:
			print('You pushed the on button short')
		elif self.this_buttonevent//1000 == 2:
			print('You pushed the up button short')
		elif self.this_buttonevent//1000 == 3:
			print('You pushed the down button short')
		elif self.this_buttonevent//1000 == 4:
			print('You pushed the off button short')
		else:
			print('Error! Unrecognized input!')


	def button_release_after_hold(self):
		self.set_null_state_at_hub()
		if self.this_buttonevent//1000 == 1:
			print('You released the on button after holding it long')
		elif self.this_buttonevent//1000 == 2:
			print('You released the up button after holding it long')
		elif self.this_buttonevent//1000 == 3:
			print('You released the down button after holding it long')
		elif self.this_buttonevent//1000 == 4:
			print('You released the off button after holding it long')
		else:
			print('Error! Unrecognized input!')


	def update_state(self):
		while 1:
			try:
				self.state = json.load(open(self.state_file_path))
				break
			except json.JSONDecodeError:
				pass

		if self.last_buttonevent is None:
			self.last_buttonevent = self.state['state']['buttonevent']
			self.last_lastupdated = self.state['state']['lastupdated']
			return
		if self.state['state']['buttonevent'] is not None:
			self.this_buttonevent = self.state['state']['buttonevent']

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

			self.last_buttonevent = self.state['state']['buttonevent']
			self.last_lastupdated = self.state['state']['lastupdated']


house = house()
fireplace_right = hue_light(house,2)
fireplace_left = hue_light(house,3)
fireplace_dimmer = hue_dimmer(house,32)
house.update_state()

while 1:
	house.update_state()
pdb.set_trace()

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





