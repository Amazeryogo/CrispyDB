from core import *
from config import *
import pwinput

database = Database(config['path'])

global LOGGED
LOGGED = False

kum = []
commands = ["CREATE", "GET", "GETD", "LOAD", "DELETE", "INSERT", "REMOVE", "SAVE", "BURN"]

try:
    print("CrispyDB CLI, v1.0-testing")
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
                    kum.append(word)
                command = kum[0]
                try:
                    if command == "CREATE".lower():
                        database.createCollection(kum[1])
                        print("DONE")
                    elif command == "GET".lower():
                        p = database.get_collections()
                        for i in p:
                            print(i)
                    elif command == "GETD".lower():
                        print(database.get_collection_data(kum[1]))
                    elif command == "LOAD".lower():
                        database.loadCollection(kum[1])
                        print("DONE")
                    elif command == "DELETE".lower():
                        database.deleteCollection(kum[1])
                        print("DONE")
                    elif command == "INSERT".lower():
                        for i in range(2, len(kum)):
                            database.add_to_collection(kum[1], kum[i])
                        print("DONE")
                    elif command == "REMOVE".lower():
                        for i in range(2, len(kum)):
                            database.remove_from_collection(kum[1], kum[i])
                        print("DONE")
                    elif command == "SAVE".lower():
                        database.saveCollection(kum[1])
                    elif command == "BURN".lower():
                        database.removeall_from_collection(kum[1])
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
                        """)
                    elif command == "EXIT".lower():
                        print("bye")
                        quit()
                    else:
                        print(command, " not found")
                except:
                    print("oh no, we ran into a problem, try again!")
                kum = []
        else:
            print("wrong password")
    else:
        print("wrong username")
except KeyboardInterrupt:
    print("bye")
    quit()
except EOFError:
    print("bye")
    quit()
