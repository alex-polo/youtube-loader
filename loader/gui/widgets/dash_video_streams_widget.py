from typing import List, Optional

from loader.grubber.types import DashVideoTrack, VideoInfo
from loader.gui.ui import Ui_DashVideoStreamsWidget
from loader.gui.widgets.content_widget import ContentWidget


class DashVideoStreamsWidget(ContentWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_DashVideoStreamsWidget()
        self.ui.setupUi(self)

        self._dash_video_tracks: Optional[List[DashVideoTrack]] = None
        self._availability_download: Optional[bool] = False

    def setValues(self, video: VideoInfo) -> None:
        self._dash_video_tracks = video.dash_video_tracks
        if len(self._dash_video_tracks) > 0:
            self.ui.tracks.addItems(video.get_dash_video_streams_info())
            self.ui.tracks.currentTextChanged.connect(self._eventHandlerItemChange)
            self._selectedItemChange()
            self._availability_download = True

    def _selectedItemChange(self) -> None:
        stream = self._dash_video_tracks[self.ui.tracks.currentIndex()]
        self.ui.videoResolutionLabel.setText(stream.resolution)
        self.ui.videoFpsLabel.setText(stream.fps)
        self.ui.videoCodecLabel.setText(stream.video_codec)
        self.ui.mimeTypeLabel.setText(stream.mime_type)

    def _eventHandlerItemChange(self) -> None:
        self._selectedItemChange()

    def checkAvailability(self) -> bool:
        return self._availability_download

    def getSelectedStream(self) -> Optional[DashVideoTrack]:
        return self._dash_video_tracks[self.ui.tracks.currentIndex()]
