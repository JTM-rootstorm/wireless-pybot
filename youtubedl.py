import json
import sys

# we're going to ignore the horrible things I have to do here
sys.path.append("./yt-dlp")
# noinspection PyUnresolvedReferences
import yt_dlp


def get_video(url: str):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(json.dumps(ydl.sanitize_info(info)))
