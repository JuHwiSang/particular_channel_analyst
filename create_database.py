# from ._config import config
from utils.get_config import config
from utils.database import Database

CREATE_DATABASE = """CREATE DATABASE IF NOT EXISTS {database} default character set utf8mb4 collate utf8mb4_general_ci;"""
USE_DATABASE = """USE {database}"""
CREATE_TABLE_CHANNEL = """CREATE TABLE IF NOT EXISTS channel (
    channel_id varchar(24) primary key,
    title binary(120),
    thumbnail varchar(200),
    playlist_id varchar(24),
    update_time integer
);"""
CREATE_TABLE_CHANNEL_RECORD = """CREATE TABLE IF NOT EXISTS channel_record (
    channel_id varchar(24),
    view_count integer,
    subscriber_count integer,
    video_count integer,
    record_time integer
);"""
CREATE_TABLE_VIDEO = """CREATE TABLE IF NOT EXISTS video (
    channel_id varchar(24),
    video_id varchar(24) primary key,
    title varchar(255),
    shorts boolean,
    licensed_content boolean,
    length integer,
    upload_time integer,
    update_time integer
);"""
CREATE_TABLE_VIDEO_RECORD = """CREATE TABLE IF NOT EXISTS video_record (
    video_id varchar(24),
    view_count integer,
    like_count integer,
    comment_count integer,
    record_time integer
);"""



def create():

    db_name = config['database']['database']
    db = Database(
        user=config['database']['user'],
        passwd=config['database']['passwd'],
        host=config['database']['host'],
        charset=config['database']['charset']
    )

    db.execute(CREATE_DATABASE.format(database=db_name))
    db.execute(USE_DATABASE.format(database=db_name))
    db.execute(CREATE_TABLE_CHANNEL)
    db.execute(CREATE_TABLE_CHANNEL_RECORD)
    db.execute(CREATE_TABLE_VIDEO)
    db.execute(CREATE_TABLE_VIDEO_RECORD)

    print("succeed")
    db.commit()
    db.close()


if __name__ == "__main__":
    create()