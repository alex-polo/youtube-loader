from PyQt6.QtCore import QObject, pyqtSignal

from loader.grubber.types import GrubberError, VideoInfo, GrubberSuccessLoad


class FindProcessSignals(QObject):
    error = pyqtSignal(GrubberError)
    result = pyqtSignal(VideoInfo)


class DownloadProcessSignals(QObject):
    error = pyqtSignal(GrubberError)
    result = pyqtSignal(GrubberSuccessLoad)
