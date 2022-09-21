def _select_mp3_quality(bitrate: str):
    bitrate = int(bitrate[:-4])
    if bitrate > 250:
        return '0'
    elif 170 < bitrate < 250:
        return '1'
    elif 150 < bitrate < 170:
        return '2'
    elif 140 < bitrate < 150:
        return '3'
    elif 120 < bitrate < 140:
        return '4'
    elif 100 < bitrate < 120:
        return '5'
    else:
        return '6'


def ffmpeg_concat_video_and_audio_command(threads: str, src_audio: str, src_video: str, out_filename: str) -> list:
    return ['-y', '-threads', threads, '-i', src_audio, '-i', src_video, out_filename]


def ffmpeg_convert_audio_command(threads: str, src_audio: str, bitrate: str, out_filename: str) -> list:
    return ['-y', '-threads', threads, '-i', src_audio, '-codec:a', 'libmp3lame', '-qscale:a',
            _select_mp3_quality(bitrate=bitrate), out_filename]
