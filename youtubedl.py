import concurrent.futures
import datetime
import json
import os
import yt_dlp

from media_info import MediaInfo

download_path = os.getenv("DOWNLOAD_PATH")

ydl_opts = {
    'format': 'mp4',
    'outtmpl': f"{download_path}/%(title)s.%(ext)s"
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
    sanitized_info = extract_json(url)
    if "youtube" in sanitized_info['webpage_url']:
        return process_playlist(sanitized_info)

    return None


def process_playlist(url: str) -> list[MediaInfo]:
    json_info = extract_json(url)

    url_type = json_info['_type']
    videos: list[MediaInfo] = []

    if url_type is "playlist":
        video_list = json_info['entries']
        for item in video_list:
            videos.append(create_media_info(item))
    else:
        videos.append(create_media_info(json_info))

    return videos


def extract_json(url: str):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return sanitize_json(ydl.sanitize_info(info))


def download_video(media_info: MediaInfo) -> MediaInfo | None:
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(media_info.url)
            return media_info
    except (concurrent.futures.CancelledError, concurrent.futures.TimeoutError):
        return None


def create_media_info(video_info) -> MediaInfo:
    (video_title, video_duration, file_path, web_url) = (video_info["title"],
                                                         datetime.timedelta(seconds=int(video_info["duration"])),
                                                         video_info["requested_downloads"][0]["filepath"],
                                                         video_info['webpage_url'])
    return MediaInfo(file_path, video_title, video_duration, web_url)


def sanitize_json(_input):
    return json.loads(json.dumps(_input))
