from PyQt6 import QtGui
from PyQt6.QtWidgets import QMessageBox

from loader.grubber.types import GrubberError, GrubberErrorType


def _get_icon():
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("src/img/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    return icon


def error_message():
    dlg = QMessageBox()
    dlg.setWindowTitle('Ошибка.')
    dlg.setText('Упс, что-то пошло не так. Обратитесь к разработчику.')
    dlg.setInformativeText('Подробности в лог файле.')
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    dlg.setIcon(QMessageBox.Icon.Warning)
    dlg.setWindowIcon(_get_icon())
    dlg.exec()


def grubber_error_message(grubber_error: GrubberError) -> None:
    dlg = QMessageBox()
    dlg.setWindowTitle(grubber_error.title)
    dlg.setText(grubber_error.text)
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    dlg.setWindowIcon(_get_icon())

    if grubber_error.grubber_error_type == GrubberErrorType.Error:
        dlg.setDetailedText(grubber_error.details)
        dlg.setIcon(QMessageBox.Icon.Critical)
    elif grubber_error.grubber_error_type == GrubberErrorType.Warning:
        dlg.setDetailedText(grubber_error.details)
        dlg.setIcon(QMessageBox.Icon.Warning)
    elif grubber_error.grubber_error_type == GrubberErrorType.Info:
        dlg.setIcon(QMessageBox.Icon.Information)

    dlg.exec()
