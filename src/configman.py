import json

with open('src/config/config.json', 'r') as f:
    config = json.load(f)


rpm = str(config['RequestsPerMinute']) + ' per minute'
ccpm = str(config['CollectionCreationPerMinute']) + ' per minute'
cdpm = str(config['CollectionDeletionPerMinute']) + ' per minute'
version = config['version']
PORT = config['port']
HOST = config['host']
webUI = config['webUI']
name = config['name']
users = config['users']

with open('src/config/tokens.json', 'r') as p:
    tokens = json.load(p)
