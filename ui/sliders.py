from PyQt4 import QtGui
from PyQt4 import Qt
from PyQt4 import QtCore
from settings import settings
from functools import partial

class SlidersDialog(QtGui.QDialog):
    def __init__(self, parent):
        super(SlidersDialog, self).__init__(parent)
        grid = Qt.QGridLayout()
        self.init_slider('ey',   1, 100, grid)
        self.init_slider('ex',   1, 100, grid)
        self.init_slider('dy',   1, 100, grid)
        self.init_slider('dx',   1, 100, grid)
        self.init_slider('rMin', 0, 255, grid)
        self.init_slider('rMax', 0, 255, grid)
        self.init_slider('gMin', 0, 255, grid)
        self.init_slider('gMax', 0, 255, grid)
        self.init_slider('bMin', 0, 255, grid)
        self.init_slider('bMax', 0, 255, grid)
        self.setLayout(grid);

    def init_slider(self, variable, min_val, max_val, grid):
        row = grid.rowCount()
        label = QtGui.QLabel(str(settings[variable]))
        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider.setMinimumWidth(300)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setSliderPosition(settings[variable])
        slider.valueChanged.connect(partial(self.on_change, variable, label))

        grid.addWidget(QtGui.QLabel(variable, self), row, 0)
        grid.addWidget(slider, row, 1)
        grid.addWidget(label, row, 2)
        
    def on_change(self, variable, label, value):
        settings[variable] = value
        label.setText(str(value))
