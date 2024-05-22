import re
from scripts.spotify import spotify
from youtube_search import YoutubeSearch
from scripts.youtube import youtube_downloader
from pandas import *
import os

spotify = spotify()

trackslist, artistslist = spotify.fetch()

print('\n')

print('Starting to download songs on Youtube... This might take a while')

current_processing = 1
max_processing_length = len(trackslist)

if os.path.exists("./songs") == False:
    print('Songs directory not found, creating folder')
    os.makedirs("./songs")

class musicdl:
    def __init__(self, artist, song, url):
        self.artist = artist
        self.song = song
        self.url = url

    def download(self):
        
        if not os.path.exists(f'./songs'):
            os.makedirs(f'./songs')
        songpath = (f'./songs/{self.artist} - {self.song}')
        if not os.path.exists(songpath):
            youtube_downloader.download(path=songpath, url=self.url)
        else:
            print(self.song + " already exists, skipping")

for count in range(len(trackslist)):

    print(f'Currently processing song {current_processing} out of {max_processing_length}')
    current_processing += 1

    current_artist = artistslist[count]
    current_song = trackslist[count]

    text = f'{current_artist} {current_song} Official Audio Lyric Video'

    z = str(text)
    z = z.replace(',', ' ')
    z = re.sub('[\W_]+ ', '', z)
    z = ''.join(char for char in z if ord(char) < 128)
    z = z.replace(' ', '+')
    z = z.replace('/', ' ')

    results = YoutubeSearch(z, max_results=1).to_dict()

    current_url = 'https://www.youtube.com' + str(results[0]["url_suffix"])

    current = musicdl(artist=current_artist, song = current_song, url=current_url)

    current.download()