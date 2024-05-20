import csv
import os
import re

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

if os.path.exists('.env') == False:
    with open('.env', 'w') as f:
        f.write('CLIENT_ID=\nCLIENT_SECRET=')
        f.close()

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
OUTPUT_FILE_NAME = "track_info.csv"

class spotify:
    def __init__(self):
        return
    
    def fetch(self):
        
        PLAYLIST_LINK = input("Playlist url: ")
        print("\n")

        client_credentials_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET
        )

        session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
            playlist_uri = match.groups()[0]
            type = "playlist"
        elif match := re.match(r"https://open.spotify.com/album/(.*)\?", PLAYLIST_LINK):
            playlist_uri = match.groups()[0]
            type = "album"
        else:
            raise ValueError("Expected format: https://open.spotify.com/playlist/ or https://open.spotify.com/album/...")

        if type == "playlist":
            tracks = session.playlist_tracks(playlist_uri)["items"]
        elif type == "album":
            tracks = session.album_tracks(playlist_uri)["items"]

        trackslist = []
        artistslist = []

        for track in tracks:
            name = track["name"]
            primaryartist = ["artists"]

            trackslist.append(str(track["name"]))
            artistslist.append(str(track["artists"]))

        return trackslist, artistslist





                