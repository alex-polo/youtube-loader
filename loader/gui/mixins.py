import os
from typing import Optional

from PyQt6.QtCore import QThreadPool, QProcess
from PyQt6.QtWidgets import QFileDialog, QMainWindow
from loguru import logger

from loader.grubber import clean_temp_directory
from loader.gui.process_window import OutProcessWindow
from loader.gui.settings_window import SettingsWindow
from loader.misc import Settings
from loader.gui.exceptions import grubber_error_handler_exception

from loader.gui.events import (
    FindProcess,
    DownloadProcess,
)
from loader.grubber.types import (
    GrubberConfig,
    GrubberSuccessLoad,
    FfmpegConfig,
    StreamType,
    DownloadContent,
)
from loader.ffmpeg import (
    ffmpeg_convert_audio_command,
    ffmpeg_concat_video_and_audio_command,
)


class MainWindowMixin:

    def __init__(self) -> None:
        self._threadpool: Optional[QThreadPool] = QThreadPool()
        self._qprocess: Optional[QProcess] = None
        self._ffmpeg_config: Optional[FfmpegConfig] = None
        self._process_window: Optional[OutProcessWindow] = None
        self._settings_window: Optional[SettingsWindow] = None

    def find_video_details(self, url: str, grubber_config: GrubberConfig, success_event, error_event) -> None:
        logger.debug(f'start find video, url: {str}, grubber_config: {grubber_config}')
        find_process = FindProcess(url=url, grubber_config=grubber_config)
        find_process.signals.result.connect(success_event)
        find_process.signals.error.connect(error_event)
        logger.debug('start find process in threadpool')
        self._threadpool.start(find_process)

    def download_video(self, download_content: DownloadContent, ffmpeg_config: FfmpegConfig = None) -> None:
        logger.debug(f'start download video, download_content: {download_content}, ffmpeg_config: {ffmpeg_config}')
        self._ffmpeg_config = ffmpeg_config
        self._process_window = OutProcessWindow()
        self._process_window.show()

        download_process = DownloadProcess(download_content)
        self._event_print_process_window(message='Получение данных от YouTube.')
        download_process.signals.result.connect(self._event_success_download_video)
        download_process.signals.error.connect(self._event_error_download_video)
        logger.debug('start download process in threadpool')
        self._threadpool.start(download_process)

    def _event_print_process_window(self, message: str) -> None:
        logger.debug(message)
        self._process_window.print(message=message)

    def _event_process_window_finish_status(self) -> None:
        self._event_print_process_window(message='Завершено.')
        self._process_window.finishStatus()

    def _event_success_download_video(self, grubber_success_load: GrubberSuccessLoad) -> None:
        logger.debug(f'method download_video is success, grubber_success_load: {grubber_success_load}')
        if grubber_success_load.stream_type == StreamType.Progressive:
            logger.debug(f'downloaded video is progressive, file {grubber_success_load.downloaded_filename_audio}.')
            self._event_print_process_window(message=f'Файл скачан:\n{grubber_success_load.downloaded_filename_video}.')
            self._finish_download()
        elif grubber_success_load.stream_type == StreamType.DashAudio:
            logger.debug(f'downloaded dash audio, file {grubber_success_load.downloaded_filename_audio}.')
            self._event_print_process_window(
                message=f'Скачан аудиопоток: {grubber_success_load.downloaded_filename_audio}\nПереконвертирование:\n')
            self._ffmpeg_convert_audio_ffmpeg(grubber_success_load=grubber_success_load)
        elif grubber_success_load.stream_type == StreamType.DasVideo:
            logger.debug(f'downloaded dash audio and video, files:\n'
                         f'video: {grubber_success_load.downloaded_filename_video},'
                         f'audio: {grubber_success_load.downloaded_filename_audio}.')
            self._event_print_process_window(
                message=f'Скачаны временные файлы:\n'
                        f'Видеопоток: {grubber_success_load.downloaded_filename_video}.\n'
                        f'Аудиопоток: {grubber_success_load.downloaded_filename_audio}.\n'
                        f'\nОбъединение аудио и видео потоков.:\n')
            self._ffmpeg_concat_video_and_audio(grubber_success_load=grubber_success_load)

    def _event_error_download_video(self, grubber_error) -> None:
        logger.debug(f'download video is error status, error: {grubber_error}')
        grubber_error_handler_exception(grubber_error=grubber_error)
        self._event_print_process_window(message=grubber_error.text)
        self._event_process_window_finish_status()

    def _finish_download(self) -> None:
        logger.debug('download video process is finished')
        self._qprocess = None
        self._ffmpeg_config = None
        self._event_process_window_finish_status()

    def _ffmpeg_convert_audio_ffmpeg(self, grubber_success_load: GrubberSuccessLoad) -> None:
        logger.debug('start convert audio stream to mp3.')
        ffmpeg_command = ffmpeg_convert_audio_command(
            threads=self._ffmpeg_config.threads,
            src_audio=grubber_success_load.downloaded_filename_audio,
            bitrate=grubber_success_load.bitrate,
            out_filename=grubber_success_load.user_filename_for_download)
        logger.debug(f'ffmpeg convert command {ffmpeg_command}.')

        self._ffmpeg_start(ffmpeg_command=ffmpeg_command)

    def _ffmpeg_concat_video_and_audio(self, grubber_success_load: GrubberSuccessLoad) -> None:
        logger.debug('start concat audio and video streams.')
        ffmpeg_command = ffmpeg_concat_video_and_audio_command(
            threads=self._ffmpeg_config.threads,
            src_audio=grubber_success_load.downloaded_filename_audio,
            src_video=grubber_success_load.downloaded_filename_video,
            out_filename=grubber_success_load.user_filename_for_download)
        logger.debug(f'ffmpeg concat command {ffmpeg_command}.')

        self._ffmpeg_start(ffmpeg_command=ffmpeg_command)

    def _ffmpeg_start(self, ffmpeg_command: list) -> None:
        if self._qprocess is None:
            self._qprocess = QProcess()
            self._qprocess.readyReadStandardOutput.connect(self._ffmpeg_handle_stdout)
            self._qprocess.readyReadStandardError.connect(self._ffmpeg_handle_stderr)
            self._qprocess.finished.connect(self._ffmpeg_process_finished)
            logger.debug('start ffmpeg process')
            self._qprocess.start(self._ffmpeg_config.ffmpeg_path, ffmpeg_command)

    def _ffmpeg_handle_stderr(self) -> None:
        data = self._qprocess.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self._event_print_process_window(stderr)

    def _ffmpeg_handle_stdout(self) -> None:
        data = self._qprocess.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self._event_print_process_window(stdout)

    def _ffmpeg_process_finished(self) -> None:
        self._finish_download()

    def open_settings(self, settings: Settings) -> None:
        self._settings_window = SettingsWindow()
        self._settings_window.setValues(settings=settings)
        self._settings_window.show()

    @classmethod
    def clear_temp_folder(cls, temp_directory: str) -> None:
        clean_temp_directory(temp_directory=temp_directory)

    @classmethod
    def save_file_dialog(cls, window: QMainWindow, app_directory: str, default_filename: str, type_filename: str):
        user_filename, _ = QFileDialog.getSaveFileName(window,
                                                       caption='Save stream',
                                                       directory=os.path.join(app_directory, default_filename),
                                                       filter=f'*.{type_filename}')
        return user_filename
