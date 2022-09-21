import os

from etc.settings import (
    logger_dir,
    logger_filename,
    logger_format,
    logger_level,
    logger_rotation,
    logger_compression,
    database_path
)
from dataclasses import dataclass


@dataclass
class LoggerConfig:
    logger_dir: str
    logger_filename: str
    logger_format: str
    logger_level: str
    logger_rotation: str
    logger_compression: str


def load_logger_config(path: str) -> LoggerConfig:
    return LoggerConfig(
        logger_dir=os.path.join(path, logger_dir),
        logger_filename=logger_filename,
        logger_format=logger_format,
        logger_level=logger_level,
        logger_rotation=logger_rotation,
        logger_compression=logger_compression
    )


def database_filename(path: str) -> str:
    return os.path.join(path, database_path)
