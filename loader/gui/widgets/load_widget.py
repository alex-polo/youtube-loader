from PyQt6.QtWidgets import QWidget

from loader.gui.ui import Ui_LoadScreen


class LoadScreenWidget(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_LoadScreen()
        self.ui.setupUi(self)
