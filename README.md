# pi-wall-art

Application to power wall art run on a Raspberry Pi

Experimenting currently

## Deploying

```bash
# Ensure dependencies are installed for sudo
pip freeze > requirements.txt
sudo pip install -r requirements.txt

# Copy repo to /usr/local/bin
sudo rm -rf /usr/local/bin/pi-wall-art
sudo cp -R . /usr/local/bin/pi-wall-art

# Copy service start/stop script
sudo cp rgbmatrix.sh /etc/init.d

# Add rgbmatrix.sh to startup
sudo update-rc.d rgbmatrix.sh defaults

# To manually start the controller
sudo /etc/init.d/rgbmatrix.sh start
```

## Available Pinouts

Available on Adafruit Hat/Bonnet:

- 3: SCL
- 2: SDA
- 15: RX
- 14: TX
- 25
- 10: MOSI
- 9: MISO
- 11: SCLK
- 8: CE0
- 7: CE1
- 19

Pin 24 is taken up by the 1/32 scan (64x64 matrix)

Pin 18 is taken up by the "quality" setting.
