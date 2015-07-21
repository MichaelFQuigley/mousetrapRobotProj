from PyQt4 import QtGui
from PyQt4 import Qt
from PyQt4 import QtCore


class SlidersWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(SlidersWidget, self).__init__(parent)
        self.eySlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.exSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.dySlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.dxSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.bMaxSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.bMinSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.rMinSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.rMaxSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.gMinSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.gMaxSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
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

        self.rMinSlider.setMinimum(0)
        self.rMinSlider.setMaximum(255)
        self.rMinSlider.setSliderPosition(0)
        rMinBox.addWidget(self.rMinSlider, 2)
        self.rMaxSlider.setMinimum(0)
        self.rMaxSlider.setMaximum(255)
        self.rMaxSlider.setSliderPosition(255)
        rMaxBox.addWidget(self.rMaxSlider, 2)
        self.gMinSlider.setMinimum(0)
        self.gMinSlider.setMaximum(255)
        self.gMinSlider.setSliderPosition(0)
        gMinBox.addWidget(self.gMinSlider, 2)
        self.gMaxSlider.setMinimum(0)
        self.gMaxSlider.setMaximum(255)
        self.gMaxSlider.setSliderPosition(255)
        gMaxBox.addWidget(self.gMaxSlider, 2)
        self.bMinSlider.setMinimum(0)
        self.bMinSlider.setMaximum(255)
        self.bMinSlider.setSliderPosition(0)
        bMinBox.addWidget(self.bMinSlider, 2)
        self.bMaxSlider.setMinimum(0)
        self.bMaxSlider.setMaximum(255)
        self.bMaxSlider.setSliderPosition(255)
        bMaxBox.addWidget(self.bMaxSlider, 2)
        self.dxSlider.setMinimum(0)
        self.dxSlider.setMaximum(100)
        self.dxSlider.setSliderPosition(0)
        dxBox.addWidget(self.dxSlider, 2)
        self.dySlider.setMinimum(0)
        self.dySlider.setMaximum(100)
        self.dySlider.setSliderPosition(0)
        dyBox.addWidget(self.dySlider, 2)
        self.exSlider.setMinimum(0)
        self.exSlider.setMaximum(100)
        self.exSlider.setSliderPosition(0)
        exBox.addWidget(self.exSlider, 2)
        self.eySlider.setMinimum(0)
        self.eySlider.setMaximum(100)
        self.eySlider.setSliderPosition(0)
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

    def buildSlider(self, min, max):
        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider.setMinimum(min)
        slider.setMaximum(max)


def getHBox():
    hbox = QtGui.QHBoxLayout()
    hbox.addStretch(0)
    return hbox