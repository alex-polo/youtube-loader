from typing import Optional

from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QMainWindow, QWidget
from loguru import logger

from loader.misc import Settings
from loader.gui.mixins import MainWindowMixin
from loader.gui.ui import Ui_MainWindow

from loader.grubber.types import (
    VideoInfo,
    GrubberError,
    StreamType,
)
from loader.gui.widgets import (
    FindWidget,
    LoadScreenWidget,
    DisplayVideoDetailsWidget,
)
from loader.gui.exceptions import (
    grubber_error_handler_exception,
    gui_qt_slot_handler_exception,
    grubber_error_message,
    gui_handler_exception,
)


class MainWindow(MainWindowMixin, QMainWindow):

    def __init__(self, settings: Settings) -> None:
        MainWindowMixin.__init__(self)
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.registryActions()

        self._settings = settings
        self.findWidget: Optional[FindWidget] = None
        self.loadScreenWidget: Optional[LoadScreenWidget] = None
        self.displayVideoDetailsWidget: Optional[DisplayVideoDetailsWidget] = None

        self.showFindWidget()

    @gui_qt_slot_handler_exception
    def actionSearchingVideo(self) -> None:
        logger.debug(f'start action search video, url: {self.findWidget.ui.url.text()}')
        self.hiddenWidget(self.findWidget)
        self.showLoadScreen()
        self.find_video_details(
            url=self.findWidget.ui.url.text(),
            grubber_config=self._settings.grubber_config(),
            success_event=self.event_video_find,
            error_event=self.event_video_not_found)

    @gui_qt_slot_handler_exception
    def actionDownload(self) -> None:
        logger.debug('start download action')
        download_content = self.displayVideoDetailsWidget.getDownloadContent()
        logger.debug(f'Content to download: {download_content}')

        filename, type_filename = download_content.download_filename.split('.')
        user_filename = self.save_file_dialog(
            window=self,
            app_directory=self._settings.grubber_config().app_directory,
            default_filename=filename,
            type_filename=type_filename)
        logger.debug(f'User select file save: {user_filename}.')

        if len(user_filename) > 0:
            if filename != download_content.download_filename:
                download_content.download_filename = user_filename
            if download_content.stream_type == StreamType.DashAudio \
                    or download_content.stream_type == StreamType.DasVideo:
                self.download_video(download_content=download_content, ffmpeg_config=self._settings.ffmpeg_config())
            else:
                self.download_video(download_content=download_content)
        else:
            logger.debug('User cancel select file, name is empty.')

    @gui_qt_slot_handler_exception
    def actionBack(self) -> None:
        logger.debug('start action back button pressed')
        self.hideDisplayVideoDetails()
        self.showFindWidget()
        self.ui.backButton.setEnabled(False)

    @gui_handler_exception
    def closeEvent(self, event: QCloseEvent) -> None:
        logger.debug('start action close main window.')
        self.clear_temp_folder(temp_directory=self._settings.grubber_config().temporary_directory)

    @gui_qt_slot_handler_exception
    def actionOpenSettings(self) -> None:
        logger.info('start action open misc.')
        self.open_settings(settings=self._settings)

    def registryActions(self) -> None:
        logger.debug('registry action main window')
        self.ui.settingsButton.clicked.connect(self.actionOpenSettings)
        self.ui.backButton.clicked.connect(self.actionBack)

    def event_video_find(self, video: VideoInfo) -> None:
        logger.debug('Video found')
        self.hideLoadScreen()
        self.ui.backButton.setEnabled(True)
        self.showDisplayVideoDetails(video=video)

    def event_video_not_found(self, grubber_error: GrubberError) -> None:
        logger.debug('Video not found')
        grubber_error_handler_exception(grubber_error=grubber_error)
        grubber_error_message(grubber_error=grubber_error)
        self.hideLoadScreen()
        self.showFindWidget()

    def showDisplayVideoDetails(self, video: VideoInfo) -> None:
        logger.debug('show widget display video.')
        self.displayVideoDetailsWidget = DisplayVideoDetailsWidget()
        self.displayVideoDetailsWidget.setVideoContent(video)
        self.ui.contentLayout.addWidget(self.displayVideoDetailsWidget)
        self.displayVideoDetailsWidget.ui.downloadButton.clicked.connect(self.actionDownload)

    def hideLoadScreen(self) -> None:
        logger.debug('hide load screen.')
        self.hiddenWidget(self.loadScreenWidget)
        self.loadScreenWidget = None

    def hideDisplayVideoDetails(self) -> None:
        logger.debug('hide widget display video.')
        self.hiddenWidget(self.displayVideoDetailsWidget)
        self.displayVideoDetailsWidget = None

    def showFindWidget(self) -> None:
        logger.debug('show searching widget.')
        self.findWidget = FindWidget()
        self.ui.contentLayout.addWidget(self.findWidget)
        self.findWidget.ui.findButton.clicked.connect(self.actionSearchingVideo)

    def showLoadScreen(self) -> None:
        logger.debug('show load screen.')
        self.loadScreenWidget = LoadScreenWidget()
        self.ui.contentLayout.addWidget(self.loadScreenWidget)

    @classmethod
    def hiddenWidget(cls, widget: QWidget) -> None:
        widget.setParent(None)
        widget.deleteLater()
