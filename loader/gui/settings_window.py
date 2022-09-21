from typing import Optional

from PyQt6.QtWidgets import QDialog

from loader.gui.ui import Ui_SettingsWindow
from loader.misc import Settings


class SettingsWindow(QDialog):

    def __init__(self) -> None:
        QDialog.__init__(self)
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        self._settings: Optional[Settings] = None
        self.ui.okButton.clicked.connect(self.close_with_saving)
        self.ui.cancelButton.clicked.connect(self.close_window)

    def setValues(self, settings: Settings) -> None:
        self._settings = settings
        grubber_config = self._settings.grubber_config()
        ffmpeg_config = self._settings.ffmpeg_config()

        self.ui.minProgressiveResolutionComboBox.addItems(grubber_config.resolution_values)
        self.ui.minDashVideoResolutionComboBox.addItems(grubber_config.resolution_values)
        self.ui.minDashAudioBitrateComboBox.addItems(grubber_config.bitrate_values)
        self.ui.ffmpegThreadsComboBox.addItems(ffmpeg_config.threads_values)

        self.ui.minProgressiveResolutionComboBox.setCurrentText(grubber_config.min_progressive_resolution)
        self.ui.minDashVideoResolutionComboBox.setCurrentText(grubber_config.min_dash_video_resolution)
        self.ui.minDashAudioBitrateComboBox.setCurrentText(grubber_config.min_dash_audio_bitrate)
        self.ui.ffmpegThreadsComboBox.setCurrentText(ffmpeg_config.threads)

    def close_with_saving(self):
        self._settings.update_min_progressive_resolution(self.ui.minProgressiveResolutionComboBox.currentText())
        self._settings.update_min_dash_video_resolution(self.ui.minDashVideoResolutionComboBox.currentText())
        self._settings.update_min_dash_audio_bitrate(self.ui.minDashAudioBitrateComboBox.currentText())
        self._settings.update_ffmpeg_thread(self.ui.ffmpegThreadsComboBox.currentText())
        self.close()

    def close_window(self):
        self.close()
