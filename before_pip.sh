apt update -y
apt install -y python-dev-is-python3 portaudio19-dev
apt autoremove -y
# wifi AP setup
# use raspi-config to set wifi region
#sudo nmcli device wifi hotspot ssid <ssid> password <password>
