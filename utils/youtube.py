from datetime import datetime
from typing import Iterable
import requests
import json
import time
import isodate

from .element import ChannelRecord, VideoRecord, Video, Channel
from .helpers import strptime_to_second
from .logger import logger

REQUIRE_VIDEOS_BY_PLAYLIST = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={api_key}"
REQUIRE_VIDEOS_BY_PLAYLIST_PAGE_TOKEN = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={api_key}&pageToken={page_token}"
REQUIRE_CHANNEL = "https://www.googleapis.com/youtube/v3/channels?part=snippet,contentDetails,statistics&id={channel_id}&key={api_key}"
REQUIRE_VIDEO = "https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id}&key={api_key}"
strptime_format = "%Y-%m-%dT%H:%M:%SZ"


class Youtube:
    _api_key: str
    used_quota: int
    
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self.used_quota = 0

    def request_json(self, *args, **kwargs):
        self.used_quota += 1
        return request_json(*args, **kwargs)

    def require_channel(self, channel_id: str) -> tuple[Channel, ChannelRecord]:
        res = self.request_json(REQUIRE_CHANNEL.format(channel_id=channel_id, api_key=self._api_key))
        return item2channel(res['items'][0]), item2channel_record(res['items'][0])

    def require_video(self, video_id: str) -> tuple[Video, VideoRecord]:
        res = self.request_json(REQUIRE_VIDEO.format(video_id=video_id, api_key=self._api_key))
        return item2video(res['items'][0]), item2video_record(res['items'][0])

    def require_videos(self, video_ids: Iterable[str], max_results: int = 50) -> list[tuple[Video, VideoRecord]]:
        video_list = []
        for i in range(0, len(video_ids), max_results):
            require_ids = video_ids[i:i+max_results]
            res = self.request_json(REQUIRE_VIDEO.format(video_id=",".join(require_ids), api_key=self._api_key))
            video_list.extend([(item2video(item), item2video_record(item)) for item in res['items']])
        return video_list


    def require_videos_by_playlist(self, playlist_id: str, max_results: int = 50) -> list[Video]:
        video_list = []

        res = self.request_json(REQUIRE_VIDEOS_BY_PLAYLIST.format(playlist_id=playlist_id, max_results=max_results, api_key=self._api_key))
        page_token = res.get('nextPageToken', '')
        # video_list.extend([(item2video(item), item2video_record(item)) for item in res['items']])
        video_list.extend([item2video(item) for item in res['items']])

        # length = res['pageInfo']['totalResults']//max_results

        while page_token:
            res = self.request_json(REQUIRE_VIDEOS_BY_PLAYLIST_PAGE_TOKEN.format(playlist_id=playlist_id, max_results=max_results, api_key=self._api_key, page_token=page_token))
            page_token = res.get('nextPageToken', '')
            video_list.extend([item2video(item) for item in res['items']])
    
        return video_list
            


def item2channel(res: dict) -> Channel:
    precent_time = time.time()
    channel = Channel()
    channel.channel_id = res['id']
    channel.title = res['snippet']['title']
    channel.thumbnail = res['snippet']['thumbnails']['default']['url']
    channel.playlist_id = res['contentDetails']['relatedPlaylists']['uploads']
    channel.update_time = precent_time
    return channel
    
def item2channel_record(res: dict) -> ChannelRecord:
    precent_time = time.time()
    channel_record = ChannelRecord()
    channel_record.channel_id = res['id']
    channel_record.view_count = int(res['statistics'].get('viewCount', -1))
    channel_record.subscriber_count = int(res['statistics'].get('subscriberCount', -1))
    channel_record.video_count = int(res['statistics'].get('videoCount', -1))
    channel_record.record_time = precent_time
    return channel_record

def item2video(res: dict) -> Video:
    precent_time = time.time()
    video = Video()
    video.channel_id = res['snippet']['channelId']
    # video.video_id = res['id']
    try:
        video.video_id = res['snippet']['resourceId']['videoId']
    except KeyError:
        video.video_id = res['id'] #videos
    video.title = res['snippet']['title']
    video.shorts = is_shorts(res['snippet']['title'], res['snippet']['description'])
    video.licensed_content = res['contentDetails'].get('licensedContent', False)
    video.length = get_video_length(res['contentDetails'].get('duration', 'PT0S'))
    # video.licensed_content = res['contentDetails']['licensedContent']
    # video.length = get_video_length(res['contentDetails']['duration'])
    video.upload_time = strptime_to_second(datetime.strptime(res['snippet']['publishedAt'], strptime_format))
    video.update_time = precent_time
    return video

def item2video_record(res: dict) -> VideoRecord:
    precent_time = time.time()
    video_record = VideoRecord()
    video_record.video_id = res['id']
    video_record.view_count = int(res['statistics'].get('viewCount', -1))
    video_record.like_count = int(res['statistics'].get('likeCount', -1))
    video_record.comment_count = int(res['statistics'].get('commentCount', -1))
    video_record.record_time = precent_time
    return video_record


def request_json(url: str) -> dict:
    res = requests.get(url)
    logger.debug(f"{url} ### res: {len(res.text)}")
    # print(res.text)
    return json.loads(res.text)

def is_shorts(title: str, description: str) -> bool:
    if "#shorts" in title or "#shorts" in description:
        return True
    else:
        return False

def get_video_length(duration: str) -> int:
    return int(isodate.parse_duration(duration).total_seconds())