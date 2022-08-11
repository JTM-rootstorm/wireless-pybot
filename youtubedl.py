import datetime
import json
import yt_dlp


def get_video(url: str):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': './media/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        sanitized_info = json.loads(json.dumps(ydl.sanitize_info(info)))

        print(sanitized_info["requested_downloads"][0]["filepath"])

        (video_title, video_duration, file_path) = (sanitized_info["title"],
                                                    datetime.timedelta(seconds=int(sanitized_info["duration"])),
                                                    sanitized_info["requested_downloads"][0]["filepath"])

        return video_title, video_duration, file_path
