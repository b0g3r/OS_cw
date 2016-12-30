import os
import csv

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QFileDialog, QMessageBox, QApplication
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QTimer, QUrl
from PyQt5.QtGui import QDesktopServices

from openpyxl import load_workbook

import exemap
from process import model, view
from settings import Settings
from .settings_frame import SettingsFrame
from .about_frame import AboutFrame
import report


def get_data_from_xlsx(file_name):
    try:
        wb = load_workbook(filename=file_name,
                           read_only=True)
        ws = wb[wb.get_sheet_names()[0]]
        data = tuple(zip(*(tuple(cell.value for cell in column) for column in ws.rows)))
        wb._archive.close()
        return data
    except:
        return None


def get_data_from_oscw(file_name):
    try:
        data = csv.reader(open(file_name), delimiter=',')
        data = tuple(zip(*(tuple(float(cell) for cell in row) for row in data)))
        return data
    except:
        return None


class MainFrame(QMainWindow):
    EXIT_CODE_RESTART = 234

    def __init__(self, filename=None):
        self.settings = Settings()
        super().__init__()
        uic.loadUi(exemap.get_file_name(r'UI\mainwindow.ui'), self)
        self.init_ui()
        if filename is not None:
            self.load_data(filename)

    def init_ui(self):
        if self.settings.fullscreen:
            self.showMaximized()
        else:
            self.center()

        self.error_dialog = QMessageBox()
        self.error_dialog.setIcon(QMessageBox.Warning)
        self.error_dialog.setWindowTitle("Ошибка")

        # коннект меню
        self.action_openFile.triggered.connect(self.load_data, no_receiver_check=False)
        self.action_openSettings.triggered.connect(self.open_settings)
        self.action_saveReport.triggered.connect(self.create_report)

        self.action_step_back.triggered.connect(self.step_back)
        self.action_step_forward.triggered.connect(self.step_forward)
        self.action_play.triggered.connect(self.start_play)

        self.action_openAbout.triggered.connect(self.open_about)
        self.action_openHelp.triggered.connect(self.open_help)

        self.tableView_data.setModel(model.ChemicalProcess(self))
        self.tableView_data.resizeColumnsToContents()

        # график
        self.verticalLayout_4.removeWidget(self.graphicsView_2)
        self.graphicsView_2.deleteLater()
        self.graphicsView_2 = None
        self.errorbar = view.ErrorBar(self, dpi=80, text_view=self.text_errors)
        self.verticalLayout_4.insertWidget(0, self.errorbar)

        # диаграмма ошибок
        self.verticalLayout_2.removeWidget(self.graphicsView)
        self.graphicsView.deleteLater()
        self.graphicsView = None
        self.mpl = view.PointPolyPlot(self, dpi=80, errorbar=self.errorbar)
        self.verticalLayout_2.insertWidget(0, self.mpl)

        self.timer = QTimer()
        self.timer.timeout.connect(self.step_forward)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def display_error(self, error):
        self.error_dialog.setText(str(error))
        self.error_dialog.exec_()

    @pyqtSlot()
    def load_data(self, filename=None):
        if filename is None:
            filename = self.get_file_name()
        data = tuple()

        if filename is not None:  # check file is selected
            # extract data from file
            if filename.endswith('.xlsx'):
                data = get_data_from_xlsx(filename)
            elif filename.endswith('.oscw'):
                data = get_data_from_oscw(filename)
        else:
            return

        if data is None:  # extracting failure
            self.display_error('Неправильный формат файла')
        else:
            self.initiate_model(data)

    def open_help(self):
        QDesktopServices().openUrl(QUrl().fromLocalFile('chm.chm'))

    def create_report(self):
        """вызывает создание и сохранение отчета"""
        if hasattr(self, 'model'):
            report.create(self.mpl.get_all_data())
        # TODO: сказать что отчёт сохранен

    def initiate_model(self, data):
        self.model = model.DeviationConcentration(self)
        self.model.set_data(data)
        self.horizontalSlider.valueChanged.connect(self.mpl.set_i)
        self.spinBox.valueChanged.connect(self.mpl.set_npoly)
        self.spinBox.setValue(self.settings.poly_n)
        if self.settings.autoplay:
            self.start_play()

    def start_play(self):
        self.timer.start(1000)

    def step_back(self):
        self.horizontalSlider.setValue(self.horizontalSlider.value() - 1)

    def step_forward(self):
        i = self.horizontalSlider.value()
        if i == self.horizontalSlider.maximum():
            self.timer.stop()
        self.horizontalSlider.setValue(self.horizontalSlider.value() + 1)

    @pyqtSlot(name='initiate_view')
    def initiate_view(self):
        self.tableView_data.setModel(self.model)
        self.tableView_data.resizeColumnsToContents()
        self.mpl.set_data(*self.model.get_data())  # data - tuple of tuple_x and tuple_y
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(self.mpl.count_point)

    def get_file_name(self):
        file_name = QFileDialog.getOpenFileName(self, 'Открыть', os.getcwd(),
                                            'Table file (*.oscw *.xlsx)')
        return file_name[0] or None

    def open_about(self):
        """Вызывает гуи окна 'О Программе'"""
        about = AboutFrame()
        about.exec_()

    def open_settings(self):
        """Вызыывает гуи настроек"""
        sets = SettingsFrame()
        sets.setModal(False)
        # если 0 - отмена, если 1 - изменились настройки перезапустить программу
        if sets.exec_() == 1:
            QApplication.exit(self.EXIT_CODE_RESTART)