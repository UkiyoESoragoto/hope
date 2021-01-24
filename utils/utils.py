import os
import sys

import arrow
from PySide6.QtCore import QSettings, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox

def app_settings():
    return QSettings('UkiyoESoragoto', 'hope')


def now(timezone):
    return arrow.now(timezone)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def open_url(url: str):
    try:
        # QDesktopServices.openUrl(QUrl(url))
        pass
    except Exception as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        title = 'Network error: No connection'
        msg.setText(title)
        msg.setInformativeText('Please check your network connection.')
        msg.setWindowTitle(title)
        msg.setDetailedText(e)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        msg.exec_()
