import cameras
from PyQt4 import QtCore, QtGui
import numpy as np
from functools import partial
from os import path
from SlidersWidget import SlidersWidget
import cv2
import SubQLabel


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.imageParams = {}
        self.slidersWidget = SlidersWidget(self)
        self.setWindowTitle('Mousetrap Navigator')
        self.setWindowIcon(QtGui.QIcon(path.join('img', 'mousetrap.png')))
        self.top_left = (334, 87)
        self.top_right = (707, 96)
        self.bottom_right = (998, 535)
        self.bottom_left = (46, 536)
        self.calibration_corner = 0
        self.initializing = True

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
        # hbox.addWidget(self.slidersWidget)

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
            self.top_left = (0, 0)
            self.top_right = (orig_pixmap.width() - 1, 0)
            self.bottom_right = (orig_pixmap.width() - 1, orig_pixmap.height() - 1)
            self.bottom_left = (0, orig_pixmap.height() - 1)
            self.initializing = False
        self.processed.setPixmap(as_pixmap(new))

    def getImageParams(self):
        self.imageParams = {'mins': (self.slidersWidget.rMinSlider.value(),
                                     self.slidersWidget.gMinSlider.value(),
                                     self.slidersWidget.bMinSlider.value()),
                            'maxes': (self.slidersWidget.rMaxSlider.value(),
                                      self.slidersWidget.gMaxSlider.value(),
                                      self.slidersWidget.bMaxSlider.value()),
                            'blur': 0,
                            'dilation': (self.slidersWidget.dySlider.value(),
                                         self.slidersWidget.dxSlider.value()),
                            'erosion': (self.slidersWidget.eySlider.value(),
                                        self.slidersWidget.exSlider.value()),
                            'pts': np.array([self.top_left, self.top_right,
                                             self.bottom_right, self.bottom_left], dtype="float32")
               }
        return self.imageParams

    def show_sliders(self):
        self.popup = popup(self, self.slidersWidget)
        self.popup.show()

    # sets a corner point for image translation. cycles through points
    @QtCore.pyqtSlot(int, int)
    def points_changed(self, x, y):
        print "Setting Points..."
        self.calibration_corner %= 4
        c = self.calibration_corner
        print "c = {}".format(c)
        if c == 0:
            self.top_left = (x, y)
        elif c == 1:
            self.top_right = (x, y)
        elif c == 2:
            self.bottom_right = (x, y)
        elif c == 3:
            self.bottom_left = (x, y)
        self.calibration_corner += 1
        print "points are now {}".format(self.getImageParams()['pts'])


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


class popup(QtGui.QWidget):
    def __init__(self, parent = None, widget=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QGridLayout(self)
        layout.addWidget(widget)
        # adjust the margins or you will get an invisible, unintended border
        layout.setContentsMargins(10, 10, 10, 10)
        # need to set the layout
        self.setLayout(layout)
        self.adjustSize()
        # tag this widget as a popup
        self.setWindowFlags(QtCore.Qt.Popup)
        # calculate the botoom right point from the parents rectangle
        point = widget.rect().bottomRight()
        # map that point as a global position
        global_point = widget.mapToGlobal(point)
        # by default, a widget will be placed from its top-left corner, so
        # we need to move it to the left based on the widgets width
        # self.move(global_point - QtCore.QPoint(self.width(), 0))
