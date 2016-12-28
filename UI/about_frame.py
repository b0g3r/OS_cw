from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


import exemap

class AboutFrame(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(exemap.get_file_name(r'UI\about.ui'), self)
        self.init_ui()

    def init_ui(self):
        self.pushButton.clicked.connect(lambda x: self.accept())
