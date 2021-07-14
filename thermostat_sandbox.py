import json
from requests import get, put, post, Session, adapters
import pdb
import urllib

url = 'http://192.168.0.159/'
req = get(url + 'query/info')

print(json.loads(get(url + 'query/info').text))

#0=off
#1=heat
#2=cool
#3=both

params = {'mode': 3,'fan': 0,'heattemp': 64,'cooltemp': 72}


post(url + 'control', data = urllib.parse.urlencode(params)).text
print(json.loads(get(url + 'query/info').text))


pdb.set_trace()