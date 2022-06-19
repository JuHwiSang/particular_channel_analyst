from recorder.recorder import Recorder
from utils.get_config import config
from utils.database import Database
from utils.youtube import Youtube
from utils.logger import logger

def main():
    database = Database(**config['database'])
    youtube = Youtube(config['youtube']['api_key'])
    recorder = Recorder(database, youtube)
    for channel_id in config['youtube']['channels']:
        recorder.record(channel_id)

    database.commit()
    database.close()
    
    logger.debug(f"used quota: {youtube.used_quota}")

if __name__ == "__main__":
    main()