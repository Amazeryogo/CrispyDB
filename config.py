import json
import logging
import sys
import platform
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from colorama import Fore, Back, Style


with open('config/config.json', 'r') as f:
    config = json.load(f)
# request per minute
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