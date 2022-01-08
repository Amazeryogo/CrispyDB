pip3 install -r requirements.txt
# copy .config/config.json to a safe location and then move it back after a reset
cp .config/config.json ~/.crispy/config.json
git fetch --all
git reset --hard origin/master
mv ~/.crispy/config.json  .config/config.json
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
