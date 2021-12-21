import json
import sys
import platform
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

with open('config/config.json', 'r') as f:
    config = json.load(f)





# request per minute
rpm = str(config['rpm']) + ' per minute'
#collection creation per minute
ccpm = str(config['ccpm']) + ' per minute'
# collection deletion per minute
cdpm = str(config['cdpm']) + ' per minute'
version = config['version']
python_version = config['python version']
PORT = config['port']
HOST = config['host']
USERNAME = config['admin name']
PASSWORD = config['admin password']
webUI = config['webUI']