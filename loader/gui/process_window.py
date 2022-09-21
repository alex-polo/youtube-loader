from PyQt6.QtWidgets import QDialog

from loader.gui.ui import Ui_OutProcessWindow


class OutProcessWindow(QDialog):

    def __init__(self) -> None:
        QDialog.__init__(self)
        self.ui = Ui_OutProcessWindow()
        self.ui.setupUi(self)

    def print(self, message: str) -> None:
        self.ui.textEdit.append(message)

    def closeWindow(self):
        self.close()

    def finishStatus(self):
        self.ui.okButton.setEnabled(True)
        self.ui.okButton.clicked.connect(self.closeWindow)
