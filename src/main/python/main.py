import sys

from PyQt5.QtGui import QIcon
from fbs_runtime.application_context import ApplicationContext

from views import main


class AppContext(ApplicationContext):
    def run(self):
        window = main.MainWindow()

        self.app.setWindowIcon(QIcon(self.get_resource('hope.png')))
        version = self.build_settings['version']
        window.setWindowTitle("Hope v" + version)
        window.show()
        return self.app.exec_()


if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)

    # app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon('media/hope.png'))
    # ex = hope.MainWindow(app)
    # sys.exit(app.exec_())
