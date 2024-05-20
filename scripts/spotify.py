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
        else:
            raise ValueError("Expected format: https://open.spotify.com/playlist/...")

        tracks = session.playlist_tracks(playlist_uri)["items"]

        with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
    
            writer.writerow(["primaryartist", "artists", "track", "album", "year", "image_url"])

            prompt = 'Scraping playlists tracks and their info...'

            for track in tracks:
                print(prompt)
                name = track["track"]["name"]
                primaryartist = track["track"]["artists"][0]["name"]
                artists = ", ".join(
                    [artist["name"] for artist in track["track"]["artists"]]
                )
                album = track["track"]["album"]["name"]
                year = track["track"]["album"]["release_date"]
                year = year[:4]
                image_url = track["track"]["album"]["images"][0]["url"]

                prompt += '.'
        
                writer.writerow([primaryartist, artists, name, album, year, image_url])