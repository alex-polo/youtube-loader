import os
import ffmpeg
from pytube import YouTube

bad_symbols = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}


def quest_user(func):
    def wrapper(quest):
        while True:
            user_answer = input(quest)
            success, result = func(user_answer)
            if success:
                return result
    return wrapper


@quest_user
def _define_download_directory(user_answer: str) -> tuple:
    if len(user_answer) > 0:
        if os.path.exists(user_answer):
            return True, user_answer
        else:
            print(f'Directory "{user_answer}" does not exist')
            return False, None
    else:
        path = os.path.join(os.getcwd(), 'downloaded')
        if os.path.exists(path):
            return True, path
        else:
            print(f'Error. Directory "{path}" not fount')
            return False, None


@quest_user
def _define_resolution_video(user_answer: str) -> tuple:
    if len(user_answer) > 0:
        if user_answer == '240p' or user_answer == '360p' \
                or user_answer == '480p' or user_answer == '720p' \
                or user_answer == '1080p' or user_answer == '1440p' or user_answer == '2160p':
            return True, user_answer
        else:
            print('Incorrect resolution\n'
                  'Please enter 2160p/1440p/1080p/720p/480p/360p/240p')
            return False, None

    else:
        return True, '1080p'


@quest_user
def _define_progressive_value(user_answer: str) -> tuple:
    if len(user_answer) == 0 or user_answer.lower() == 'yes' or user_answer.lower() == 'y':
        return True, True
    elif user_answer.lower() == 'no' or user_answer.lower() == 'n':
        return True, False
    else:
        return False, None


@quest_user
def _define_youtube_url(user_answer: str) -> tuple:
    if 'https://www.youtube.com/watch?v=' in user_answer[:32]:
        return True, user_answer
    else:
        print('Incorrect url')
        return False, None


def _search_dash_stream_content(yt: YouTube, resolution: str) -> tuple:
    print('Search for audio and video tracks')
    video = yt.streams.filter(adaptive=True,
                              only_video=True, file_extension='webm', resolution=resolution).desc().last()
    audio = yt.streams.filter(adaptive=True, only_audio=True, file_extension='webm').desc().first()
    if video is not None:
        video_title = ''.join(symbol for symbol in yt.title if symbol not in bad_symbols)
        print(f'Find:\n'
              f'\tVideo title: {video_title}\n'
              f'\tVideo - resolution: {video.resolution}, fps: {video.fps}, video codec: "{video.video_codec}", '
              f'format file video: {video.mime_type}\n'
              f'\tAudio - bitrate: {audio.abr}, audio codec: {audio.audio_codec}, format file audio: {audio.mime_type}')
    else:
        video_title = None

    return video, audio, video_title


def _search_progressive_stream_content(yt: YouTube, resolution: str) -> tuple:
    print('Search video tracks')
    video = yt.streams.filter(progressive=True, resolution=resolution).desc().first()
    if video is not None:
        video_title = ''.join(symbol for symbol in yt.title if symbol not in bad_symbols)
        print(f'Find:\n'
              f'\tVideo title: {video_title}\n'
              f'\tVideo - resolution: {video.resolution}, fps: {video.fps}, video codec: "{video.video_codec}", '
              f'format file video: {video.mime_type}\n')
    else:
        video_title = None
    return video, video_title


def _merge_video_and_audio_tracks(path_video: str, path_audio: str, video_title: str,
                                  output_directory: str, path_ffmpeg: str) -> None:
    video_ffmpeg = ffmpeg.input(path_video)
    audio_ffmpeg = ffmpeg.input(path_audio)
    ffmpeg.concat(video_ffmpeg, audio_ffmpeg, v=1, a=1). \
        output(os.path.join(output_directory, f'{video_title}.webm')). \
        run(overwrite_output=True, cmd=path_ffmpeg)


def _load(url: str, progressive: bool, resolution_video: str, output_directory: str, path_ffmpeg: str) -> None:
    try:
        print(f'Getting info video, url: {url}')
        yt = YouTube(url)
        if progressive:
            video, video_title = _search_progressive_stream_content(yt=yt, resolution=resolution_video)
            if video is not None:
                print('Start download video')
                video.download(output_directory, f'{video_title}.mp4')
            else:
                print('Not found streams.')
        else:
            video, audio, video_title = _search_dash_stream_content(yt=yt, resolution=resolution_video)
            if video is not None and audio is not None:
                print('Start download audio and video tracks')

                video.download(output_directory, f'video_{video_title}.webm')
                audio.download(output_directory, f'audio_{video_title}.webm')
                print('Download is success')

                print('Merge video and audio tracks')
                path_video = os.path.join(output_directory, f'video_{video_title}.webm')
                path_audio = os.path.join(output_directory, f'audio_{video_title}.webm')
                _merge_video_and_audio_tracks(
                    path_video=path_video, path_audio=path_audio, video_title=video_title,
                    output_directory=output_directory, path_ffmpeg=path_ffmpeg)
                print('Remove temp files')
                os.remove(path_video)
                os.remove(path_audio)
            else:
                print('Not found streams.')
        print('DONE!')
    except Exception as error:
        print(error)


def _main() -> None:
    url = _define_youtube_url('Enter YouTube URL: ')
    progressive = _define_progressive_value('Use progressive streams? (default yes) (y/n): ')
    if progressive:
        resolution_video = '720p'
    else:
        resolution_video = _define_resolution_video('Enter resolution video (default: 1080p): ')

    output_directory = _define_download_directory('Enter download directory (default: downloaded): ')
    path_ffmpeg = os.path.join(os.getcwd(), 'ffmpeg-4.4\\bin\\ffmpeg.exe')

    if os.path.exists(path_ffmpeg):
        _load(url=url,
              progressive=progressive,
              resolution_video=resolution_video,
              output_directory=output_directory,
              path_ffmpeg=path_ffmpeg)
    else:
        print('Error. ffmpeg.exe not fount')


if __name__ == '__main__':
    _main()
