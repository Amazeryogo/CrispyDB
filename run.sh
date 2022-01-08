pip3 install -r requirements.txt
# copy .config/config.json to a safe location and then move it back after a reset
git checkout master
git branch new-branch-to-save-current-commits
git fetch --all
git reset --hard origin/master
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
