class URLValidationException(Exception):

    def __init__(self, url: str) -> None:
        self._message = f'Введен некорректный URL: {url}.\nПодобные адреса не поддерживаются.'
        super().__init__(self._message)


class URLisEmptyException(Exception):
    def __init__(self) -> None:
        self._message = f'URL не может быть пустым. Введите ссылку на видео.'
        super().__init__(self._message)


class TempDirectoryException(Exception):

    def __init__(self, path: str) -> None:
        self._message = f'Не удалось создать директорию: {path}.'
        super().__init__(self._message)
