# This file takes the path of crispydb and dumps it into config.json file
# the path is given as an argument
import sys
import json

path = sys.argv[1]

with open('config/config.json', 'r') as f:
    config = json.load(f)

config['path'] = path

with open('config/config.json', 'w') as f:
    json.dump(config, f, indent=4)
