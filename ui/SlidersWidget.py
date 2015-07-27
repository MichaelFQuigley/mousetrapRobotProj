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
        self.hMinSlider = self.createSlider(0, 255, 0)
        self.hMaxSlider = self.createSlider(0, 255, 255)
        self.sMinSlider = self.createSlider(0, 255, 0)
        self.sMaxSlider = self.createSlider(0, 255, 255)
        self.vMinSlider = self.createSlider(0, 255, 100)
        self.vMaxSlider = self.createSlider(0, 255, 255)
        self.initWidget()

    def initWidget(self):
        # create widgets
        hMinBox = getHBox()
        hMaxBox = getHBox()
        sMinBox = getHBox()
        sMaxBox = getHBox()
        vMinBox = getHBox()
        vMaxBox = getHBox()
        dxBox = getHBox()
        dyBox = getHBox()
        exBox = getHBox()
        eyBox = getHBox()

        hMinLabel = QtGui.QLabel('rMin', self)
        hMinBox.addWidget(hMinLabel, 1)
        hMaxLabel = QtGui.QLabel('rMax', self)
        hMaxBox.addWidget(hMaxLabel, 1)
        sMinLabel = QtGui.QLabel('gMin', self)
        sMinBox.addWidget(sMinLabel, 1)
        sMaxLabel = QtGui.QLabel('gMax', self)
        sMaxBox.addWidget(sMaxLabel, 1)
        vMinLabel = QtGui.QLabel('bMin', self)
        vMinBox.addWidget(vMinLabel, 1)
        vMaxLabel = QtGui.QLabel('bMax', self)
        vMaxBox.addWidget(vMaxLabel, 1)
        dxLabel = QtGui.QLabel('DilationX', self)
        dxBox.addWidget(dxLabel, 1)
        dyLabel = QtGui.QLabel('DilationY', self)
        dyBox.addWidget(dyLabel, 1)
        exLabel = QtGui.QLabel('ErosionX', self)
        exBox.addWidget(exLabel, 1)
        eyLabel = QtGui.QLabel('ErosionY', self)
        eyBox.addWidget(eyLabel, 1)

        hMinBox.addWidget(self.hMinSlider, 2)
        hMaxBox.addWidget(self.hMaxSlider, 2)
        sMinBox.addWidget(self.sMinSlider, 2)
        sMaxBox.addWidget(self.sMaxSlider, 2)
        vMinBox.addWidget(self.vMinSlider, 2)
        vMaxBox.addWidget(self.vMaxSlider, 2)
        dxBox.addWidget(self.dxSlider, 2)
        dyBox.addWidget(self.dySlider, 2)
        exBox.addWidget(self.exSlider, 2)
        eyBox.addWidget(self.eySlider, 2)

        vbox = Qt.QGridLayout()
        vbox.addLayout(hMinBox, 0, 0)
        vbox.addLayout(hMaxBox, 1, 0)
        vbox.addLayout(sMinBox, 2, 0)
        vbox.addLayout(sMaxBox, 3, 0)
        vbox.addLayout(vMinBox, 4, 0)
        vbox.addLayout(vMaxBox, 5, 0)
        vbox.addLayout(dxBox, 6, 0)
        vbox.addLayout(dyBox, 7, 0)
        vbox.addLayout(exBox, 8, 0)
        vbox.addLayout(eyBox, 9, 0)

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
