import json
import os

def get_config(config_file_name: str):
    with open(config_file_name, "r") as f:
        config = json.load(f)
    return config

config_file_name = os.getenv("YOUTUBE_ANALYST_CONFIG", "./config.json")
config = get_config(config_file_name)