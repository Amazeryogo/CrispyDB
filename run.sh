#debian family (debian,raspbian,ubuntu,mint) only, hash if you want to use it on other distros
sudo apt update && sudo apt full-upgrade
#arch family (arch, manjaro) only, hash if you want to use it on other distros
sudo pacman -Syu
#suse family (suse, opensuse) only, hash if you want to use it on other distros
sudo zypper update
#fedora family (fedora) only, hash if you want to use it on other distros
sudo dnf update
#centos family (centos, rhel) only, hash if you want to use it on other distros
sudo yum update
#gentoo family (gentoo) only, hash if you want to use it on other distros
sudo emerge --sync

pip3 install -r requirements.txt 
python3 main.py
# End: run.sh