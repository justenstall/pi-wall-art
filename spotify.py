#!/usr/bin/env python
from mimetypes import init
import requests
import string
import time
import sys
from typing import Any
from io import BytesIO
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

my_username="vx9p6hddl4d7ymwuo1u3zvpxm"

# spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Initialize Spotify Client
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id="beace81697df48ca99e0496bb79dba7c",
    client_secret="3d5a8e048c1b43ae86bfc6dd366efbd2",
))

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

    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    img_data = BytesIO(response.content)

    image = Image.open(img_data)

    # Make image fit our screen.
    image.thumbnail((matrix.width, matrix.height),
                    Image.Resampling.LANCZOS)

    matrix.SetImage(image.convert('RGB'))


def main():
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    results = spotify.artist_top_tracks(lz_uri)

    for track in results['tracks'][:10]:
        image_url = track['album']['images'][0]['url']
        displayImageFromURL(image_url)
        time.sleep(2)
    
    playlists = spotify.user_playlists(my_username)

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            playlist['images'][0]['url']
            # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = spotify.next(playlists)
        else:
            playlists = None

    try:
        print("Press CTRL-C to stop.")
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
