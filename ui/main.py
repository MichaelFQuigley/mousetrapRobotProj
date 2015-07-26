import cameras
from PyQt4 import QtCore, QtGui
import numpy as np
from functools import partial
from os import path
from sliders import SlidersDialog
import cv2
import SubQLabel
from settings import settings

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.imageParams = {}
        self.setWindowTitle('Mousetrap Navigator')
        self.setWindowIcon(QtGui.QIcon(path.join('img', 'mousetrap.png')))
        self.top_left = (334, 87)
        self.top_right = (707, 96)
        self.bottom_right = (998, 535)
        self.bottom_left = (46, 536)
        self.calibration_corner = 0
        self.initializing = True
        self.sliders = SlidersDialog(self)

        self.init_menubar()
        self.init_central_widget()

    def init_menubar(self):
        menu = self.menuBar()

        exit = QtGui.QAction(QtGui.QIcon('&Exit'), '&Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.triggered.connect(QtGui.qApp.quit)

        fileMenu = menu.addMenu('&File')
        fileMenu.addAction(exit)

        ag = QtGui.QActionGroup(self, exclusive=True)
        cameraMenu = menu.addMenu('Capture')
        for c in range(cameras.detected):
            a = QtGui.QAction('Camera %d' % c, self, checkable=True)
            if c == cameras.detected - 1:
                a.setChecked(True)
            a.triggered.connect(partial(cameras.VideoCapture, c))
            cameraMenu.addAction(ag.addAction(a))
        menu.addMenu(cameraMenu)

        initMenu = menu.addMenu('&Init')
        init = QtGui.QAction(QtGui.QIcon('&Init'), '&Init', self)
        init.setShortcut('Ctrl+I')

        init.setStatusTip('Image initialization settings')
        init.triggered.connect(self.show_sliders)
        initMenu.addAction(init)
        menu.addMenu(initMenu)


    def init_central_widget(self):
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)

        self.raw = SubQLabel.SubQLabel()
        hbox.addWidget(self.raw)

        self.processed = QtGui.QLabel()
        hbox.addWidget(self.processed)

        mainBox = QtGui.QHBoxLayout()
        mainBox.addStretch(1)
        mainBox.addLayout(hbox)
        widget.setLayout(mainBox)

    def on_image_ready(self, orig, new):
        orig_pixmap = as_pixmap(orig)
        self.raw.setPixmap(orig_pixmap)
        if self.initializing:
            settings.top_left = (0, 0)
            settings.top_right = (orig_pixmap.width() - 1, 0)
            settings.bottom_right = (orig_pixmap.width() - 1, orig_pixmap.height() - 1)
            settings.bottom_left = (0, orig_pixmap.height() - 1)
            self.initializing = False
        self.processed.setPixmap(as_pixmap(new))

    @QtCore.pyqtSlot()
    def show_sliders(self):
        self.sliders.exec_()

    # sets a corner point for image translation. cycles through points
    @QtCore.pyqtSlot(int, int)
    def points_changed(self, x, y):
        print "Setting Points..."
        self.calibration_corner %= 4
        c = self.calibration_corner
        print "c = {}".format(c)
        if c == 0:
            settings.top_left = (x, y)
        elif c == 1:
            settings.top_right = (x, y)
        elif c == 2:
            settings.bottom_right = (x, y)
        elif c == 3:
            settings.bottom_left = (x, y)
        self.calibration_corner += 1

def as_pixmap(frame):
    gray = False
    if len(frame.shape) == 2:
        gray = True
    if gray:
        img = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    else:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    qt_image = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(qt_image)
