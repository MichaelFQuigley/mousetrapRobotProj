import cameras
from PyQt4 import QtCore, QtGui, Qt
import numpy as np
from functools import partial
from os import path
from sliders import SlidersDialog
import cv2
from SubQLabel import SubQLabel
import settings
import path as pth
from transform import as_pixmap, resize_image
from camera_dialog import CameraDialog

def track_bot():
    settings.track_bot = not settings.track_bot


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
        self.bot_front_sliders = SlidersDialog(self, 'bot_front')
        self.bot_back_sliders = SlidersDialog(self, 'bot_back')
        self.camera_dialog = CameraDialog(self)

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

        init_bot_front = QtGui.QAction(QtGui.QIcon('Init Bot Front'), 'Init Bot Front', self)
        init_bot_front.setShortcut('Ctrl+B')
        init_bot_front.setStatusTip('Bot image initialization settings')
        init_bot_front.triggered.connect(self.show_bot_front_sliders)
        initMenu.addAction(init_bot_front)

        init_bot_back = QtGui.QAction(QtGui.QIcon('Init Bot Back'), 'Init Bot Back', self)
        init_bot_back.setShortcut('Ctrl+B')
        init_bot_back.setStatusTip('Bot image initialization settings')
        init_bot_back.triggered.connect(self.show_bot_back_sliders)
        initMenu.addAction(init_bot_back)

        init_camera = QtGui.QAction(QtGui.QIcon('Init Camera'), 'Init Camera', self)
        init_camera.setShortcut('Ctrl+C')
        init_camera.setStatusTip('Set camera height and horizontal distance from maze')
        init_camera.triggered.connect(self.show_camera_init)
        initMenu.addAction(init_camera)

        init_track_bot = QtGui.QAction(QtGui.QIcon('Track Bot'), 'Track Bot', self)
        init_track_bot.setShortcut('Ctrl+T')
        init_track_bot.setStatusTip('Begin tracking bot position')
        init_track_bot.triggered.connect(track_bot)
        initMenu.addAction(init_track_bot)

        reset_video = QtGui.QAction(QtGui.QIcon('replay video'), 'replay video', self)
        reset_video.triggered.connect(partial(cameras.VideoCapture, 'output.avi'))
        initMenu.addAction(reset_video)

        menu.addMenu(initMenu)

    def show_camera_init(self):
        camheight, okh = QtGui.QInputDialog.getDouble(self, 'Camera', 'Enter Camera Height (in feet)')
        camdist, okd = QtGui.QInputDialog.getDouble(self, 'Camera', 'Enter Horizontal distance from camera to maze (in feet)')
        if okh and okd:
            settings.camera_height = camheight
            settings.camera_distance = camdist
            print str(camheight) + " " + str(camdist)

    def init_central_widget(self):
        widget = QtGui.QWidget()
        self.setCentralWidget(widget)

        grid = QtGui.QGridLayout()
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 1)

        grid.addWidget(self.raw, 0, 0)

        grid.addWidget(self.processed, 0, 1)

        main_box = QtGui.QHBoxLayout()
        main_box.addLayout(grid)
        widget.setLayout(main_box)

    def on_image_ready(self, orig, new):
        orig_pixmap = as_pixmap(orig)
        self.raw.setPixmap(orig_pixmap)
        if self.initializing:
            for key in settings.bot, settings.maze:
                settings.top_left = (0, 0)
                settings.top_right = (orig_pixmap.width() - 1, 0)
                settings.bottom_right = (orig_pixmap.width() - 1, orig_pixmap.height() - 1)
                settings.bottom_left = (0, orig_pixmap.height() - 1)

            self.initializing = False

        pm = as_pixmap(new)
        cpm = QtGui.QPixmap(pm.size())
        cpm.fill(QtCore.Qt.red)
        cpm.setMask(pm.createMaskFromColor(QtCore.Qt.transparent))
        self.processed.setPixmap(pm)

    def set_bot_pos(self, x, y):
        print "set_bot_pos called with ({}, {})".format(x, y)
        settings.bot_position = (x, y)

    def set_goal_pos(self, x, y):
        print "set_goal_pos called with ({}, {})".format(x, y)
        settings.goal_position = (x, y)
#        settings.path_length, settings.robot_path = path.find_path(self.processed)

    @QtCore.pyqtSlot()
    def show_map_sliders(self):
        self.map_sliders.exec_()

    @QtCore.pyqtSlot()
    def show_bot_front_sliders(self):
        self.bot_front_sliders.exec_()

    @QtCore.pyqtSlot()
    def show_bot_back_sliders(self):
        self.bot_back_sliders.exec_()

    # sets a corner point for image translation. cycles through points
    def points_changed(self, x, y):
        self.calibration_corner %= 4
        c = self.calibration_corner
        print "Setting point: c = {}. Pt: ({}, {})".format(c, x, y)
        if c == 0:
            settings.top_left = (x, y)
        elif c == 1:
            settings.top_right = (x, y)
        elif c == 2:
            settings.bottom_right = (x, y)
        elif c == 3:
            settings.bottom_left = (x, y)
        self.calibration_corner += 1
