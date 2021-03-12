import requests
import json
from datetime import datetime
import pdb
from time import sleep

config = json.load(open('config.json'))
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=100,pool_maxsize=100)
session.mount('http://', adapter)

last_sensor_req_text = ''
last_light_req_text = ''

sleep_time = 0.1
while 1:
	try:
		step_start = datetime.now()
		req = session.get(config['hue_api_base_url']+"sensors")
		req_text = req.text
		req = json.loads(req_text)
		if req_text != last_sensor_req_text:
			for hue_id in req:
				with open(config['hue_sensor_states_path'] + hue_id + '.json', 'w') as f:
					json.dump(req[hue_id],f, indent=True)

		last_sensor_req_text = req_text

		req = session.get(config['hue_api_base_url']+"lights")
		req_text = req.text
		req = json.loads(req_text)
		if req_text != last_light_req_text:
			for hue_id in req:
				with open(config['hue_light_states_path'] + hue_id + '.json', 'w') as f:
					json.dump(req[hue_id],f, indent=True)

		last_light_req_text = req_text
		
		sleep_time = 0.1
	except requests.exceptions.ChunkedEncodingError:
		sleep_time *= 2
		print('Connection Reset by Peer! Doubling Sleep time to ' + str(sleep_time) + ' seconds!')
	
	sleep(sleep_time)

pdb.set_trace()