from mimetypes import init
import string
import PIL
import requests
import time
import sys
from typing import Any
from io import BytesIO
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth, SpotifyImplicitGrant
from urllib.request import urlopen
from mysecrets import spotify as secrets

import itertools

from matrix import Matrix

scope = "user-library-read"

# Initialize Spotify Client
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=secrets['client_id'],
    client_secret=secrets['client_secret'],
))

def print_lz_top_songs(m: Matrix):
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    results = spotify.artist_top_tracks(lz_uri)
    if results:
        for track in results['tracks'][:10]:
            image_url = track['album']['images'][0]['url']
            # m.display_image_from_url(image_url)
            time.sleep(2)

def print_my_playlists(m: Matrix):
    response = spotify.user_playlists(secrets['username'])
    if response:
        image_urls = [playlist['images'][0]['url'] for playlist in response['items']]
        m.loop_image_urls(image_urls)

def print_current_track(m: RGBMatrix):
    current = spotify.current_user_playing_track()
    print(current)

def listInfo(results: Any):
    for track in results['tracks'][:10]:
        print('track    : ' + track['name'])
        print('audio    : ' + track['preview_url'])
        print('cover art: ' + track['album']['images'][0]['url'])

m = Matrix()
m.resampling = Image.Resampling.NEAREST


spotify_user = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=secrets['client_id'],
                                                client_secret=secrets['client_secret'],
                                                redirect_uri=secrets['redirect_uri'],
                                                scope="user-library-read",
                                                open_browser=False))

current = spotify_user.current_user_playing_track()
if current == None:
    sys.exit(1)
image_url = current['album']['images'][0]['url']
# m.display_image_from_url(image_url)
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])