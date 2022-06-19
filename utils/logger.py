import logging

def getlogger(filename: str = ""):

    logger = logging.getLogger("analyst")

    logger.setLevel(logging.INFO)
    # logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s - %(levelname)s] %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    if filename:
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = getlogger()