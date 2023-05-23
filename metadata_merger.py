import requests
import shutil
import os
import eyed3
from mutagen.id3 import ID3, TIT2, TALB, TYER, TPE1
from eyed3.id3.frames import ImageFrame

class metadata_merger:
    def __init__(self):
        return
    def merge(self, url, track, primaryartist, artist, album, year):
        self.url = url
        self.track = track
        self.artist = artist
        self.album = album
        self.year = year
        self.primaryartist = primaryartist

        path = f'./songs/{primaryartist}/{album}/'
        filepath = f'{path}/{track}'

        res = requests.get(url, stream = True)

        if res.status_code == 200:
            with open(filepath + '.jpg','wb') as f:
                shutil.copyfileobj(res.raw, f)

        audio = ID3(f'{filepath}.mp3')

        audio["TIT2"] = TIT2(encoding=3, text=track)
        audio["TALB"] = TALB(encoding=3, text=album)
        audio["TYER"] = TYER(encoding=3, text=str(year))
        audio["TPE1"] = TPE1(encoding=3, text=artist)

        audio.save()

        audiofile = eyed3.load(filepath + '.mp3')

        if (audiofile.tag == None):
            audiofile.initTag()

        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(filepath + '.jpg','rb').read(), 'image/jpeg')

        audiofile.tag.save()

        os.remove(filepath + '.jpg')