import os
import platform

from loguru import logger

import loader
from etc import LoggerConfig, load_logger_config, database_filename


def configure_logger(logger_config: LoggerConfig) -> None:
    logger.add(
        os.path.join(os.path.dirname(__file__), logger_config.logger_dir + '/' + logger_config.logger_filename),
        format=logger_config.logger_format,
        level=logger_config.logger_level,
        rotation=logger_config.logger_rotation,
        compression=logger_config.logger_compression
    )


def platform_define():
    return {
        'os': platform.system(),
        'threads': os.cpu_count(),
        'path': os.getcwd()
    }


if __name__ == '__main__':
    platform_args = platform_define()
    configure_logger(logger_config=load_logger_config(path=platform_args['path']))
    database_filename = database_filename(path=platform_args['path'])
    if os.path.exists(database_filename):
        loader.run(
            database_filename=database_filename,
            platform_args=platform_args)
    else:
        logger.error(f'Не найден файл базы данных: {database_filename}')
