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
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth, SpotifyImplicitGrant

import itertools

scope = "user-library-read"
client_id="beace81697df48ca99e0496bb79dba7c"
client_secret="3d5a8e048c1b43ae86bfc6dd366efbd2"
redirect_uri="http://raspi4/callback"

my_username="vx9p6hddl4d7ymwuo1u3zvpxm"

# def get_access_token(url, client_id, client_secret):
#     response = requests.post(
#         url,
#         data={"grant_type": "client_credentials"},
#         auth=(client_id, client_secret),
#         timeout="30"
#     )
#     return response.json()["access_token"]

auth_manager=SpotifyOAuth(
    scope=scope,
    username=my_username,
    # open_browser=True,
    # show_dialog=True
)

# spotify = spotipy.Spotify(auth_manager=auth_manager)

# Initialize Spotify Client
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret,
))

# Initialize RGB Matrix object
matrix = RGBMatrix(options=RGBMatrixOptions(
    rows=64,
    cols=64,
    brightness=70,
    pwm_dither_bits=1,
    chain_length=1,
    parallel=1,
    hardware_mapping="adafruit-hat-pwm"
))

def display_image_from_url(image_url: string):
    print(f"Displaying image {image_url}")

    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    img_data = BytesIO(response.content)

    image = Image.open(img_data)

    # Make image fit our screen.
    image.thumbnail((matrix.width, matrix.height),
                    Image.Resampling.LANCZOS)

    matrix.SetImage(image.convert('RGB'))

def print_lz_top_songs():
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    results = spotify.artist_top_tracks(lz_uri)

    for track in results['tracks'][:10]:
        image_url = track['album']['images'][0]['url']
        display_image_from_url(image_url)
        time.sleep(2)

def print_my_playlists():
    playlists = spotify.user_playlists(my_username)

    while playlists:
        for i, playlist in itertools.cycle(enumerate(playlists['items'])):
            display_image_from_url(playlist['images'][0]['url'])
            # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = spotify.next(playlists)
        else:
            playlists = None

def print_current_track():
    current = spotify.current_user_playing_track()
    print(current)

def main():
    
    print_my_playlists()

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
