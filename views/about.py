import sys
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QLabel,
    QGridLayout,
)

from views.widget import Widget
from config import VERSION


class About(Widget):

    def __init__(self):
        super().__init__()

        self.app.view_about = self

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(400, 180)
        self.center()

        content = ([] if 'darwin' not in sys.platform else [
            'Press Cmd + r to speed up(refresh)',
            'Press Cmd + , to open settings',
            'Press Cmd + q to quit',
        ])

        content.append(f'Version {VERSION}')

        grid = QGridLayout()
        grid.setSpacing(10)

        a_tag = '''
        <a href="https://ukiyoesoragoto.com" style="color:Black">
            By UkiyoESoragoto (๑•̀ㅂ•́)و✧
        </a>
        '''
        lab = QLabel(a_tag)
        lab.setOpenExternalLinks(True)
        grid.addWidget(lab, 0, 0)
        for index, line in enumerate(content):
            grid.addWidget(QLabel(line), index + 1, 0)

        self.setLayout(grid)

        self.setWindowTitle('About')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
