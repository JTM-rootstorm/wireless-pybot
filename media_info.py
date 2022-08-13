import datetime
from concurrent.futures import Future


class MediaInfo:
    """Basically just a big shell for data"""
    def __init__(self, media_path, video_title, duration, url):
        self.mediaPath = media_path
        self.videoTitle = video_title
        self.duration = duration
        self.url = url


class MediaQueue:
    def __init__(self):
        self.queue = []
        self.queue_duration = datetime.timedelta(seconds=0)

    def append(self, item):
        if item is list[MediaInfo]:
            for entry in item:
                self.queue_duration += entry.duration
        else:
            self.queue_duration += item.duration

    def pop(self) -> MediaInfo | Future[MediaInfo]:
        item = self.queue.pop()

        # subtract duration from total Q duration, return item
