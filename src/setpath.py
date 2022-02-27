import sys
import json

path = sys.argv[1]
f = open('src/config/config.json', 'r')
config = json.load(f)
config['path'] = path
f.close()
f = open('src/config/config.json', 'w')
json.dump(config, f, indent=4)
