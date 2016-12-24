# -*- coding: utf-8 -*-
from settings import Settings
import sys

from UI.main_frame import MainFrame
from PyQt5.QtWidgets import QApplication

# todo: os.system('start "" "file.pdf"')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainFrame()

    sys._excepthook = sys.excepthook


    def my_exception_hook(exctype, value, traceback):
        # fix unhandled exception
        ex.display_error(value)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.excepthook = my_exception_hook

    sys.exit(app.exec_())
