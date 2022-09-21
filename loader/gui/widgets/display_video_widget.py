from typing import Optional

from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget

from loader.grubber.types import VideoInfo, StreamType, DownloadContent
from loader.gui.ui import Ui_DisplayVideoDetails
from loader.gui.widgets.dash_video_streams_widget import DashVideoStreamsWidget
from loader.gui.widgets.dash_audio_streams_widget import DashAudioStreamsWidget
from loader.gui.widgets.progressive_video_streams_widget import ProgressiveVideoStreamsWidget
from loader.gui.widgets.content_widget import ContentWidget


class DisplayVideoDetailsWidget(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_DisplayVideoDetails()
        self.ui.setupUi(self)

        self._dashVideoStreamsWidget: Optional[DashVideoStreamsWidget] = None
        self._dashAudioStreamsWidget: Optional[DashAudioStreamsWidget] = None
        self._progressiveVideoStreamsWidget: Optional[ProgressiveVideoStreamsWidget] = None

        self._videoInfo: Optional[VideoInfo] = None
        self._stream_type: Optional[StreamType] = None

    def setVideoContent(self, video: VideoInfo) -> None:
        self._videoInfo = video

        self.ui.titleLabel.setText(video.title)
        self.ui.videoLabel.setPixmap(QtGui.QPixmap(video.thumbnail_path))
        self.ui.urlLabel.setText(video.url)
        self.ui.authorLabel.setText(video.author)
        self.ui.lengthLabel.setText(video.length)

        self.ui.showAudioTracksButton.clicked.connect(self._showDashAudioTracks)
        self.ui.showDashVideoTracksButton.clicked.connect(self._showDashVideoTracks)
        self.ui.showProgressiveVideoTracksButton.clicked.connect(self._showProgressiveVideoTracks)

        self._showDashVideoTracks()

    def getDownloadContent(self) -> Optional[DownloadContent]:
        if self._stream_type == StreamType.DasVideo:
            dash_video = self._dashVideoStreamsWidget.getSelectedStream()
            dash_audio = self._dashAudioStreamsWidget.getSelectedStream()
            return DownloadContent(
                stream_type=self._stream_type,
                url=self._videoInfo.url,
                download_filename=dash_video.default_filename,
                working_directory=self._videoInfo.working_directory,
                video_track=dash_video,
                audio_track=dash_audio
            )
        elif self._stream_type == StreamType.DashAudio:
            dash_audio = self._dashAudioStreamsWidget.getSelectedStream()
            return DownloadContent(
                stream_type=self._stream_type,
                url=self._videoInfo.url,
                download_filename=f'{dash_audio.default_filename.split(".")[0]}.mp3',
                working_directory=self._videoInfo.working_directory,
                video_track=None,
                audio_track=dash_audio
            )
        elif self._stream_type == StreamType.Progressive:
            progressive_video = self._progressiveVideoStreamsWidget.getSelectedStream()
            return DownloadContent(
                stream_type=self._stream_type,
                url=self._videoInfo.url,
                download_filename=progressive_video.default_filename,
                working_directory=self._videoInfo.working_directory,
                video_track=progressive_video,
                audio_track=None
            )
        else:
            return None

    def _showProgressiveVideoTracks(self):
        self._clear()
        self._disabledProgressiveVideoButton()
        self._progressiveVideoStreamsWidget = ProgressiveVideoStreamsWidget()
        self._progressiveVideoStreamsWidget.setValues(self._videoInfo)
        self.ui.tracksLayout.addWidget(self._progressiveVideoStreamsWidget)
        self._stream_type = StreamType.Progressive
        self._checkDownloadButtonAvailability(self._progressiveVideoStreamsWidget)

    def _showDashAudioTracks(self):
        self._clear()
        self._disabledDashAudioButton()
        self._dashAudioStreamsWidget = DashAudioStreamsWidget()
        self._dashAudioStreamsWidget.setValues(self._videoInfo)
        self.ui.tracksLayout.addWidget(self._dashAudioStreamsWidget)
        self._stream_type = StreamType.DashAudio
        self._checkDownloadButtonAvailability(self._dashAudioStreamsWidget)

    def _showDashVideoTracks(self):
        self._clear()
        self._disabledDashVideoButton()
        self._dashVideoStreamsWidget = DashVideoStreamsWidget()
        self._dashAudioStreamsWidget = DashAudioStreamsWidget()
        self._dashVideoStreamsWidget.setValues(self._videoInfo)
        self._dashAudioStreamsWidget.setValues(self._videoInfo)

        self.ui.tracksLayout.addWidget(self._dashVideoStreamsWidget)
        self.ui.tracksLayout.addWidget(self._dashAudioStreamsWidget)
        self._stream_type = StreamType.DasVideo

        if self._dashVideoStreamsWidget.checkAvailability() and self._dashAudioStreamsWidget.checkAvailability():
            self.ui.downloadButton.setEnabled(True)
        else:
            self.ui.downloadButton.setEnabled(False)

    def _disabledDashVideoButton(self):
        self.ui.showAudioTracksButton.setEnabled(True)
        self.ui.showDashVideoTracksButton.setEnabled(False)
        self.ui.showProgressiveVideoTracksButton.setEnabled(True)

    def _disabledDashAudioButton(self):
        self.ui.showAudioTracksButton.setEnabled(False)
        self.ui.showDashVideoTracksButton.setEnabled(True)
        self.ui.showProgressiveVideoTracksButton.setEnabled(True)

    def _disabledProgressiveVideoButton(self):
        self.ui.showAudioTracksButton.setEnabled(True)
        self.ui.showDashVideoTracksButton.setEnabled(True)
        self.ui.showProgressiveVideoTracksButton.setEnabled(False)

    def _clear(self):
        for i in reversed(range(self.ui.tracksLayout.count())):
            self.ui.tracksLayout.itemAt(i).widget().setParent(None)

    def _checkDownloadButtonAvailability(self, widget: ContentWidget):
        if widget.checkAvailability():
            self.ui.downloadButton.setEnabled(True)
        else:
            self.ui.downloadButton.setEnabled(False)

