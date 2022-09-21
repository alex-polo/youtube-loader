import sys
import traceback

from PyQt6.QtWidgets import QApplication
from loguru import logger

from loader.gui import MainWindow
from loader.misc import Settings


def run(database_filename: str, platform_args: dict) -> None:
    try:
        settings = Settings(
            database_filename=database_filename,
            platform_args=platform_args)

        logger.debug('starting application.')
        app = QApplication(sys.argv)
        window = MainWindow(settings=settings)
        window.show()
        sys.exit(app.exec())
    except Exception as error:
        logger.error(error)
        logger.error(traceback.format_exc(limit=None, chain=True))
