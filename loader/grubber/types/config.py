import enum
from dataclasses import dataclass
from typing import List


class TypePlatform(enum.Enum):
    Windows = 'Windows'
    Linux = 'Linux'


@dataclass
class GrubberConfig:
    app_directory: str
    temporary_directory: str
    validation_urls: List[str]
    min_progressive_resolution: str
    min_dash_video_resolution: str
    min_dash_audio_bitrate: str
    resolution_values: List[str]
    bitrate_values: List[str]


@dataclass
class FfmpegConfig:
    ffmpeg_path: str
    threads: str
    threads_values: list
