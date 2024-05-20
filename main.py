import os
import re
from scripts.spotify import spotify_scraper
from youtube_search import YoutubeSearch
from scripts.youtube import youtube_downloader
from pandas import *

spotify = spotify_scraper()

spotify.scrape()

track_info = read_csv("track_info.csv")
 
artists = track_info['artists'].tolist()
primaryartists = track_info['primaryartist'].tolist()
tracks = track_info['track'].tolist()
albums = track_info['album'].tolist()
years = track_info['year'].tolist()
image_urls = track_info['image_url'].tolist()

search_terms = []

for x in range(len(tracks)):
    text = f'{artists[x]} {tracks[x]} Official Audio'
    search_terms.append(text)

yt_urls = []

print('\n')
prompt = 'Scraping Youtube URLs...'

for term in search_terms:
    print(prompt)
    prompt += '.'
    z = str(term)
    z = z.replace(',', ' ')
    z = re.sub('[\W_]+ ', '', z)
    z = ''.join(char for char in z if ord(char) < 128)
    z = z.replace(' ', '+')
    z = z.replace('/', ' ')

    results = YoutubeSearch(z, max_results=1).to_dict()

    yt_urls.append('https://www.youtube.com' + str(results[0]["url_suffix"]))


print('Starting to download songs on Youtube... This might take a while')

current_processing = 1
max_processing_length = len(tracks)

if os.path.exists("./songs") == False:
    print('Songs directory not found, creating folder')
    os.makedirs("./songs")

class song:
    def __init__(self, artist, primaryartist, album, song, url):
        self.artist = artist
        self.primaryartist = primaryartist
        self.album = album
        self.song = song
        self.url = url

    def download(self):
        
        if not os.path.exists(f'./songs/{self.primaryartist}/{self.album}'):
            os.makedirs(f'./songs/{self.primaryartist}/{self.album}')
        youtube_downloader.download(path=f'./songs/{self.primaryartist}/{self.album}/{self.song}', url=self.url)

for count in range(len(tracks)):

    print(f'Currently processing song {current_processing} out of {max_processing_length}')
    current_processing += 1

    current_artist = artists[count]
    current_primaryartist = primaryartists[count]
    current_song = tracks[count]
    current_album = albums[count]
    current_year = years[count]
    current_yturl = yt_urls[count]

    current_url = image_urls[count]

    current = song(artist=current_artist, primaryartist=current_primaryartist, album=current_album, song = current_song, url=current_yturl)

    current.download()
    
os.remove('track_info.csv')