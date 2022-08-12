import datetime
import json
import yt_dlp


ydl_opts = {
        'format': 'mp4',
        'outtmpl': './media/%(title)s.%(ext)s'
    }


def get_video(url: str):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        sanitized_info = sanitize_json(ydl.sanitize_info(info))

        (video_title, video_duration, file_path) = (sanitized_info["title"],
                                                    datetime.timedelta(seconds=int(sanitized_info["duration"])),
                                                    sanitized_info["requested_downloads"][0]["filepath"])

        return video_title, video_duration, file_path


def output_trash(url: str):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        sanitized_info = sanitize_json(ydl.sanitize_info(info))

        if "youtube" in sanitized_info['webpage_url']:
            download_type = sanitized_info['_type']
            if download_type is "video":
                pass
            elif download_type is "playlist":
                pass
            else:
                pass


def sanitize_json(_input):
    return json.loads(json.dumps(_input))
