import sys
from time import sleep

import arrow
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import (QIcon, QKeySequence,
    QShortcut,    QAction)
from PySide6.QtWidgets import (
    QMainWindow,
    QFrame,
    QSystemTrayIcon,
    QMenu,
    QApplication,
    QMessageBox,
)

from config import HEIGHT, VERSION
from utils.updater import Updater
from utils.utils import app_settings, now, resource_path, open_url
from views.about import About
from views.setting import Setting


class ForHope(QThread):
    """Runs a counter thread.
    """
    countChanged = Signal(int)

    def run(self):
        settings = app_settings()
        tz = settings.value('timezone')
        width = settings.value('screen_width')
        time_end = arrow.get(settings.value('time_end'))
        time_delta = settings.value('time_delta')
        while now(tz) < time_end:
            frequency = time_delta / width
            if frequency < 0.0166:
                frequency = 0.0166
            process = width - int(
                (time_end.float_timestamp - now(tz).float_timestamp)
                / time_delta
                * width
            )
            sleep(frequency)
            self.countChanged.emit(process)
        self.countChanged.emit(width)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = QApplication.instance()

        self.calc: QThread = QThread()
        self.frm: QFrame = QFrame(self)
        self.tray_icon_menu: QMenu = QMenu(self)
        self.tray_icon: QSystemTrayIcon = QSystemTrayIcon(self)

        self.app.view_main = self
        Setting()
        About()
        self.init_settings()
        self.init_main_window()
        self.init_tray_icon()
        self.init_frm()

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.shortcut_settings = QShortcut(QKeySequence("Ctrl+,"), self)
        self.shortcut_settings.activated.connect(self.show_settings)
        self.shortcut_refresh = QShortcut(QKeySequence("Ctrl+r"), self)
        self.shortcut_refresh.activated.connect(self.start_to_hope)
        self.shortcut_refresh = QShortcut(QKeySequence("Ctrl+q"), self)
        self.shortcut_refresh.activated.connect(self.close)

        if 'darwin' in sys.platform:
            menubar = self.menuBar()
            hope_menu = menubar.addMenu('Hope')

            hope_menu.addAction(
                QAction('About', self, triggered=self.show_about))
            hope_menu.addAction(
                QAction('Settings', self, triggered=self.show_settings)
            )

        self.show()
        # self.show_settings()
        self.start_to_check_update()

    def init_settings(self):
        settings = app_settings()

        # Screen conf
        screen = self.app.primaryScreen()
        screen_size = screen.size()
        width = screen_size.width()
        height = screen_size.height()
        rect = screen.availableGeometry()
        print('Screen: %s' % screen.name())
        print('Size: %d x %d' % (width, height))
        print('Available size: %d x %d' % (rect.width(), rect.height()))
        print('Available at: %d x %d' % (rect.x(), rect.y()))

        settings.setValue('screen_width', width)
        settings.setValue('screen_height', height)

        y = rect.y() if rect.y() else 0
        self.move(0, y)

        settings.sync()

    def init_main_window(self):
        self.setWindowTitle('Hope')

        if 'darwin' in str(sys.platform):
            self.setWindowFlags(
                Qt.WindowStaysOnTopHint
                | Qt.FramelessWindowHint
            )
        else:
            self.setWindowFlags(
                Qt.WindowStaysOnTopHint
                | Qt.FramelessWindowHint
                | Qt.Tool
            )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(app_settings().value('screen_width'), HEIGHT)

    def init_tray_icon(self):
        self.tray_icon_menu.addAction(
            QAction('Settings', self, triggered=self.show_settings)
        )
        self.tray_icon_menu.addAction(
            QAction('Speed up!', self, triggered=self.start_to_hope)
        )
        self.tray_icon_menu.addAction(
            QAction('About', self, triggered=self.show_about)
        )
        self.tray_icon_menu.addAction(
            QAction('&Quit', self, triggered=self.close)
        )
        self.tray_icon.setIcon(QIcon(resource_path('resources/hope-h.png')))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

    def init_frm(self):
        color = app_settings().value('color')
        self.frm.setStyleSheet('QWidget { background-color: %s }' % color)
        self.frm.setGeometry(0, 0, 0, HEIGHT)

    def show_settings(self):
        self.app.view_settings.show()

    def show_about(self):
        self.app.view_about.show()

    def on_refresh(self, value):
        self.frm.setGeometry(0, 0, value, 4)
        color = app_settings().value('color')
        self.frm.setStyleSheet('QWidget { background-color: %s }' % color)

    def showEvent(self, event):
        self.start_to_hope()

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.tray_icon.hide()
        if self.app.view_settings:
            self.app.view_settings.need_close = True
            self.app.view_settings.close()
        if self.app.view_about:
            self.app.view_about.need_close = True
            self.app.view_about.close()

    @staticmethod
    def show_update_info(info: dict):
        print(info)

        html_url = info.get('html_url', '')
        content = [
            f'New v{info.get("version")} (Now v{VERSION})',
            info.get('name', ''),
            html_url,
        ]
        title = 'Update available, download now?'

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(title)
        msg.setInformativeText('\n\n'.join(content))
        msg.setWindowTitle(title)
        msg.setDetailedText(info.get('desc', ''))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        btn_ret = msg.exec_()

        if btn_ret == QMessageBox.Yes:
            print('Yes clicked.')
            open_url(html_url)
        elif btn_ret == QMessageBox.Ok:
            print('Ok clicked.')
        elif btn_ret == QMessageBox.No:
            print('No clicked.')
        elif btn_ret == QMessageBox.Cancel:
            print('Cancel')

    def start_to_hope(self):
        self.on_refresh(0)
        new = ForHope()
        new.countChanged.connect(self.on_refresh)
        new.start()
        if self.calc:
            self.calc.terminate()
            self.app.view_settings.init_settings()
        self.calc = new

    def start_to_check_update(self):
        pass
        # check = Updater()
        # check.check.connect(self.show_update_info)
        # check.start()

        # timer = QTimer(self)
        # timer.timeout.connect(self.check_update)
        # timer.start(1000 * 3600 * 12)  # Check update per 12 hours
