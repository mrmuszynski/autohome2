import time
from glob import glob
from os import remove
while 1:
	files = glob('heartbeat/*')
	for f in files: remove(f)
	f = open('heartbeat/'+str(time.time()),'w')
	f.close()
	time.sleep(1)
