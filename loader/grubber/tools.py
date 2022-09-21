import os
import shutil
from typing import List, Optional

import pytube
import requests as requests
from pytube import YouTube

from loader.grubber.exceptions import URLValidationException, TempDirectoryException, URLisEmptyException
from loader.grubber.types import (
    DashAudioTrack,
    DashVideoTrack,
    ProgressiveTrack,
    GrubberResponse,
    GrubberSuccessLoad,
    GrubberResponseStatus,
    StreamType,
    DownloadContent,
)


def validation_url(url: str, validation_list: List[str]) -> None:
    if len(url) == 0:
        raise URLisEmptyException()
    if not len(list(filter(lambda v_url: url.find(v_url) == 0, validation_list))):
        raise URLValidationException(url=url)


def clean_temp(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)


def _check_temporary_directory(path: str) -> None:
    access_rights = 0o755
    try:
        if not os.path.exists(path):
            os.mkdir(path, access_rights)
    except OSError:
        raise TempDirectoryException(path)


def creating_working_directory(app_path: str, temporary_directory: str, video_id: int) -> str:
    path_temporary_directory: str = os.path.join(app_path, temporary_directory)
    _check_temporary_directory(path=path_temporary_directory)
    path_working_directory = os.path.join(path_temporary_directory, str(video_id))
    _check_temporary_directory(path=path_working_directory)

    return path_working_directory


def download_thumbnail(thumbnail_url: str, video_id: int, working_directory_path: str) -> Optional[str]:
    response = requests.get(thumbnail_url)
    if response.status_code == 200:
        with open(os.path.join(working_directory_path, f'{video_id}.png'), 'wb') as image_file:
            for chunk in response:
                image_file.write(chunk)
        return os.path.join(working_directory_path, f'{video_id}.png')
    else:
        return None


def sort_progressive_streams(yt: YouTube, resolution: str = '0p') -> List[ProgressiveTrack]:
    return [ProgressiveTrack(
        itag=progressive_stream.itag,
        default_filename=progressive_stream.default_filename,
        filesize=str(progressive_stream.filesize),
        mime_type=progressive_stream.mime_type,
        subtype=progressive_stream.subtype,
        type=progressive_stream.type,
        resolution=progressive_stream.resolution,
        fps=str(progressive_stream.fps),
        audio_bitrate=progressive_stream.abr,
        video_bitrate=str(progressive_stream.bitrate),
        video_codec=progressive_stream.video_codec,
        audio_codec=progressive_stream.audio_codec,
    ) for progressive_stream in yt.streams.filter(progressive=True).order_by('resolution')
        if int(progressive_stream.resolution[:-1]) >= int(resolution[:-1])]


def sort_dash_video_streams(yt: YouTube, resolution: str = '0p') -> List[DashVideoTrack]:
    return [DashVideoTrack(
        itag=dash_video_stream.itag,
        default_filename=dash_video_stream.default_filename,
        filesize=str(dash_video_stream.filesize),
        mime_type=dash_video_stream.mime_type,
        subtype=dash_video_stream.subtype,
        type=dash_video_stream.type,
        resolution=dash_video_stream.resolution,
        fps=str(dash_video_stream.fps),
        video_bitrate=str(dash_video_stream.bitrate),
        video_codec=dash_video_stream.video_codec,
    ) for dash_video_stream in yt.streams.filter(adaptive=True,
                                                 only_video=True,
                                                 only_audio=False).order_by('resolution')
        if int(dash_video_stream.resolution[:-1]) >= int(resolution[:-1])]


def sort_dash_audio_streams(yt: YouTube, bitrate: str = '1kbps') -> List[DashAudioTrack]:
    return [DashAudioTrack(
        itag=dash_audio_stream.itag,
        default_filename=dash_audio_stream.default_filename,
        filesize=str(dash_audio_stream.filesize),
        mime_type=dash_audio_stream.mime_type,
        subtype=dash_audio_stream.subtype,
        type=dash_audio_stream.type,
        audio_bitrate=dash_audio_stream.abr,
        audio_codec=dash_audio_stream.audio_codec,
    ) for dash_audio_stream in yt.streams.filter(adaptive=True, only_audio=True, only_video=False).order_by('abr')
        if int(dash_audio_stream.abr[:-4]) >= int(bitrate[:-4])]


def download_dash_audio(download_content: DownloadContent) -> GrubberResponse:
    youtube = pytube.YouTube(download_content.url)
    youtube.check_availability()

    temp_filename = os.path.join(download_content.working_directory,
                                 f'temp_audio.{download_content.audio_track.default_filename.split(".")[1]}')
    download_filename = youtube.streams.get_by_itag(download_content.audio_track.itag).download(filename=temp_filename)

    return GrubberResponse(
        status=GrubberResponseStatus.Ok,
        content=GrubberSuccessLoad(
            stream_type=StreamType.DashAudio,
            downloaded_filename_video=None,
            downloaded_filename_audio=download_filename,
            bitrate=download_content.audio_track.audio_bitrate,
            user_filename_for_download=download_content.download_filename
        )
    )


def download_dash_video_and_audio(download_content: DownloadContent) -> GrubberResponse:
    youtube = pytube.YouTube(download_content.url)
    youtube.check_availability()
    temp_audio_filename = os.path.join(download_content.working_directory,
                                       f'temp_audio.{download_content.audio_track.default_filename.split(".")[1]}')
    temp_video_filename = os.path.join(download_content.working_directory,
                                       f'temp_video.{download_content.video_track.default_filename.split(".")[1]}')

    downloaded_temp_audio_filename = youtube.streams.get_by_itag(download_content.audio_track.itag) \
        .download(filename=temp_audio_filename)
    downloaded_temp_video_filename = youtube.streams.get_by_itag(download_content.video_track.itag) \
        .download(filename=temp_video_filename)
    return GrubberResponse(
        status=GrubberResponseStatus.Ok,
        content=GrubberSuccessLoad(
            stream_type=StreamType.DasVideo,
            downloaded_filename_video=downloaded_temp_video_filename,
            downloaded_filename_audio=downloaded_temp_audio_filename,
            bitrate=None,
            user_filename_for_download=download_content.download_filename
        )
    )


def download_progressive_video(download_content: DownloadContent) -> GrubberResponse:
    youtube = pytube.YouTube(download_content.url)
    youtube.check_availability()
    download_filename = youtube.streams.get_by_itag(download_content.video_track.itag).download(
        filename=download_content.download_filename)
    return GrubberResponse(
        status=GrubberResponseStatus.Ok,
        content=GrubberSuccessLoad(
            stream_type=StreamType.Progressive,
            downloaded_filename_video=download_filename,
            downloaded_filename_audio=None,
            bitrate=None,
            user_filename_for_download=None
        )
    )
