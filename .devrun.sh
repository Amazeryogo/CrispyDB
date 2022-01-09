# basically run.sh but for development
pip3 install -r requirements.txt
if [ -z "$1" ]; then
    python3 main.py
else
    if [ "$1" = "cli" ]; then
        python3 cli.py
    else
        if [ "$1" = "nevergonna" ]; then
            python3 cryaboutit.py
        fi
        echo "Invalid argument"
    fi
fi