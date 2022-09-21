import enum
from dataclasses import dataclass
from typing import Union, List, Optional


class GrubberResponseStatus(enum.Enum):
    Ok = 'Ok'
    Error = 'Error'


class GrubberErrorType(enum.Enum):
    Info = 'Info'
    Warning = 'Warning'
    Error = 'Error'


class StreamType(enum.Enum):
    Progressive = 'progressive'
    DashAudio = 'dash_audio'
    DasVideo = 'dash_video'


@dataclass
class YtBaseStream:
    itag: int
    default_filename: str
    filesize: str
    mime_type: str
    subtype: str
    type: str


@dataclass
class DashVideoTrack(YtBaseStream):
    resolution: str
    fps: str
    video_bitrate: str
    video_codec: str


@dataclass
class DashAudioTrack(YtBaseStream):
    audio_bitrate: str
    audio_codec: str


@dataclass
class ProgressiveTrack(YtBaseStream):
    resolution: str
    fps: str
    audio_bitrate: str
    video_bitrate: str
    video_codec: str
    audio_codec: str


@dataclass
class VideoInfo:
    url: str
    working_directory: str
    author: str
    title: str
    length: str
    thumbnail_path: str
    progressive_tracks: List[ProgressiveTrack]
    dash_video_tracks: List[DashVideoTrack]
    dash_audio_tracks: List[DashAudioTrack]

    def get_dash_video_streams_info(self) -> List[str]:
        return [f'VIDEO#{index}. Разрешение видео: {stream.resolution}, fps: {stream.fps}, '
                f'видео кодек: {stream.video_codec}, mime type: {stream.mime_type}'
                for index, stream in enumerate(self.dash_video_tracks)]

    def get_progressive_video_streams_info(self) -> List[str]:
        return [f'VIDEO#{index}. Разрешение видео: {stream.resolution}, fps: {stream.fps}, '
                f'видео кодек: {stream.video_codec}, mime type: {stream.mime_type}'
                for index, stream in enumerate(self.progressive_tracks)]

    def get_dash_audio_streams_info(self) -> List[str]:
        return [f'AUDIO#{index}. Битрейт: {stream.audio_bitrate}, '
                f'аудио кодек: {stream.audio_codec}, mime type: {stream.mime_type}'
                for index, stream in enumerate(self.dash_audio_tracks)]


@dataclass
class GrubberError:
    grubber_error_type: GrubberErrorType
    title: str
    text: str
    details: str


@dataclass
class DownloadContent:
    stream_type: StreamType
    url: str
    download_filename: str
    working_directory: str
    video_track: Union[DashVideoTrack, ProgressiveTrack, None]
    audio_track: Optional[DashAudioTrack]


@dataclass
class GrubberSuccessLoad:
    stream_type: StreamType
    downloaded_filename_video: Optional[str]
    downloaded_filename_audio: Optional[str]
    bitrate: Optional[str]
    user_filename_for_download: Optional[str]


@dataclass
class GrubberResponse:
    status: GrubberResponseStatus
    content: Union[VideoInfo, GrubberError, GrubberSuccessLoad]
