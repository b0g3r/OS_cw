from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic


import exemap
from settings import Settings


class SettingsFrame(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(exemap.get_file_name(r'UI\settings.ui'), self)
        self.settings = Settings()
        self.init_ui()

    def init_ui(self):
        self.spinBox_polynum.setValue(self.settings.poly_n)
        self.checkBox_fullscreen.setCheckState(2 if self.settings.fullscreen else 0)
        self.checkBox_autoplay.setCheckState(2 if self.settings.autoplay else 0)
        self.pushButton_save.clicked.connect(self.save_settings)

    def save_settings(self):
        """предупреждает о перезапуске и сохраняет настройки"""
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        msgbox.setText("Программа будет перезапущена")
        msgbox.setWindowTitle("Вы уверены?")
        if msgbox.exec_() == QMessageBox.Ok:
            self.settings.fullscreen = self.checkBox_fullscreen.checkState() == 2
            self.settings.autoplay = self.checkBox_autoplay.checkState() == 2
            self.settings.poly_n = self.spinBox_polynum.value()
            self.accept()