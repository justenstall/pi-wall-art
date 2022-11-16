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

import itertools

from matrix import Matrix

scope = "user-library-read"
client_id="beace81697df48ca99e0496bb79dba7c"
client_secret="3d5a8e048c1b43ae86bfc6dd366efbd2"
redirect_uri="http://127.0.0.1/callback"

my_username="vx9p6hddl4d7ymwuo1u3zvpxm"

# Initialize Spotify Client
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret,
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
    response = spotify.user_playlists(my_username)
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


spotify_user = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
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