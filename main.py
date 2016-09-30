import registry.settings as settings

# -*- coding: utf-8 -*-

import sys
from UI.main_frame import MainFrame
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainFrame()
    sys.exit(app.exec_())