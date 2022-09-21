from PyQt6.QtWidgets import QWidget

from loader.gui.ui import Ui_FindWidget


class FindWidget(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_FindWidget()
        self.ui.setupUi(self)
