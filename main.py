from src import *
from src.configman import *
import sys
import waitress


init_db()

try:
    print("CrispyDB is now running on {}:{}".format(config['host'], config['port']))
    waitress.serve(app, host=HOST, port=PORT)
except KeyboardInterrupt:
    sys.exit(1)
except EOFError:
    sys.exit(1)
