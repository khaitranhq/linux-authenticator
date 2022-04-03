# linux-authenticator
Linux Authenticator base on TOTP
## Install
```
sudo apt install libgirepository1.0-dev
pip install -r ./requirements.txt
./setup.sh
```
## Create desktop application for Authenticator
Create file in `/usr/share/applications/authenticator.desktop` with content:
```
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=Authenticator
Exec="/usr/local/bin/authenticator"
Icon=/usr/local/authenticator/icon.png
Comment=Authenticator
Categories=Security;
Terminal=false
StartupNotify=true
```
