# from ..utils.config import config
from utils.database import Database
from utils.youtube import Youtube
from utils.helpers import is_err
from utils.logger import logger
from pymysql.err import DatabaseError
# from ..utils.database import connect


class Recorder:

    database: Database
    youtube: Youtube

    def __init__(self, database, youtube) -> None:
        self.database = database
        self.youtube = youtube

    # def db_channel_exist(self, channel_id: str) -> bool: ...

    # def db_create_channel_info(self, channel_id: str) -> str: ...

    # def db_get_channel_info(self, channel_id: str) -> str: ...

    def record(self, channel_id: str) -> None:
        channel, channel_record = self.youtube.require_channel(channel_id)

        try:
            last_update_time = self.database.select_channel(channel_id).update_time
            last_video_count = self.database.select_channel_record_by_update_time(channel_id, last_update_time).video_count
            if channel_record.video_count > last_video_count:
                logger.info(f"video_count change: {last_video_count} -> {channel_record.video_count}")
                videos = self.youtube.require_videos_by_playlist(channel.playlist_id)
            else:
                videos = self.database.select_channel_videos(channel_id)
        except IndexError:
            # raise e
            logger.info(f"No channel information")
            videos = self.youtube.require_videos_by_playlist(channel.playlist_id)
        video_ids = tuple(map(lambda x:x.video_id, videos))
        bundles = self.youtube.require_videos(video_ids)

        for video, video_record in bundles:
            if is_err(IndexError, self.database.select_video, (video.video_id,)):
                logger.info(f"NEW VIDEO: {video.video_id}")
                self.database.insert_video(video)
            else:
                self.database.update_video(video)
            self.database.insert_video_record(video_record)

        if is_err(IndexError, self.database.select_channel, (channel_id,)):
            logger.info(f"NEW CHANNEL: {channel_id}")
            self.database.insert_channel(channel)
        else:
            self.database.update_channel(channel)
        self.database.insert_channel_record(channel_record)
            
        # for video, video_record in bundles:
        #     self.database.update_video(video)
        #     self.database.insert_video_record(video_record)