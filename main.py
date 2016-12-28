# -*- coding: utf-8 -*-
import sys

from UI.main_frame import MainFrame
from PyQt5.QtWidgets import QApplication

# TODO: os.system('start "" "file.pdf"')


if __name__ == '__main__':
    current_exit_code = MainFrame.EXIT_CODE_RESTART
    while current_exit_code == MainFrame.EXIT_CODE_RESTART:
        app = QApplication(sys.argv)
        print(sys.argv)

        ex = MainFrame(*sys.argv[1:])
        sys._excepthook = sys.excepthook

        def my_exception_hook(exctype, value, traceback):
            # fix unhandled exception
            ex.display_error(value)
            sys._excepthook(exctype, value, traceback)
            sys.exit(1)

        sys.excepthook = my_exception_hook

        current_exit_code = app.exec_()
        ex.close()
        app = None
        ex = None
