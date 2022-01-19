from core import *
from config import *
import pwinput
import json
from core import collection

from config import version

database = Database(config['path'])

global LOGGED
LOGGED = False

commandslist = []

try:
    print("CrispyDB CLI, version {}".format(version))
    print("\t By Suvid Datta")
    print("Use \"help\" to learn more\n")
    print("PLEASE LOG IN FIRST!\n")
    username = input("username:")
    password = pwinput.pwinput()
    if username == USERNAME:
        if password == PASSWORD:
            print("WELCOME BACK ", USERNAME, "!")
            while True:
                x = input(">>")
                for word in x.split(' '):
                    commandslist.append(word)
                command = commandslist[0]
                try:
                    if command == "CREATE".lower():
                        database.createCollection(commandslist[1])
                        print("DONE")
                    elif command == "GET".lower():
                        p = database.get_collections()
                        for i in p:
                            print(i)
                    elif command == "GETD".lower():
                        print(database.get_collection_data(commandslist[1]))
                    elif command == "LOAD".lower():
                        database.loadCollection(commandslist[1])
                        print("DONE")
                    elif command == "DELETE".lower():
                        database.deleteCollection(commandslist[1])
                        print("DONE")
                    elif command == "INSERT".lower():
                        for i in range(2, len(commandslist)):
                            database.add_to_collection(commandslist[1], commandslist[i])
                        print("DONE")
                    elif command == "REMOVE".lower():
                        for i in range(2, len(commandslist)):
                            database.remove_from_collection(commandslist[1], commandslist[i])
                        print("DONE")
                    elif command == "SAVE".lower():
                        database.save()
                    elif command == "BURN".lower():
                        database.removeall_from_collection(commandslist[1])
                    elif command == "KEYSEARCH".lower():
                        print(database.keysearch(commandslist[1], commandslist[2]))
                    elif command == "SEARCH".lower():
                        print(database.search(commandslist[1], commandslist[2]))
                    elif command == "HELP".lower():
                        print("""
                        CREATE [collection]
                        GET
                        GETD [collection]
                        LOAD [collection]
                        DELETE [collection]
                        INSERT [collection] [data]
                        REMOVE [collection] [data]
                        SAVE [collection]
                        BURN [collection]
                        HELP
                        KEYSEARCH [collection] [key]
                        SEARCH [collection] [data]
                        """)
                    elif command == "EXIT".lower():
                        Database.save(database)
                        print("bye")
                        quit()
                    else:
                        print(command, " not found")
                except:
                    print("oh no, we ran into a problem, try again!")
                    # print the issue
                    print(sys.exc_info())
                commandslist = []
        else:
            print("wrong password")
    else:
        print("wrong username")
except KeyboardInterrupt:
    database.save()
    print("bye")
    quit()
except EOFError:
    database.save()
    print("bye")
    quit()