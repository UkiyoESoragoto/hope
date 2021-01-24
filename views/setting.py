import arrow
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QColorDialog,
)
from arrow.parser import ParserError

from views.widget import Widget


class Setting(Widget):

    def __init__(self):
        super().__init__()
        self.app.view_settings = self
        self.init_settings()

        self.setWindowFlags(
            Qt.WindowCloseButtonHint
        )

        self.btn_color: QPushButton = QPushButton('Color!', self)
        self.lab_info: QLabel = QLabel()

        self.edit_hour: QLineEdit = QLineEdit()
        self.edit_min: QLineEdit = QLineEdit()
        self.edit_sec: QLineEdit = QLineEdit()

        self.time_end: arrow.Arrow = arrow.now()

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(250, 150)
        self.center()

        self.lab_info = QLabel('Input your HOPE', self)
        self.lab_info.setMinimumWidth(230)
        self.lab_info.move(20, 20)

        self.btn_color.move(135, 20)

        self.btn_color.clicked.connect(self.show_color_dialog)

        lab_time = QLabel('Time')
        lab_separator_m = QLabel(':')
        lab_separator_s = QLabel(':')

        self.edit_hour = QLineEdit()
        self.edit_min = QLineEdit()
        self.edit_sec = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(lab_time, 1, 0)
        grid.addWidget(self.edit_hour, 1, 1)

        grid.addWidget(lab_separator_m, 1, 2)
        grid.addWidget(self.edit_min, 1, 3)

        grid.addWidget(lab_separator_s, 1, 4)
        grid.addWidget(self.edit_sec, 1, 5)

        self.setLayout(grid)

        self.time_end = arrow.get(self.settings.value('time_end'))

        self.edit_hour.setText(str(self.time_end.datetime.hour))
        self.edit_min.setText(str(self.time_end.datetime.minute))
        self.edit_sec.setText(str(self.time_end.datetime.second))

        self.edit_hour.editingFinished.connect(self.check_hour)
        self.edit_min.editingFinished.connect(self.check_minute)
        self.edit_sec.editingFinished.connect(self.check_second)

        self.setWindowTitle('Settings')

    def showEvent(self, event):
        self.time_end = arrow.get(self.settings.value('time_end'))

    def hideEvent(self, event):
        timezone = self.settings.value('timezone')
        time_now = arrow.now(timezone)
        time_end = time_now.replace(
            hour=int(self.edit_hour.text()),
            minute=int(self.edit_min.text()),
            second=int(self.edit_sec.text())
        )

        if time_end.format(
                'YYYY-MM-DD HH:mm:ss ZZ'
        ) == self.time_end.format(
            'YYYY-MM-DD HH:mm:ss ZZ'
        ):
            return

        self.settings.setValue('time_end', str(time_end))
        self.settings.sync()
        self.app.view_main.start_to_hope()

    def check_hour(self):
        try:
            hour = int(self.edit_hour.text())
        except ValueError as e:
            print(e)
            hour = -1

        if not (0 <= hour <= 23):
            self.lab_info.setText('Hour must be in 0 ~ 23')
            self.edit_hour.setFocus()
            self.edit_hour.setText(str(self.time_end.datetime.hour))

    def check_minute(self):
        try:
            minute = int(self.edit_min.text())
        except ValueError as e:
            print(e)
            minute = -1

        if not (0 <= minute <= 59):
            self.lab_info.setText('Minute must be in 0 ~ 59')
            self.edit_min.setFocus()
            self.edit_min.setText(str(self.time_end.datetime.minute))

    def check_second(self):
        try:
            second = int(self.edit_sec.text())
        except ValueError as e:
            print(e)
            second = -1

        if not (0 <= second <= 59):
            self.lab_info.setText('Second must be in 0 ~ 59')
            self.edit_sec.setFocus()
            self.edit_sec.setText(str(self.time_end.datetime.second))

    def center(self):
        qr = self.frameGeometry()
        self.move(qr.topLeft())

    def init_settings(self):
        """Time conf
        """
        timezone = self.settings.value('timezone')
        if not timezone:
            timezone = 'Asia/Shanghai'
            self.settings.setValue('timezone', timezone)
            self.settings.sync()

        time_now = arrow.now(timezone)

        time_end_str = self.settings.value('time_end')
        time_end = None

        if time_end_str:
            try:
                time_end = arrow.get(time_end_str)
            except ParserError as e:
                print(e)

        if not time_end:
            time_end = arrow.utcnow().replace(hour=18, minute=30, second=0)

        if time_end < time_now:
            time_end = arrow.utcnow().replace(hour=18, minute=30, second=0)
            if time_end < time_now:
                time_end = time_end.shift(days=1)

        delta = time_end.timestamp - time_now.timestamp

        self.settings.setValue('time_end', str(time_end))
        self.settings.setValue('time_delta', delta)
        if not self.settings.value('color'):
            self.settings.setValue('color', '#FFFFFF')

        self.settings.sync()

    def show_color_dialog(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.settings.setValue('color', col.name())
