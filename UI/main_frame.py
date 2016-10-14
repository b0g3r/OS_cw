from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QFileDialog, QTableView
from PyQt5 import uic
import exemap
import os
from openpyxl import load_workbook
from process import model

def get_data_from_xlsx(file_name):
    try:
        wb = load_workbook(filename=file_name,
                           read_only=True)
        ws = wb[wb.get_sheet_names()[0]]
        data = tuple(zip(*(tuple(cell.value for cell in column) for column in ws.rows)))
        wb._archive.close()
        return data
    except OSError:
        return None


def get_data_from_oscw(file_name):
    try:
        pass
    except OSError:
        return None


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(exemap.get_file_name(r'UI\mainwindow.ui'), self)
        self.initUI()

    def initUI(self):
        self.center()
        self.action_openFile.triggered.connect(self.load_data)
        self.tableView_data.setModel(model.ChemicalProcess(self))
        self.tableView_data.resizeColumnsToContents()
        self.show()


    def load_data(self):
        file_name = self.get_file_name()
        data = tuple()
        if file_name is not None:  # check file is selected
            # extract data from file
            if file_name.endswith('.xlsx'):
                data = get_data_from_xlsx(file_name)
            elif file_name.endswith('.oscw'):
                data = get_data_from_oscw(file_name)
        else:
            return

        if data is None:  # extracting failure
            self.display_error('Неправильный формат файла')
        else:
            self.tableView_data.setModel(model.DeviationConcentration(self, data))

    def display_error(self, error):
        pass

    def get_file_name(self):
        file_name = QFileDialog.getOpenFileName(self, 'Открыть', os.getcwd(),
                                            'Table file (*.oscw, *.xlsx)')
        return file_name[0] or None

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())