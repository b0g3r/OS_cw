# -*- coding: utf-8 -*-
import settings
import sys

from UI.main_frame import MainFrame
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    settings = settings.get_settings()
    print(settings)
    app = QApplication(sys.argv)
    ex = MainFrame()
    sys.exit(app.exec_())