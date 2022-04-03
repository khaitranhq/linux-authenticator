#!/bin/bash

PWD=$(pwd)
INSTALL_DIR='/usr/local/authenticator'
pyinstaller --onedir --noconfirm $PWD/authenticator.py
sudo rm -rf $INSTALL_DIR
sudo mkdir -p $INSTALL_DIR
sudo cp -r $PWD/dist $INSTALL_DIR
sudo cp $PWD/icon.png $INSTALL_DIR
sudo ln -sf $INSTALL_DIR/dist/authenticator/authenticator /usr/local/bin/authenticator
