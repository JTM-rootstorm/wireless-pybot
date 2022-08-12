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
        download_type = sanitized_info['_type']
        if download_type is "video":
            download_video(url)
        elif download_type is "playlist":
            (video_list, media_info_list) = process_playlist(sanitized_info)
            download_video(video_list)
        else:
            pass


def process_playlist(json_info) -> (list, list[MediaInfo]):
    video_list = json_info['entries']
    video_urls = []
    videos: list[MediaInfo] = []
    for item in video_list:
        video_urls.append(item['webpage_url'])

        (video_title, video_duration, file_path) = (item["title"],
                                                    datetime.timedelta(seconds=int(item["duration"])),
                                                    item["requested_downloads"][0]["filepath"])
        videos.append(MediaInfo(file_path, video_title, video_duration))

    return video_urls, videos


def extract_json(url: str):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return sanitize_json(ydl.sanitize_info(info))


def download_video(url):
    url_list = []
    if url is not list:
        url_list.append(url)
    else:
        url_list = url

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url_list)


def sanitize_json(_input):
    return json.loads(json.dumps(_input))
