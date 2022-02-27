url="0.0.0.0:5000"
echo "Crispy CLI v2.0"
token=$1
while true; do
    read -p "$token@crispydb $ " command
    if [ "$command" = "exit" ]; then
        curl -X POST "$url/flush/token?token=$token"
        echo "Bye!"
        break
    elif [ "$command" = "create" ]; then
        read -p "Collection name: " collection
        curl -X POST "$url/create/$collection?token=$token"
    elif [ "$command" = "load" ]; then
        read -p "Collection name: " collection
        curl -X POST "$url/load/$collection?token=$token"
    elif [ "$command" = "save" ]; then
        read -p "Collection name: " collection
        curl -X POST "$url/save/$collection?token=$token"
    elif [ "$command" = "delete" ]; then
        read -p "Collection name: " collection
        curl -X POST "$url/delete/$collection?token=$token"
    elif [ "$command" = "removefrom" ]; then
        read -p "Collection name: " collection
        curl -X POST "$url/removefrom/$collection?token=$token"
    elif [ "$command" = "addto" ]; then
        read -p "Collection name: " collection
        curl -X POST "$url/add/$collection?token=$token"
    elif [ "$command" = "getdata" ]; then
        read -p "Collection name: " collection
        curl -X POST "$url/getdata/$collection?token=$token"
    elif [ "$command" = "getallroutes" ]; then
        curl -X POST "$url/getallroutes?token=$token"
    elif [ "$command" = "help" ]; then
        echo "create - Create a new collection"
        echo "load - Load a collection"
        echo "save - Save a collection"
        echo "delete - Delete a collection"
        echo "removefrom - Remove a document from a collection"
        echo "addto - Add a document to a collection"
        echo "getdata - Get data from a collection"
        echo "getallroutes - Get all routes"
        echo "exit - Exit CrispyDB"
    else
        echo "Command not found!"
    fi
done