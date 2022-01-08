pip3 install -r requirements.txt
#git stash
#git pull
#git stash 
echo 'do remember to get the latest version of the code whenever possible'
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
