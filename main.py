from object_definitions import house

try:
	house.mySensorsGateway.start()
	house.run()
except KeyboardInterrupt:
	house.mySensorsGateway.stop()