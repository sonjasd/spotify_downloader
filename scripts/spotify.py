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
        
        PLAYLIST_LINK = input("Playlist/album/artist url: ")
        print("\n")

        client_credentials_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET
        )

        session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        playlist_uri_list = []

        if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
            playlist_uri = match.groups()[0]
            playlist_uri_list.append(playlist_uri)
            type = "playlist"
        elif match := re.match(r"https://open.spotify.com/album/(.*)\?", PLAYLIST_LINK):
            playlist_uri = match.groups()[0]
            playlist_uri_list.append(playlist_uri)
            type = "album"
        elif match := re.match(r"https://open.spotify.com/artist/(.*)\?", PLAYLIST_LINK):
            artist_id = match.groups()[0]
            type = "album"
            albums = session.artist_albums(artist_id)["items"]

            counter = 0

            for album in albums:
                playlist_uri_list.append(albums[counter]["id"])
                counter += 1

        else:
            raise ValueError("Invalid url...")
        
        trackslist = []
        artistslist = []

        for playlist_uri in playlist_uri_list:
            if type == "playlist":
                tracks = session.playlist_tracks(playlist_uri)["items"]
            elif type == "album":
                tracks = session.album_tracks(playlist_uri)["items"]

            for track in tracks:
                name = track["name"]
                artists = track["artists"]
                artist = artists[0]['name']

                #list inside list inside list or something, mcgyver fix for using spotify api

                trackslist.append(str(name))
                artistslist.append(str(artist))

        return trackslist, artistslist





                