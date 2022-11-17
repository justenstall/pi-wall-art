# pi-wall-art

Application to power wall art run on a Raspberry Pi.

## Authentication

API authentication is needed for APIs used in the program. These are stored in a file called `mysecrets.py` in the `src` folder.

The format is as follows:

```python
# This file is where you keep secret settings, passwords, and tokens!
# If you put them in the code you risk committing that info or sharing it
# which would be not great. So, instead, keep it all in this one file and
# keep it a secret.

spotify = {
    "scope": "user-library-read",
    "client_id": "<spotify application client ID>",
    "client_secret": "<spotify application client secret>",
    "redirect_uri": "<redirect uri set for spotify application>",
    "username": "<your spotify username>",
}

nasa = {
    'api_key': '<nasa api key>',
}
```

## Deploying

```bash
# Ensure dependencies are installed for root
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

## rpi-rgb-led-matrix

`sudo led-image-viewer --led-rows=64 --led-cols=64 --led-gpio-mapping=adafruit-hat-pwm --led-slowdown-gpio=4 --led-brightness=70 --led-show-refresh --led-pwm-dither-bits=1 <image>`
