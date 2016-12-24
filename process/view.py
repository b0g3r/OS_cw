from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import io

def distance(points):
    return max(points) - min(points)

class PointPolyPlot(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent, dpi, errorbar=None):
        self.fig = Figure(figsize=(4, 6), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        plt.style.use('seaborn-paper')
        self.axes.hold(False)
        self.gui = parent

        self.x = tuple()
        self.y = tuple()
        self.newx = []
        self.newy = []
        self.fpoly = np.poly1d([0])

        self.count_point = 0
        self.n_poly = 1

        self.errorbar = errorbar
        FigureCanvas.__init__(self, self.fig)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def set_data(self, x, y): #x_label, y_label,
        self.x = x
        self.y = y

        self.count_point = len(self.x)
        self.set_i(0)

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
            self.xnew = np.linspace(min(x), max(x), num=len(x)*10, endpoint=True)
            self.fpoly = np.poly1d(np.polyfit(x, y, self.n_poly))
            self.ynew = self.fpoly(self.xnew)
            self.axes.plot(self.xnew, self.ynew, 'r--', x, y, 'bo')
            self.axes.axis((min(x) - 0.05 * distance(x),
                            max(x) + 0.05 * distance(x),
                            min(y) - 0.05 * distance(y),
                            max(y) + 0.05 * distance(y)))
        self.errorbar.compute(self.i, self.x, self.y, self.fpoly)
        self.draw()

    def get_all_data(self):
        data = {}
        temp_i = self.i
        self.set_i(self.count_point)
        plot_image = io.BytesIO()
        self.fig.savefig(plot_image, format='png')
        data['plot_image'] = plot_image

        data['i'] = self.i
        data['x'] = self.x
        data['y'] = self.y

        data['poly'] = ' + '.join('%s*x^%s' % (coeff, n) for n, coeff in enumerate(self.fpoly.coeffs), )

        error_image = io.BytesIO()
        self.errorbar.fig.savefig(error_image, format='png')
        data['error_image'] = error_image

        data['sd'] = self.errorbar.calculate_error(self.y[:self.i], self.fpoly(self.y[:self.i]))

        self.set_i(temp_i)
        return data


class ErrorBar(FigureCanvas):
    def __init__(self, parent, dpi, text_view):
        self.fig = Figure(figsize=(4, 6), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        plt.style.use('seaborn-paper')
        self.axes.hold(False)
        self.gui = parent

        self.text_view = text_view

        FigureCanvas.__init__(self, self.fig)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute(self, i, x, y, fpoly):

        x = x[:i]
        y = y[:i]
        if i == 0 or i == 1:
            self.axes.cla()
        else:
            self.axes.errorbar(x, y, yerr=[abs(y[i]-fpoly(x[i])) for i in range(i)], ecolor='red', elinewidth=2, fmt='.')
            self.axes.axis((min(x) - 0.05 * distance(x),
                            max(x) + 0.05 * distance(x),
                            min(y) - 0.05 * distance(y),
                            max(y) + 0.05 * distance(y)))
        self.draw()
        self.text_view.setText('Среднеквадратичное отклонение: {:.4f}'.format(self.calculate_error(y, fpoly(x))))

    def calculate_error(self, y, y_a):
        if len(y) > 1:
            return np.sqrt(sum((y[i]-y_a[i])**2 for i in range(len(y)))/(len(y)-1))
        else:
            return float('nan')

