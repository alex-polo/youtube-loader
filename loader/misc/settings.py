import os

from loader.grubber.types import GrubberConfig, FfmpegConfig, TypePlatform
from loader.models import SettingsModel


class Settings:

    def __init__(self, database_filename: str, platform_args: dict) -> None:
        self._settings_model = SettingsModel(database_filename=database_filename)
        self._threads = platform_args['threads']
        self._os = platform_args['os']
        self._app_path = platform_args['path']

    def grubber_config(self) -> GrubberConfig:
        properties = self._settings_model.get_grubber_properties()
        return GrubberConfig(
            app_directory=self._app_path,
            temporary_directory=properties['grubber_temporary_directory'],
            validation_urls=properties['grubber_validation_urls'].split(','),
            min_progressive_resolution=properties['grubber_min_progressive_resolution'],
            min_dash_video_resolution=properties['grubber_min_dash_video_resolution'],
            min_dash_audio_bitrate=properties['grubber_min_dash_audio_bitrate'],
            resolution_values=properties['grubber_resolution_values'].split(','),
            bitrate_values=properties['grubber_bitrate_values'].split(',')
        )

    def ffmpeg_config(self) -> FfmpegConfig:
        properties = self._settings_model.get_ffmpeg_properties()
        return FfmpegConfig(
            ffmpeg_path=self._get_ffmpeg_path(
                win_ffmpeg_path=properties['ffmpeg_win64_ffmpeg_path'],
                linux_ffmpeg_path=properties['ffmpeg_linux64_ffmpeg_path']),
            threads=self._get_ffmpeg_threads(database_value=properties['ffmpeg_thread']),
            threads_values=properties['ffmpeg_thread_values'].split(',')
        )

    def _get_ffmpeg_threads(self, database_value: str) -> str:
        return str(self._threads) if int(database_value) > self._threads else database_value

    def _get_ffmpeg_path(self, win_ffmpeg_path: str, linux_ffmpeg_path: str) -> str:
        if self._os == TypePlatform.Windows.value:
            return os.path.join(self._app_path, win_ffmpeg_path)
        elif self._os == TypePlatform.Linux.value:
            return os.path.join(self._app_path, linux_ffmpeg_path)
        else:
            raise Exception('Не удалось определить операционную систему')

    def update_min_progressive_resolution(self, value):
        self._settings_model.update_min_progressive_resolution(value=value)

    def update_min_dash_video_resolution(self, value):
        self._settings_model.update_min_dash_video_resolution(value=value)

    def update_min_dash_audio_bitrate(self, value):
        self._settings_model.update_min_dash_audio_bitrate(value=value)

    def update_ffmpeg_thread(self, value):
        self._settings_model.update_ffmpeg_thread(value=value)
