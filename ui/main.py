import cameras
from PyQt4 import QtCore, QtGui
import numpy as np
from functools import partial
from os import path
from sliders import SlidersDialog
import cv2
from SubQLabel import SubQLabel
import settings
import path as pth
from transform import as_pixmap


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.processed = SubQLabel()
        self.raw = SubQLabel()
        self.imageParams = {}
        self.setWindowTitle('Mousetrap Navigator')
        self.setWindowIcon(QtGui.QIcon(path.join('img', 'mousetrap.png')))
        self.top_left = (334, 87)
        self.top_right = (707, 96)
        self.bottom_right = (998, 535)
        self.bottom_left = (46, 536)
        self.calibration_corner = 0
        self.initializing = True
        self.map_sliders = SlidersDialog(self, 'maze')
        self.bot_sliders = SlidersDialog(self, 'bot')

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
        init_map = QtGui.QAction(QtGui.QIcon('Init Map'), 'Init Map', self)
        init_map.setShortcut('Ctrl+I')
        init_map.setStatusTip('Map image initialization settings')
        init_map.triggered.connect(self.show_map_sliders)
        initMenu.addAction(init_map)

        init_bot = QtGui.QAction(QtGui.QIcon('Init Bot'), 'Init Bot', self)
        init_bot.setShortcut('Ctrl+B')
        init_bot.setStatusTip('Bot image initialization settings')
        init_bot.triggered.connect(self.show_bot_sliders)
        initMenu.addAction(init_bot)

        menu.addMenu(initMenu)

    def init_central_widget(self):
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)

        hbox.addWidget(self.raw)

        hbox.addWidget(self.processed)

        main_box = QtGui.QHBoxLayout()
        main_box.addStretch(1)
        main_box.addLayout(hbox)
        widget.setLayout(main_box)

    def on_image_ready(self, orig, new):
        orig_pixmap = as_pixmap(orig)
        self.raw.setPixmap(orig_pixmap)
        if self.initializing:
            settings.maze['top_left'] = (0, 0)
            settings.maze['top_right'] = (orig_pixmap.width() - 1, 0)
            settings.maze['bottom_right'] = (orig_pixmap.width() - 1, orig_pixmap.height() - 1)
            settings.maze['bottom_left'] = (0, orig_pixmap.height() - 1)
            self.initializing = False
        self.processed.setPixmap(as_pixmap(new))

    @QtCore.pyqtSlot(int, int)
    def set_bot_pos(self, x, y):
        print "set_bot_pos called with ({}, {})".format(x, y)
        settings.bot_position = (x, y)

    @QtCore.pyqtSlot(int, int)
    def set_goal_pos(self, x, y):
        print "set_goal_pos called with ({}, {})".format(x, y)
        settings.goal_position = (x, y)
#        settings.path_length, settings.robot_path = path.find_path(self.processed)

    @QtCore.pyqtSlot()
    def show_map_sliders(self):
        self.map_sliders.set_raw(cameras.last)
        self.map_sliders.exec_()

    @QtCore.pyqtSlot()
    def show_bot_sliders(self):
        self.bot_sliders.set_raw(cameras.last)
        self.bot_sliders.exec_()

    # sets a corner point for image translation. cycles through points
    @QtCore.pyqtSlot(int, int)
    def points_changed(self, x, y):
        self.calibration_corner %= 4
        c = self.calibration_corner
        print "Setting point: c = {}. Pt: ({}, {})".format(c, x, y)
        if c == 0:
            settings.maze['top_left'] = (x, y)
        elif c == 1:
            settings.maze['top_right'] = (x, y)
        elif c == 2:
            settings.maze['bottom_right'] = (x, y)
        elif c == 3:
            settings.maze['bottom_left'] = (x, y)
        self.calibration_corner += 1
