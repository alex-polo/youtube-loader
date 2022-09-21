import traceback

from loguru import logger

from loader.grubber.types import GrubberError, GrubberErrorType
from loader.gui.exceptions.message import error_message, grubber_error_message


def gui_handler_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            logger.error(error)
            logger.error(traceback.format_exc(limit=None, chain=True))
            error_message()

    return wrapper


def gui_qt_slot_handler_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args[:-1], **kwargs)
        except Exception as error:
            logger.error(error)
            logger.error(traceback.format_exc(limit=None, chain=True))
            error_message()

    return wrapper


def grubber_error_handler_exception(grubber_error: GrubberError) -> None:
    if grubber_error.grubber_error_type == GrubberErrorType.Error:
        logger.error(grubber_error.text)
        logger.error(grubber_error.details)
    elif grubber_error.grubber_error_type == GrubberErrorType.Warning:
        logger.warning(grubber_error.text)
        logger.warning(grubber_error.details)
    elif grubber_error.grubber_error_type == GrubberErrorType.Info:
        logger.info(grubber_error.text)
        logger.info(grubber_error.details)
