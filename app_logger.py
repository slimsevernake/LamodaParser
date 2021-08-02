import logging
import logging.handlers
import os

# in case another behaviour is needed for debug output
# _log_format_debug = f"%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"
from typing import Union

LOG_FORMAT = f"%(asctime)s - %(name)s - [%(levelname)s] - (%(filename)s).%(funcName)s:%(lineno)d - %(message)s"
LOG_FOLDER = "logs/"
LOG_MAX_BYTES = 10485760  # 10 Megabytes
LOG_FILE_FORMAT = "{0:03d}--{1}.log"  # ex: 001--master.log


class DebugFilter(logging.Filter):
    """
    Filter allows only for debug messages
    """

    def filter(self, record):
        return record.levelno == logging.DEBUG


class SectionAdapter(logging.LoggerAdapter):
    """
    Adapter adds section field for logger
    """
    SECTION_SIZE = 300  # number of records for each section
    _section_id = 0  # current section
    _current_section_counter = 0  # number of record inside current section

    def process(self, msg, kwargs):
        SectionAdapter._current_section_counter += 1

        if SectionAdapter._current_section_counter == SectionAdapter.SECTION_SIZE:
            SectionAdapter._section_id += 1
            SectionAdapter._current_section_counter = 0

        return f'[SEC: {SectionAdapter._section_id}]:\t{msg}', kwargs


def generate_new_log_name(name: 'str') -> 'str':
    """
    Create new log file name

    :param name: logger name
    :return: filename of new log journal
    """
    file_count = len([f for f in os.listdir(LOG_FOLDER)])
    new_name = LOG_FILE_FORMAT.format(file_count, name)
    return new_name


def get_file_handler(name: 'str') -> 'logging.FileHandler':
    """
    Create file handler

    :param name: logger name
    :return: file handler
    """
    log_file = f"{LOG_FOLDER}{generate_new_log_name(name)}"

    # handler for different output for debug
    # file_handler_debug = logging.FileHandler(log_file)
    # file_handler_debug.setLevel(logging.DEBUG)
    # file_handler_debug.addFilter(DebugFilter())
    # file_handler_debug.setFormatter(logging.Formatter(_log_format_debug))

    file_handler_others = logging.handlers.RotatingFileHandler(log_file, maxBytes=LOG_MAX_BYTES, backupCount=100)
    file_handler_others.setLevel(logging.DEBUG)  # should be replaced to logging.INFO
    file_handler_others.setFormatter(logging.Formatter(LOG_FORMAT))

    return file_handler_others  # file_handler_debug, file_handler_others


def get_stream_handler() -> 'logging.StreamHandler':
    """
    Create stream handler

    :return:
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return stream_handler


def get_logger(name: 'str', level: 'int' = logging.DEBUG) -> 'Union[logging.Logger, logging.LoggerAdapter]':
    """
    Create logger

    :param name: logger name
    :param level: logging level
    :return: new logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.addHandler(get_file_handler(name))
    logger.addHandler(get_stream_handler())
    logger = SectionAdapter(logger, {"section": 0})
    return logger
