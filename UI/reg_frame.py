from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic


import exemap
import json

class RegFrame(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(exemap.get_file_name(r'UI\reg.ui'), self)
        self.msgbox = QMessageBox()
        self.init_ui()

    def init_ui(self):
        self.pushButton_reg.clicked.connect(self.registration)
        self.pushButton_login.clicked.connect(self.login)

        self.msgbox.setWindowTitle("Ошибка")

    def print_error(self, error):
        self.msgbox.setText(error)
        self.msgbox.exec_()

    def login(self):
        if self.lineEdit_login.text() != '' and self.lineEdit_pass.text() != "":
            data = json.load(open('data.regos', 'r'))
            if data.get(self.lineEdit_login.text()) == self.lineEdit_pass.text():
                self.accept()
            else:
                self.print_error("Неправильная связка логин-пароль")
        else:
            self.print_error("Все поля должны быть заполнены")

    def registration(self):
        if self.lineEdit_login_reg.text() != '' and self.lineEdit_pass_reg.text() != "" and self.lineEdit_pass_reg.text() != "":
            if self.lineEdit_pass_reg.text() != self.lineEdit_pass2_reg.text():
                self.print_error("Пароли не совпадают")
                self.lineEdit_pass_reg.setText('')
                self.lineEdit_pass2_reg.setText('')
            else:
                try:
                    data = json.load(open('data.regos', 'r'))
                except:
                    data = {}
                data[self.lineEdit_login_reg.text()] = self.lineEdit_pass_reg.text()
                json.dump(data, open('data.regos', 'w'))
                self.print_error("Регистрация успешна")
        else:
            self.print_error("Все поля должны быть заполнены")
