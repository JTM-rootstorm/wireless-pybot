import json
import yt_dlp


def get_video(url: str):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(json.dumps(ydl.sanitize_info(info)))
