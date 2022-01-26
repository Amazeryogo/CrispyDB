if [ -z "$1" ]; then
    python3 main.py
else
    if [ "$1" = "cli" ]; then
        python3 cli.py
    elif [ "$1" = "update" ]; then
        python3 update.py
    elif [ "$1" = "install" ]; then
        pip3 install -r requirements.txt
    else
        echo "Invalid argument"
    fi
fi
