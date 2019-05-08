from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QWidget,
    QShortcut,
    QApplication,
)

from utils.utils import app_settings


class Widget(QWidget):
    settings: QSettings = app_settings()

    need_close = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app: QApplication = QApplication.instance()

        self.shortcut_close = QShortcut(QKeySequence("Ctrl+w"), self)
        self.shortcut_close.activated.connect(self.hide)

    def closeEvent(self, event):
        if not self.need_close:
            event.ignore()
            self.hide()

    def show(self):
        self.setWindowState(
            self.windowState()
            & Qt.WindowMinimized
            | Qt.WindowActive
        )
        self.activateWindow()
        super().show()

        self.raise_()
