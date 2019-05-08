import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from utils.utils import resource_path
from views import main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('resources/hope.png')))
    ex = main.MainWindow()
    sys.exit(app.exec_())
