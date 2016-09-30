from registry import settings
from PyQt5.QtWidgets import QWidget, QDesktopWidget


class MainFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.initSettings()
        self.initUI()

    def initSettings(self):
        if not settings.get_setting('state'):
            settings.edit_setting('state', 'set')

    def initUI(self):
        self.resize(250, 150)
        self.center()

        self.setWindowTitle('Center')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())