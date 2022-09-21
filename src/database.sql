DROP TABLE settings;

CREATE TABLE settings(
    id INTEGER PRIMARY KEY,
    name_property VARCHAR(255) NOT NULL UNIQUE,
    property_value VARCHAR(255) NOT NULL
);


INSERT INTO settings (
                         name_property,
                         property_value
                     )
                     VALUES 
                     --grubber
                     ('grubber_temporary_directory','temp'),
                     ('grubber_validation_urls', 'https://www.youtube.com/watch?v=,https://youtu.be/'),
                     ('grubber_min_progressive_resolution','144p'),
                     ('grubber_min_dash_video_resolution','144p'),
                     ('grubber_min_dash_audio_bitrate','20kbps'),
                     ('grubber_resolution_values','144p,240p,360p,480p,720p,1080p'),
                     ('grubber_bitrate_values','20kbps,40kbps,50kbps,80kbps,100kbps'),
                     --ffmpeg
                     ('ffmpeg_win64_ffmpeg_path','src//ffmpeg//win64//ffmpeg.exe'),
                     ('ffmpeg_linux64_ffmpeg_path','src//ffmpeg//linux64//ffmpeg'),
                     ('ffmpeg_thread','4'),
                     ('ffmpeg_thread_values','1,2,4,6,8,10,12,14,16');