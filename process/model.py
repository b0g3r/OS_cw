from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt


class ChemicalProcess(QAbstractTableModel):
    def __init__(self, parent):
        super(ChemicalProcess, self).__init__()
        self.gui = parent
        self.x = tuple()
        self.y = tuple()
        self.x_label = 'x'
        self.y_label = 'y'

    def columnCount(self, parent=None, *args, **kwargs):
        return 2

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.x)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            el = ''
            if index.column() == 0:
                el = self.x[index.row()]
            elif index.column() == 1:
                el = self.y[index.row()]
            return QVariant(el)
        else:
            return QVariant()

    def headerData(self, p_int, Qt_Orientation, role=Qt.DisplayRole):

        if Qt_Orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = ''
            if p_int == 0:
                header = self.x_label
            elif p_int == 1:
                header = self.y_label
            return QVariant(header)
        else:
            return QVariant()


class DeviationConcentration(ChemicalProcess):
    def __init__(self, parent, data):
        super().__init__(parent)
        if self.validate_data(data):
            self.set_data(data)

    def set_data(self, data):
        self.x = data[0]
        self.y = data[1]

    def validate_data(self, data):
        if len(data) != 2:
            return False
        if len(data[0]) != len(data[1]):
            return False
        for column in data:
            for el in column:
                if el is None or not (isinstance(el, int) or isinstance(el, float)):
                    return None
        return True