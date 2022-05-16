from src import *
from src.configman import *
import sys
import waitress

try:
    print("CrispyDB is now running on {}:{}".format(config['host'], config['port']))
    waitress.serve(app, host=HOST, port=PORT)
except KeyboardInterrupt:
    Database.save()
    sys.exit(1)
except EOFError:
    Database.save()
    sys.exit(1)
