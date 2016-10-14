# -*- coding: utf-8 -*-
import settings
import sys

from UI.main_frame import MainFrame
from PyQt5.QtWidgets import QApplication

sys._excepthook = sys.excepthook
def my_exception_hook(exctype, value, traceback):
    # fix unhandled exception
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = my_exception_hook


if __name__ == '__main__':

    settings = settings.get_settings()
    print(settings)
    app = QApplication(sys.argv)
    ex = MainFrame()
    sys.exit(app.exec_())
