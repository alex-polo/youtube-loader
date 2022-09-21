from PyQt6.QtCore import QRunnable, pyqtSlot

from loader import grubber
from loader.grubber.types import GrubberConfig, GrubberResponseStatus, DownloadContent
from loader.gui.events import FindProcessSignals, DownloadProcessSignals


class FindProcess(QRunnable):

    def __init__(self, url: str, grubber_config: GrubberConfig) -> None:
        super().__init__()
        self._url = url
        self._grubber_config = grubber_config
        self.signals = FindProcessSignals()

    @pyqtSlot()
    def run(self):
        grubber_response = grubber.load_video_details(url=self._url, grubber_config=self._grubber_config)
        if grubber_response.status == GrubberResponseStatus.Ok:
            self.signals.result.emit(grubber_response.content)
        else:
            self.signals.error.emit(grubber_response.content)


class DownloadProcess(QRunnable):

    def __init__(self, download_content: DownloadContent) -> None:
        super().__init__()
        self.download_content = download_content
        self.signals = DownloadProcessSignals()

    @pyqtSlot()
    def run(self):
        grubber_response = grubber.download_streams(download_content=self.download_content)
        if grubber_response.status == GrubberResponseStatus.Ok:
            self.signals.result.emit(grubber_response.content)
        else:
            self.signals.error.emit(grubber_response.content)
