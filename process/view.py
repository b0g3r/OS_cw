from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


def distance(points):
    return max(points) - min(points)

class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent, dpi):
        fig = Figure(figsize=(4, 6), dpi=dpi)
        self.axes = fig.add_subplot(111)
        plt.style.use('seaborn-paper')
        self.axes.hold(False)
        self.gui = parent
        self.x = tuple()
        self.y = tuple()
        self.count_point = 0
        self.n_poly = 1

        FigureCanvas.__init__(self, fig)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def set_data(self, x, y): #x_label, y_label,
        self.x = x
        self.y = y

        self.count_point = len(self.x)

    @pyqtSlot(int, name='set_npoly')
    def set_npoly(self, n_poly):
        self.n_poly = n_poly
        self.compute()

    @pyqtSlot(int, name='set_i')
    def set_i(self, i):
            self.i = i
            self.compute()

    def compute(self):
        x = self.x[0:self.i]
        y = self.y[0:self.i]
        if self.i == 0:
            self.axes.cla()
        elif self.i == 1:
            self.axes.plot(x, y, 'bo')
        else:
            f_poly = np.poly1d(np.polyfit(x, y, self.n_poly))

            xnew = np.linspace(min(x), max(x), num=len(x) * 10, endpoint=True)
            self.axes.plot(xnew, f_poly(xnew), 'r--', x, y, 'bo')
            self.axes.axis((min(x) - 0.05 * distance(x),
                            max(x) + 0.05 * distance(x),
                            min(y) - 0.05 * distance(y),
                            max(y) + 0.05 * distance(y)))

        self.draw()


