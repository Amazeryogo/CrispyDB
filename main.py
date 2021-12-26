from logging import debug
from src import *

print(Back.WHITE)

logging.basicConfig(filename="DB.log",level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
app.run(host=HOST, port=PORT, debug=config['DEBUG'])