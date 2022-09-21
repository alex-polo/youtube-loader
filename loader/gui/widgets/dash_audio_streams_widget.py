from typing import List, Optional

from loader.grubber.types import VideoInfo, DashAudioTrack
from loader.gui.ui import Ui_DashAudioStreamsWidget
from loader.gui.widgets.content_widget import ContentWidget


class DashAudioStreamsWidget(ContentWidget):

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_DashAudioStreamsWidget()
        self.ui.setupUi(self)

        self._dash_audio_tracks: Optional[List[DashAudioTrack]] = None
        self._availability_download: Optional[bool] = False

    def setValues(self, video: VideoInfo) -> None:
        self._dash_audio_tracks = video.dash_audio_tracks
        if len(self._dash_audio_tracks) > 0:
            self.ui.tracks.addItems(video.get_dash_audio_streams_info())
            self.ui.tracks.currentTextChanged.connect(self._eventHandlerItemChange)
            self._selectedItemChange()
            self._availability_download = True

    def _selectedItemChange(self) -> None:
        stream = self._dash_audio_tracks[self.ui.tracks.currentIndex()]
        self.ui.mimeTypeLabel.setText(stream.mime_type)
        self.ui.audioBitrateLabel.setText(stream.audio_bitrate)
        self.ui.audioCodecLabel.setText(stream.audio_codec)

    def _eventHandlerItemChange(self) -> None:
        self._selectedItemChange()

    def checkAvailability(self) -> bool:
        return self._availability_download

    def getSelectedStream(self) -> Optional[DashAudioTrack]:
        return self._dash_audio_tracks[self.ui.tracks.currentIndex()]
