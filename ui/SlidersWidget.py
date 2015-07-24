from PyQt4 import QtGui
from PyQt4 import Qt
from PyQt4 import QtCore


class SlidersWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(SlidersWidget, self).__init__(parent)
        self.eySlider = self.createSlider(1, 100, 1)
        self.exSlider = self.createSlider(1, 100, 1)
        self.dySlider = self.createSlider(1, 100, 1)
        self.dxSlider = self.createSlider(1, 100, 1)
        self.rMinSlider = self.createSlider(0, 255, 0)
        self.rMaxSlider = self.createSlider(0, 255, 255)
        self.gMinSlider = self.createSlider(0, 255, 0)
        self.gMaxSlider = self.createSlider(0, 255, 255)
        self.bMinSlider = self.createSlider(0, 255, 100)
        self.bMaxSlider = self.createSlider(0, 255, 255)
        self.initWidget()

    def initWidget(self):
        # create widgets
        rMinBox = getHBox()
        rMaxBox = getHBox()
        gMinBox = getHBox()
        gMaxBox = getHBox()
        bMinBox = getHBox()
        bMaxBox = getHBox()
        dxBox = getHBox()
        dyBox = getHBox()
        exBox = getHBox()
        eyBox = getHBox()

        rMinLabel = QtGui.QLabel('rMin', self)
        rMinBox.addWidget(rMinLabel, 1)
        rMaxLabel = QtGui.QLabel('rMax', self)
        rMaxBox.addWidget(rMaxLabel, 1)
        gMinLabel = QtGui.QLabel('gMin', self)
        gMinBox.addWidget(gMinLabel, 1)
        gMaxLabel = QtGui.QLabel('gMax', self)
        gMaxBox.addWidget(gMaxLabel, 1)
        bMinLabel = QtGui.QLabel('bMin', self)
        bMinBox.addWidget(bMinLabel, 1)
        bMaxLabel = QtGui.QLabel('bMax', self)
        bMaxBox.addWidget(bMaxLabel, 1)
        dxLabel = QtGui.QLabel('DilationX', self)
        dxBox.addWidget(dxLabel, 1)
        dyLabel = QtGui.QLabel('DilationY', self)
        dyBox.addWidget(dyLabel, 1)
        exLabel = QtGui.QLabel('ErosionX', self)
        exBox.addWidget(exLabel, 1)
        eyLabel = QtGui.QLabel('ErosionY', self)
        eyBox.addWidget(eyLabel, 1)

        rMinBox.addWidget(self.rMinSlider, 2)
        rMaxBox.addWidget(self.rMaxSlider, 2)
        gMinBox.addWidget(self.gMinSlider, 2)
        gMaxBox.addWidget(self.gMaxSlider, 2)
        bMinBox.addWidget(self.bMinSlider, 2)
        bMaxBox.addWidget(self.bMaxSlider, 2)
        dxBox.addWidget(self.dxSlider, 2)
        dyBox.addWidget(self.dySlider, 2)
        exBox.addWidget(self.exSlider, 2)
        eyBox.addWidget(self.eySlider, 2)

        vbox = Qt.QGridLayout()
        vbox.addLayout(rMinBox, 0, 0)
        vbox.addLayout(rMaxBox, 1, 0)
        vbox.addLayout(gMinBox, 2, 0)
        vbox.addLayout(gMaxBox, 3, 0)
        vbox.addLayout(bMinBox, 4, 0)
        vbox.addLayout(bMaxBox, 5, 0)
        vbox.addLayout(dxBox, 6, 0)
        vbox.addLayout(dyBox, 7, 0)
        vbox.addLayout(exBox, 8, 0)
        vbox.addLayout(eyBox, 9, 0)

        vbox.setColumnMinimumWidth(200, 200)

        self.setLayout(vbox)

    def createSlider(self, min, max, default=0):
        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider.setMinimumWidth(300)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setSliderPosition(default)
        return slider


def getHBox():
    hbox = QtGui.QHBoxLayout()
    hbox.addStretch(0)
    return hbox
