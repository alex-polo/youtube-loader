import pytube as pytube

from loader.grubber.exceptions import handler_exception
from loader.grubber.tools import (
    validation_url,
    creating_working_directory,
    download_thumbnail,
    sort_progressive_streams,
    sort_dash_video_streams,
    sort_dash_audio_streams,
    clean_temp,
    download_progressive_video,
    download_dash_audio,
    download_dash_video_and_audio,
)
from loader.grubber.types import (
    GrubberResponse,
    GrubberConfig,
    GrubberResponseStatus,
    VideoInfo,
    DownloadContent,
    StreamType,
)


@handler_exception
def load_video_details(url: str, grubber_config: GrubberConfig) -> GrubberResponse:
    validation_url(url=url, validation_list=grubber_config.validation_urls)

    youtube = pytube.YouTube(url)
    youtube.check_availability()

    path_working_directory = creating_working_directory(
        app_path=grubber_config.app_directory,
        temporary_directory=grubber_config.temporary_directory,
        video_id=youtube.video_id)

    return GrubberResponse(
        status=GrubberResponseStatus.Ok,
        content=VideoInfo(
            url=youtube.watch_url,
            working_directory=path_working_directory,
            author=youtube.author,
            title=youtube.title,
            length=f'{youtube.length // 60}:{youtube.length % 60} мин.',
            thumbnail_path=download_thumbnail(
                thumbnail_url=youtube.thumbnail_url,
                video_id=youtube.video_id,
                working_directory_path=path_working_directory),
            progressive_tracks=sort_progressive_streams(
                yt=youtube,
                resolution=grubber_config.min_progressive_resolution),
            dash_video_tracks=sort_dash_video_streams(
                yt=youtube,
                resolution=grubber_config.min_dash_video_resolution),
            dash_audio_tracks=sort_dash_audio_streams(
                yt=youtube,
                bitrate=grubber_config.min_dash_audio_bitrate)
        )
    )


@handler_exception
def download_streams(download_content: DownloadContent) -> GrubberResponse:
    if download_content.stream_type == StreamType.Progressive:
        return download_progressive_video(download_content=download_content)
    elif download_content.stream_type == StreamType.DashAudio:
        return download_dash_audio(download_content=download_content)
    elif download_content.stream_type == StreamType.DasVideo:
        return download_dash_video_and_audio(download_content=download_content)


def clean_temp_directory(temp_directory: str) -> None:
    clean_temp(path=temp_directory)
