import traceback
from http.client import IncompleteRead

from pytube.exceptions import (
    AgeRestrictedError,
    ExtractError,
    HTMLParseError,
    LiveStreamError,
    MaxRetriesExceeded,
    MembersOnly,
    PytubeError,
    RecordingUnavailable,
    RegexMatchError,
    VideoPrivate,
    VideoRegionBlocked,
    VideoUnavailable,
)

from loader.grubber.exceptions import URLValidationException, TempDirectoryException, URLisEmptyException
from loader.grubber.types import GrubberResponse, GrubberErrorType, GrubberResponseStatus, GrubberError


def handler_response(grubber_error_type: GrubberErrorType, title: str, text: str):
    return GrubberResponse(
        status=GrubberResponseStatus.Error,
        content=GrubberError(
            grubber_error_type=grubber_error_type,
            title=title,
            text=text,
            details=traceback.format_exc()
        )
    )


def handler_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AgeRestrictedError:
            return handler_response(
                grubber_error_type=GrubberErrorType.Warning,
                title='Предупреждение',
                text='Видео ограничено по возрасту и недоступно без авторизации.')
        except RegexMatchError:
            return handler_response(
                grubber_error_type=GrubberErrorType.Error,
                title='Ошибка',
                text='Шаблон регулярного выражения не вернул совпадений.')
        except ExtractError:
            return handler_response(
                grubber_error_type=GrubberErrorType.Error,
                title='Ошибка',
                text='Произошло исключение на основе извлечения данных.')
        except HTMLParseError:
            return handler_response(
                grubber_error_type=GrubberErrorType.Error,
                title='Ошибка',
                text='HTML не может быть проанализирован.')
        except LiveStreamError:
            return handler_response(
                grubber_error_type=GrubberErrorType.Error,
                title='Ошибка',
                text='Видео — прямой эфир. Скачивание не возможно.')
        except MaxRetriesExceeded:
            return handler_response(
                grubber_error_type=GrubberErrorType.Warning,
                title='Предупреждение',
                text='Превышено максимальное количество попыток.')
        except MembersOnly:
            return handler_response(
                grubber_error_type=GrubberErrorType.Warning,
                title='Предупреждение',
                text='Видео доступно только для подписчиков.')
        except RecordingUnavailable:
            return handler_response(
                grubber_error_type=GrubberErrorType.Error,
                title='Ошибка',
                text='Запись недоступна.')
        except VideoPrivate:
            return handler_response(
                grubber_error_type=GrubberErrorType.Error,
                title='Ошибка',
                text='Закрытое видео. Скачивание недоступно.')
        except VideoRegionBlocked:
            return handler_response(
                grubber_error_type=GrubberErrorType.Warning,
                title='Внимание',
                text='Видео недоступно для вашего региона.')
        except VideoUnavailable:
            return handler_response(
                grubber_error_type=GrubberErrorType.Error,
                title='Ошибка',
                text='Видео недоступно.')
        except PytubeError:
            return handler_response(
                grubber_error_type=GrubberErrorType.Error,
                title='Ошибка',
                text='Произошла непредвиденная ошибка.')

        except URLisEmptyException as error:
            return handler_response(
                grubber_error_type=GrubberErrorType.Info,
                title='Предупреждение',
                text=str(error))
        except URLValidationException as error:
            return handler_response(
                grubber_error_type=GrubberErrorType.Info,
                title='Предупреждение',
                text=str(error))
        except TempDirectoryException as error:
            return handler_response(
                grubber_error_type=GrubberErrorType.Error,
                title='Ошибка',
                text=str(error))
        except IncompleteRead:
            return handler_response(
                grubber_error_type=GrubberErrorType.Error,
                title='Ошибка',
                text='Не удалось получить данные с YouTube, попробуйте позднее.')
        except Exception:
            return handler_response(
                grubber_error_type=GrubberErrorType.Error,
                title='Произошла ошибка',
                text='Произошла непредвиденная ошибка.')

    return wrapper
