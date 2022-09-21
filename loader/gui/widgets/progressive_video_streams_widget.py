from typing import Optional, List

from loader.grubber.types import VideoInfo, ProgressiveTrack
from loader.gui.ui import Ui_ProgressiveVideoStreamsWidget
from loader.gui.widgets.content_widget import ContentWidget


class ProgressiveVideoStreamsWidget(ContentWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_ProgressiveVideoStreamsWidget()
        self.ui.setupUi(self)

        self._progressive_tracks: Optional[List[ProgressiveTrack]] = None
        self._availability_download: Optional[bool] = False

    def setValues(self, video: VideoInfo) -> None:
        self._progressive_tracks = video.progressive_tracks
        if len(self._progressive_tracks) > 0:
            self.ui.tracks.addItems(video.get_progressive_video_streams_info())
            self.ui.tracks.currentTextChanged.connect(self._eventHandlerItemChange)
            self._selectedItemChange()
            self._availability_download = True

    def _selectedItemChange(self) -> None:
        stream = self._progressive_tracks[self.ui.tracks.currentIndex()]
        self.ui.resolutionLabel.setText(stream.resolution)
        self.ui.videoCodecLabel.setText(stream.video_codec)
        self.ui.fpsLabel.setText(stream.fps)
        self.ui.audioBitrateLabel.setText(stream.audio_bitrate)
        self.ui.audioCodecLabel.setText(stream.audio_codec)
        self.ui.mimeTypeLabel.setText(stream.mime_type)

    def _eventHandlerItemChange(self) -> None:
        self._selectedItemChange()

    def checkAvailability(self) -> bool:
        return self._availability_download

    def getSelectedStream(self) -> Optional[ProgressiveTrack]:
        return self._progressive_tracks[self.ui.tracks.currentIndex()]
