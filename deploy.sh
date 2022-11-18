sudo rm -rf /usr/local/bin/pi-wall-art
sudo cp -R . /usr/local/bin/pi-wall-art

sudo cp rgbmatrix.sh /etc/init.d

sudo /etc/init.d/rgbmatrix.sh stop
sudo /etc/init.d/rgbmatrix.sh start

sudo cp shutdown-button.py /usr/local/bin

sudo cp shutdown-button.sh /etc/init.d

sudo /etc/init.d/shutdown-button.sh stop
sudo /etc/init.d/shutdown-button.sh start
