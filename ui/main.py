import cameras
from PyQt4 import QtCore, QtGui
from PIL import Image, ImageQt
import numpy as np
from functools import partial
from os import path
from sliders import SlidersDialog
import cv2

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.sliders = SlidersDialog(self)
        self.setWindowTitle('Mousetrap Navigator')
        self.setWindowIcon(QtGui.QIcon(path.join('img', 'mousetrap.png')))

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

        self.raw = QtGui.QLabel()
        hbox.addWidget(self.raw)

        self.processed = QtGui.QLabel()
        hbox.addWidget(self.processed)

        mainBox = QtGui.QHBoxLayout()
        mainBox.addStretch(1)
        mainBox.addLayout(hbox)
        widget.setLayout(mainBox)

    def on_image_ready(self, orig, new):
        self.raw.setPixmap(as_pixmap(orig))
        self.processed.setPixmap(as_pixmap(new))

    @QtCore.pyqtSlot()
    def show_sliders(self):
        self.sliders.exec_()

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
