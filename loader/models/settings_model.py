import sqlite3


class SettingsModel:
    def __init__(self, database_filename: str) -> None:
        self._database_filename = database_filename
        self._select_query = "SELECT name_property, property_value FROM settings WHERE name_property like '{value}_%';"
        self._update_query = "UPDATE settings SET property_value='{value}' WHERE name_property='{condition}';"

    def get_grubber_properties(self) -> dict:
        return self._query_database('grubber')

    def get_ffmpeg_properties(self) -> dict:
        return self._query_database('ffmpeg')

    def get_main_window_properties(self):
        return self._query_database('main_window')

    def update_min_progressive_resolution(self, value):
        self._update_database(value=value, condition='grubber_min_progressive_resolution')

    def update_min_dash_video_resolution(self, value):
        self._update_database(value=value, condition='grubber_min_dash_video_resolution')

    def update_min_dash_audio_bitrate(self, value):
        self._update_database(value=value, condition='grubber_min_dash_audio_bitrate')

    def update_ffmpeg_thread(self, value):
        self._update_database(value=value, condition='ffmpeg_thread')

    def _query_database(self, keyword: str) -> dict:
        properties = dict()
        with sqlite3.connect(self._database_filename) as database:
            cursor = database.cursor()
            for row in cursor.execute(self._select_query.format(value=keyword)).fetchall():
                properties.update({row[0]: row[1]})
            cursor.close()
        return properties

    def _update_database(self, value: str, condition: str) -> None:
        with sqlite3.connect(self._database_filename) as database:
            cursor = database.cursor()
            cursor.execute(self._update_query.format(value=value, condition=condition))
            cursor.close()
            database.commit()
