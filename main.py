from logging import debug

from flask.templating import Environment
from src import *
import webbrowser

print(Back.WHITE)

if config['open_browser']:
    url = "http://"+config['host']+":"+str(config['port'])
    webbrowser.open(url=url)

logging.basicConfig(filename="DB.log",level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
app.run(host=HOST, port=PORT, debug=config['DEBUG'])