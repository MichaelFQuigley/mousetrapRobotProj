import cameras
from PyQt4 import QtCore, QtGui
from PIL import ImageQt
import numpy as np
import Image
from functools import partial
from os import path

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Mousetrap Navigator')
        self.setWindowIcon(QtGui.QIcon(path.join('img','mousetrap.png')))

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
            if c == 0:
                a.setChecked(True)
            a.triggered.connect(partial(cameras.VideoCapture, c))
            cameraMenu.addAction(ag.addAction(a))
        menu.addMenu(cameraMenu)

    def init_central_widget(self):
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)

        self.raw = QtGui.QLabel()
        hbox.addWidget(self.raw)

        self.processed = QtGui.QLabel()
        hbox.addWidget(self.processed)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        widget.setLayout(vbox)

    def on_image_ready(self, orig, new):
        self.raw.setPixmap(as_pixmap(orig))
        self.processed.setPixmap(as_pixmap(new))

def as_pixmap(frame):
    pil_image = Image.fromarray(np.uint8(frame))
    qt_image = ImageQt.ImageQt(pil_image)
    return QtGui.QPixmap.fromImage(qt_image)
