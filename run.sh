pip3 install -r requirements.txt


if [ -z "$1" ]; then
    python3 main.py
else
    if [ "$1" = "cli" ]; then
        python3 cli.py
    else
        if [ "$1" = "update" ]; then
            python3 update.py
        fi
        echo "Invalid argument"
    fi
fi
