from abc import ABC, abstractmethod

from PyQt6.QtWidgets import QWidget

from loader.grubber.types import VideoInfo


class ContentWidgetMeta(type(ABC), type(QWidget)):
    pass


class ContentWidget(ABC, QWidget, metaclass=ContentWidgetMeta):

    def __init__(self) -> None:
        ABC.__init__(self)
        QWidget.__init__(self)

    @abstractmethod
    def setValues(self, video: VideoInfo):
        pass

    @abstractmethod
    def _selectedItemChange(self):
        pass

    @abstractmethod
    def _eventHandlerItemChange(self):
        pass

    @abstractmethod
    def checkAvailability(self):
        pass

    @abstractmethod
    def getSelectedStream(self):
        pass
