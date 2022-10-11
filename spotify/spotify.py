#!/usr/bin/env python
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

from matrix.matrix import display_image_from_url

scope = "user-library-read"
client_id="beace81697df48ca99e0496bb79dba7c"
client_secret="3d5a8e048c1b43ae86bfc6dd366efbd2"
redirect_uri="http://raspi4/callback"

my_username="vx9p6hddl4d7ymwuo1u3zvpxm"

# Initialize Spotify Client
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret,
))

def print_lz_top_songs(m):
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    results = spotify.artist_top_tracks(lz_uri)

    for track in results['tracks'][:10]:
        image_url = track['album']['images'][0]['url']
        display_image_from_url(m=m, image_url=image_url)
        time.sleep(2)

def print_my_playlists(m: RGBMatrix):
    playlists = spotify.user_playlists(my_username)
    if playlists is None:
        return
    while spotify.user_playlists(my_username):
        for i, playlist in itertools.cycle(enumerate(playlists['items'])):
            display_image_from_url(m, playlist['images'][0]['url'])
            # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
            time.sleep(2)
        if playlists['next']:
            playlists = spotify.next(playlists)
        else:
            playlists = None

def print_current_track(m: RGBMatrix):
    current = spotify.current_user_playing_track()
    print(current)

def listInfo(results: Any):
    for track in results['tracks'][:10]:
        print('track    : ' + track['name'])
        print('audio    : ' + track['preview_url'])
        print('cover art: ' + track['album']['images'][0]['url'])
