if [ -z "$1" ]; then
    python3 main.py
else
    if [ "$1" = "cli" ]; then
        bash cli/cli.sh "$2"
    elif [ "$1" = "update" ]; then
        git stash
        git pull
        git stash pop
    elif [ "$1" = "install" ]; then
        pip3 install -r requirements.txt
    elif [ "$1" = "setpath" ]; then
        python3 src/setpath.py "$2"
    else
        echo "Invalid argument"
    fi
fi
