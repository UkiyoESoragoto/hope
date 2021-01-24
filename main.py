import sys

from PySide6 import QtCore, QtWidgets, QtGui

from utils.utils import resource_path
from views import main

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(resource_path('resources/hope.png')))
    ex = main.MainWindow()
    sys.exit(app.exec_())
