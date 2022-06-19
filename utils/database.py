from ctypes import Union
from typing import Iterable, Mapping
from pymysql.cursors import Cursor, DictCursor
from pymysql.connections import Connection
from pandas import DataFrame, Series
import pymysql

from .element import Video, Channel
from .element import ChannelRecord, VideoRecord
from .logger import logger


INSERT_CHANNEL = """INSERT INTO channel VALUES (
                  %(channel_id)s,
                  %(title)s,
                  %(thumbnail)s,
                  %(playlist_id)s,
                  %(update_time)s
                  )"""
INSERT_CHANNEL_RECORD = """INSERT INTO channel_record VALUES (
                         %(channel_id)s,
                         %(view_count)s,
                         %(subscriber_count)s,
                         %(video_count)s,
                         %(record_time)s
                         )"""
INSERT_VIDEO = """INSERT INTO video VALUES (
                  %(channel_id)s,
                  %(video_id)s,
                  %(title)s,
                  %(shorts)s,
                  %(licensed_content)s,
                  %(length)s,
                  %(upload_time)s,
                  %(update_time)s
                  )"""
INSERT_VIDEO_RECORD = """INSERT INTO video_record VALUES (
                         %(video_id)s,
                         %(view_count)s,
                         %(like_count)s,
                         %(comment_count)s,
                         %(record_time)s
                         )"""
UPDATE_VIDEO = """UPDATE video SET
                  title=%(title)s,
                  shorts=%(shorts)s,
                  licensed_content=%(licensed_content)s,
                  length=%(length)s,
                  update_time=%(update_time)s
                  WHERE video_id=%(video_id)s"""
UPDATE_CHANNEL = """UPDATE channel SET
                    title=%(title)s,
                    thumbnail=%(thumbnail)s,
                    playlist_id=%(playlist_id)s,
                    update_time=%(update_time)s
                    WHERE channel_id=%(channel_id)s"""
SELECT_VIDEO = "SELECT * FROM video WHERE video_id=%(video_id)s"
SELECT_VIDEO_RECORD = "SELECT * FROM video_record WHERE video_id=%(video_id)s"
SELECT_CHANNEL = "SELECT * FROM channel WHERE channel_id=%(channel_id)s"
SELECT_CHANNEL_RECORD = "SELECT * FROM channel_record WHERE channel_id=%(channel_id)s"
SELECT_CHANNEL_VIDEOS = "SELECT * FROM video WHERE channel_id=%(channel_id)s"
SELECT_CHANNEL_RECORD_BY_UPDATE_TIME = "SELECT * FROM channel_record WHERE record_time=%(record_time)s and channel_id=%(channel_id)s"


class Database:
    
    _db: Connection
    _cursor: Cursor

    def __init__(self, user, passwd, host, charset, database = None):
        kwargs = {
            "user": user,
            "passwd": passwd,
            "host": host,
            "charset": charset
        }
        if database is not None:
            kwargs.update({"database": database})

        self._db = pymysql.connect(**kwargs)
        self._cursor = self._db.cursor(DictCursor)

    def execute(self, sql: str, querys: Union[Iterable, Mapping] = ()) -> DataFrame:
        # logger.debug(f"{sql} ### {querys}")
        self._cursor.execute(sql, querys)
        return DataFrame(self._cursor.fetchall())
        
    def insert_video(self, video: Video) -> None:
        self.execute(INSERT_VIDEO, video.to_dict())

    def insert_video_record(self, video_record: VideoRecord) -> None:
        self.execute(INSERT_VIDEO_RECORD, video_record.to_dict())

    def insert_channel(self, channel: Channel) -> None:
        self.execute(INSERT_CHANNEL, channel.to_dict())

    def insert_channel_record(self, channel_record: ChannelRecord) -> None:
        self.execute(INSERT_CHANNEL_RECORD, channel_record.to_dict())

    def update_channel(self, channel: Channel) -> None:
        self.execute(UPDATE_CHANNEL, channel.to_dict())
    
    def update_video(self, video: Video) -> None:
        self.execute(UPDATE_VIDEO, video.to_dict())
    
    def select_channel(self, channel_id: str) -> Channel:
        return row2channel(self.execute(SELECT_CHANNEL, {'channel_id': channel_id}).iloc[0])

    def select_channel_record(self, channel_id: str) -> tuple[ChannelRecord]:
        return tuple(map(lambda x:row2channel_record(x), self.execute(SELECT_CHANNEL_RECORD, {'channel_id': channel_id}).iloc))

    def select_video(self, video_id: str) -> Video:
        return row2video(self.execute(SELECT_VIDEO, {'video_id': video_id}).iloc[0])

    def select_video_record(self, video_id: str) -> tuple[VideoRecord]:
        return tuple(map(lambda x:row2video_record(x), self.execute(SELECT_VIDEO_RECORD, {'video_id': video_id}).iloc))

    def select_channel_videos(self, channel_id: str) -> tuple[Video]:
        return tuple(map(lambda x:row2video(x), self.execute(SELECT_CHANNEL_VIDEOS, {'channel_id': channel_id}).iloc))

    def select_channel_record_by_update_time(self, channel_id: str, update_time: str) -> ChannelRecord:
        return row2channel_record(self.execute(SELECT_CHANNEL_RECORD_BY_UPDATE_TIME, {'channel_id': channel_id, 'record_time': update_time}).iloc[0])

    def commit(self) -> None:
        self._db.commit()
    
    def close(self) -> None:
        self._db.close()



def row2channel(row: Series) -> Channel:
    channel = Channel()
    channel.channel_id = row['channel_id']
    channel.title = row['title']
    channel.thumbnail = row['thumbnail']
    channel.playlist_id = row['playlist_id']
    channel.update_time = row['update_time']
    return channel

def row2channel_record(row: Series) -> ChannelRecord:
    channel_record = ChannelRecord()
    channel_record.channel_id = row['channel_id']
    channel_record.video_count = row['view_count']
    channel_record.subscriber_count = row['subscriber_count']
    channel_record.video_count = row['video_count']
    channel_record.record_time = row['record_time']
    return channel_record

def row2video(row: Series) -> Video:
    video = Video()
    video.channel_id = row['channel_id']
    video.video_id = row['video_id']
    video.title = row['title']
    video.shorts = row['shorts']
    video.licensed_content = row['licensed_content']
    video.length = row['length']
    video.upload_time = row['upload_time']
    video.update_time = row['update_time']
    return video

def row2video_record(row: Series) -> VideoRecord:
    video_record = VideoRecord()
    video_record.video_id = row['video_id']
    video_record.view_count = row['view_count']
    video_record.like_count = row['like_count']
    video_record.comment_count = row['comment_count']
    video_record.record_time = row['record_time']
    return video_record