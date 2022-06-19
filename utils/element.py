class Element:
    def to_dict(self) -> dict:
        return self.__dict__

class Channel(Element):
    channel_id: str
    title: str
    thumbnail: str
    playlist_id: str
    update_time: int

class ChannelRecord(Element):
    channel_id: str
    view_count: int
    subscriber_count: int
    video_count: int
    record_time: int

class Video(Element):
    channel_id: str
    video_id: str
    title: str
    shorts: bool
    licensed_content: bool
    length: int
    upload_time: int
    update_time: int

class VideoRecord(Element):
    video_id: str
    view_count: int
    like_count: int
    comment_count: int
    record_time: int