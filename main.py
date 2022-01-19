from logging import debug
from src import *
import webbrowser

try:
    if config['environment'] != 'production' and config['environment'] != 'development':
        print(Fore.BLUE + '[ERROR] Environment not set correctly')
        sys.exit(1)

    if python_version != platform.python_version():
        print(Fore.BLUE + "Python version mismatch")
        sys.exit(1)

    if webUI == True:
        print(Fore.BLUE + "Web UI is on")
    else:
        print(Fore.BLUE + "WebUI is off ")

    if config['hide_config'] != True and config['environment'] == 'production':
        print(Fore.BLUE + "Config is not hidden in production mode")
    else:
        print(Fore.BLUE + "CONFIG IS HIDDEN")

    if config['open_browser']:
        url = "http://" + config['host'] + ":" + str(config['port']) + "/" + 'web'
        webbrowser.open(url=url)

    logging.basicConfig(filename="DB.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    app.run(host=HOST, port=PORT, debug=config['DEBUG'])

except KeyboardInterrupt:
    print(Fore.RED + "KeyboardInterrupt")
    Database.save()
    sys.exit(1)
except EOFError:
    print(Fore.RED + "EOFError")
    Database.save()
    sys.exit(1)


