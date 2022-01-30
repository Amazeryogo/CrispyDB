import json

with open('config/config.json', 'r') as f:
    config = json.load(f)


rpm = str(config['RequestsPerMinute']) + ' per minute'
ccpm = str(config['CollectionCreationPerMinute']) + ' per minute'
cdpm = str(config['CollectionDeletionPerMinute']) + ' per minute'
version = config['version']
PORT = config['port']
HOST = config['host']
USERNAME = config['admin name']
PASSWORD = config['admin password']
webUI = config['webUI']
name = config['name']
