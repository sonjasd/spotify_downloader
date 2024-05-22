import yt_dlp as youtube_dl

class youtube_downloader:
    def __init__(self):
        return
    def download(path, url):
        path = f'{path}'
        with youtube_dl.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': path, 'postprocessors':[{'key':'FFmpegExtractAudio', 'preferredcodec':'mp3', 'preferredquality':'192',}]}) as video:
            video.download(url)
