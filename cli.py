from core import *
from config import *
import pwinput
import json
from core import collection

from config import version

global current_col
current_col = ""

database = Database(config['path'])

global LOGGED
LOGGED = False

query = []

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
                    query.append(word)
                command = query[0]
                try:
                    if command == "CREATE" or "CREATE".lower():
                        database.createCollection(query[1])
                        print("DONE")
                    elif command == "GET" or "GET".lower():
                        p = database.get_collections()
                        for i in p:
                            print(i)
                    elif command == "GETD" or "GETD".lower():
                        print(database.get_collection_data(current_col))
                    elif command == "LOAD" or "LOAD".lower():
                        database.loadCollection(current_col)
                        print("DONE")
                    elif command == "DELETE" or "DELETE".lower():
                        database.deleteCollection(current_col)
                        current_col = ""
                        print("DONE")
                    elif command == "INSERT" or "INSERT".lower():
                        for i in range(1, len(query)):
                            database.add_to_collection(current_col, query[i])
                        print("DONE")
                    elif command == "REMOVE" or "REMOVE".lower():
                        for i in range(1, len(query)):
                            database.remove_from_collection(current_col, query[i])
                        print("DONE")
                    elif command == "SAVE" or "SAVE".lower():
                        database.save()
                    elif command == "BURN" or "BURN".lower():
                        database.removeall_from_collection(current_col)
                    elif command == "KEYSEARCH" or "KEYSEARCH".lower():
                        print(database.keysearch(current_col, query[1]))
                    elif command == "SEARCH" or "SEARCH".lower():
                        print(database.search(current_col, query[1], query[2]))
                    elif command == "HELP" or "HELP".lower():
                        print("""
                        CREATE <collection_name>
                        GET
                        GETD
                        DELETE 
                        LOAD
                        INSERT <item>
                        REMOVE <item>
                        SAVE
                        BURN
                        KEYSEARCH <key>
                        SEARCH <key> <value>
                        HELP
                        SETCOL <collection_name>
                        """)
                    elif command == "SETCOL" or "SETCOL".lower():
                        current_col = query[1]
                    elif command == "EXIT" or "EXIT".lower():
                        Database.save(database)
                        print("bye")
                        quit()
                    elif command == "DB" or "DB".lower():
                        print(current_col)
                    else:
                        print(command, " not found")
                except:
                    if current_col == "":
                        print("please set a collection using setcol")
                    else:
                        print("oh no, we ran into a problem, try again!")
                        # print the issue
                        print(sys.exc_info()[0])
                query = []
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
