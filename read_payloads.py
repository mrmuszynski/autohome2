from object_definitions import house
from os import remove
from glob import glob

for f in glob('payloads/buttons/*'): remove(f)
for f in glob('payloads/lights/*'): remove(f)

while 1: house.read_payloads()
