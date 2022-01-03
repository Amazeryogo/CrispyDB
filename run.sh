pip3 install -r requirements.txt
# if argv[1] is not empty and argv is cli run cli.py else run main.py
if [ -z "$1" ]; then
    python3 main.py
else
    if [ "$1" = "cli" ]; then
        python3 cli.py
    else
        echo "Invalid argument"
    fi
fi
