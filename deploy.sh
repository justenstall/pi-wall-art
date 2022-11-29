#!/bin/bash

# Destroy old setup
sudo rm -rf /usr/local/bin/pi-wall-art
sudo /etc/init.d/rgbmatrix.sh stop
sudo /etc/init.d/shutdown-button.sh stop

# Copy new python files
sudo cp -R . /usr/local/bin/pi-wall-art
sudo cp shutdown-button/shutdown-button.py /usr/local/bin

# Copy new daemon files
sudo cp rgbmatrix.sh /etc/init.d
sudo cp shutdown-button/shutdown-button.sh /etc/init.d

# Start up new setup
sudo /etc/init.d/rgbmatrix.sh start
sudo /etc/init.d/shutdown-button.sh start
