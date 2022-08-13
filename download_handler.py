from concurrent.futures import Future

import youtubedl
import concurrent.futures

from media_info import MediaInfo

executor = concurrent.futures.ProcessPoolExecutor()


def queue_video_for_download(media_info: MediaInfo) -> Future[MediaInfo]:
    return executor.submit(youtubedl.download_video, media_info)
