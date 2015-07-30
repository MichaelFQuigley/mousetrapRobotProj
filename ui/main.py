import cameras
from PyQt4 import QtCore, QtGui, Qt
import numpy as np
from functools import partial
from os import path
from sliders import SlidersDialog
import cv2
from SubQLabel import SubQLabel
import settings
from transform import as_pixmap, resize_image
from camera_dialog import CameraDialog
import robotBluetooth
import pathFinder


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

        save_settings = QtGui.QAction(QtGui.QIcon('save settings'), 'save settings', self)
        save_settings.setShortcut('Ctrl+S')
        save_settings.triggered.connect(partial(settings.save, 'settings.pyb'))
        initMenu.addAction(save_settings)

        load_settings_action = QtGui.QAction(QtGui.QIcon('load settings'), 'load settings', self)
        load_settings_action.setShortcut('Ctrl+L')
        load_settings_action.triggered.connect(self.load_settings)
        initMenu.addAction(load_settings_action)
        menu.addMenu(initMenu)

        redbot_menu = menu.addMenu("Redbot")
        redbot_connect_action = QtGui.QAction(QtGui.QIcon('connect'), 'connect', self)
        redbot_connect_action.triggered.connect(self.redbot_connect)
        redbot_menu.addAction(redbot_connect_action)

        redbot_go_action = QtGui.QAction(QtGui.QIcon('go'), 'go', self)
        redbot_go_action.triggered.connect(self.redbot_go)
        redbot_menu.addAction(redbot_go_action)

        redbot_revolt_action = QtGui.QAction(QtGui.QIcon('clear revolt'), 'clear revolt', self)
        redbot_revolt_action.triggered.connect(self.redbot_clear_revolt)
        redbot_menu.addAction(redbot_revolt_action)
        menu.addMenu(redbot_menu)

    @QtCore.pyqtSlot()
    def redbot_clear_revolt(self):
        settings.robot.send('-1, -1\n')

    @QtCore.pyqtSlot()
    def redbot_go(self):
        settings.robo_go = not settings.robo_go

    @QtCore.pyqtSlot()
    def redbot_connect(self):
        self.redbot = robotBluetooth.BTPeripheral('/dev/cu.HC-06-DevB')
        try:
            if self.redbot.connect():
                print "robot connected"
            else:
                print "failed to connect"
        except Exception:
            print "robot blew up"

    @QtCore.pyqtSlot()
    def load_settings(self, file_path='settings.pyb'):
        settings.load(file_path)
        bot_back_sliders = self.bot_back_sliders.findChildren(QtGui.QSlider)
        bot_front_sliders = self.bot_front_sliders.findChildren(QtGui.QSlider)
        map_sliders = self.map_sliders.findChildren(QtGui.QSlider)
        for thing, i in {'ey': 0, 'ex': 1, 'dy': 2, 'dx': 3, 'hMin': 4, 'hMax': 5, 'sMin': 6, 'sMax': 7, 'vMin': 8,
                         'vMax': 9}.iteritems():
            bot_back_sliders[i].setSliderPosition(settings.bot_back[thing])
            print thing + ' ' + str(settings.bot_back[thing])
            bot_front_sliders[i].setSliderPosition(settings.bot_front[thing])
            map_sliders[i].setSliderPosition(settings.maze[thing])
            # back_slider = self.bot_back_sliders.findChild(QtGui.QSlider, thing)
            # back_slider.setSliderPosition(settings.bot_back[thing])
            # self.bot_front_sliders.findChild(QtGui.QSlider, thing).setSliderPosition(settings.bot_front[thing])
            # self.map_sliders.findChild(QtGui.QSlider, thing).setSliderPosition(settings.maze[thing])

    def show_camera_init(self):
        camheight, okh = QtGui.QInputDialog.getDouble(self, 'Camera', 'Enter Camera Height (in feet)')
        camdist, okd = QtGui.QInputDialog.getDouble(self, 'Camera',
                                                    'Enter Horizontal distance from camera to maze (in feet)')
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
        points, image = pathFinder.find_path_from_image(settings.maze['image'],
                                                        settings.bot_position, settings.goal_position)
        settings.maze['image'] = image
        settings.path = points

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
