from src import *

if __name__ == '__main__':
    if logginghuh == True:
        logging.basicConfig(filename='DB.log',level=logging.DEBUG)
        print("LOGGING IS ON")
    else:
        pass
    app.run(host=HOST, port=PORT)

