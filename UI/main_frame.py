from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
import exemap
import os
from openpyxl import load_workbook
from process import model, view

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
        self.verticalLayout_2.removeWidget(self.graphicsView)
        self.graphicsView.deleteLater()
        self.graphicsView = None
        self.mpl = view.MplCanvas(self, dpi=80)
        self.verticalLayout_2.insertWidget(0, self.mpl)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def display_error(self, error):
        print(error)
        # TODO

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
            self.initiate_model(data)

    def initiate_model(self, data):
        self.model = model.DeviationConcentration(self)
        self.model.set_data(data)
        self.horizontalSlider.valueChanged.connect(self.mpl.set_i)
        self.spinBox.valueChanged.connect(self.mpl.set_npoly)


    def change_i(self, i):
        self.mpl.set_i(i)

    @pyqtSlot(name='initiate_view')
    def initiate_view(self):
        self.tableView_data.setModel(self.model)
        self.mpl.set_data(*self.model.get_data())  # data - tuple of tuple_x and tuple_y
        self.mpl.set_i(5)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(self.mpl.count_point)


    def get_file_name(self):
        file_name = QFileDialog.getOpenFileName(self, 'Открыть', os.getcwd(),
                                            'Table file (*.oscw, *.xlsx)')
        return file_name[0] or None
