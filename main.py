from src import *
import waitress
try:
    print("\n\nStarting CrispyDB...")
    print("\n\nCrispyDB is now running on {}:{}".format(config['host'], config['port']))
    waitress.serve(app, host=config['host'], port=config['port'])
except KeyboardInterrupt:
    print(Fore.RED + "KeyboardInterrupt")
    Database.save()
    sys.exit(1)
except EOFError:
    print(Fore.RED + "EOFError")
    Database.save()
    sys.exit(1)


