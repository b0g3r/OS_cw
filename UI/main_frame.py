from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5 import uic
import exemap

class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(exemap.get_file_name('UI\\mainwindow.ui'), self)
        self.initUI()

    def initUI(self):
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())