import datetime
import logging
import os

_log_format = f"%(asctime)s - [%(levelname)s] - %(message)s"
_log_folder = "logs/"

_log_file_format = "{0:03d}--common.log"


def get_new_log_name():
    path, dirs, files = next(os.walk(_log_folder))
    file_count = len(files)
    new_name = _log_file_format.format(file_count+1)
    return new_name


def get_file_handler():
    file_handler = logging.FileHandler(f"{_log_folder}{get_new_log_name()}")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
