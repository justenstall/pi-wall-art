#!/usr/bin/env python
from mimetypes import init
import requests
import string
import time
import sys
from typing import Any
import io
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize Spotify Client
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.brightness = 70
# options.show_refresh_rate = True
options.pwm_dither_bits = 1
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'

# Initialize RGB Matrix object
matrix = RGBMatrix(options=options)

def displayImageFromURL(image_url: string):
    print(f"Displaying image {image_url}")

    img_data = requests.get(image_url).content

    image = Image.open(io.BytesIO(img_data))

    # Make image fit our screen.
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

    matrix.SetImage(image.convert('RGB'))

def main():
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    results = spotify.artist_top_tracks(lz_uri)

    for track in results['tracks'][:10]:
        image_url = track['album']['images'][0]['url']
        # print(image_url)
        # displayImageFromURL(image_url)
        print(f"Displaying image {image_url}")

        img_data = requests.get(image_url).content

        image = Image.open(io.BytesIO(img_data))

        # Make image fit our screen.
        image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

        matrix.SetImage(image.convert('RGB'))
        time.sleep(2)

    # image_url = results['tracks'][0]['album']['images'][0]['url']

    # displayImageFromURL(image_url)

    try:
        # print("Press CTRL-C to stop.")
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        sys.exit(0)

def listInfo(results: Any):
    for track in results['tracks'][:10]:
        print('track    : ' + track['name'])
        print('audio    : ' + track['preview_url'])
        print('cover art: ' + track['album']['images'][0]['url'])

if __name__ == "__main__":
    main()
