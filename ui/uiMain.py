#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2
from PyQt4 import QtGui
from PyQt4 import Qt
from PyQt4 import QtCore
import time
from ImageWidget import ImageWidget
sys.path.insert(0, '../imageTransform')
import imageTransform
sys.path.insert(0, '../objectDetection')
import objectDetection


class RobotUI(QtGui.QWidget):
    def __init__(self):
        super(RobotUI, self).__init__()
        self.main_layout = QtGui.QVBoxLayout()

        self.initUI()

    def initUI(self):
        # imageWidget = ImageWidget(self)
        # self.setCentralWidget(imageWidget)
        #
        self.model = RobotBrainModel()

        self.slider1 = QtGui.QSlider()
        self.model.add_slider(self.slider1)
        self.main_layout.addWidget(self.slider1)

        self.edit = QtGui.QLineEdit()
        button = QtGui.QPushButton('update model')
        button.clicked.connect(self.on_clicked)
        self.main_layout.addWidget(self.edit)
        self.main_layout.addWidget(button)

        self.setLayout(self.main_layout)

    def on_clicked(self):
        self.model.update_model(int(self.edit.text()), self.slider1)

        # start = time.time()
        # bigimg = cv2.imread('../img/mousetraps.jpg', cv2.IMREAD_COLOR)
        # img = cv2.resize(bigimg, (0, 0), fx=0.5, fy=0.5)
        # params = {}
        # params['image'] = img
        # params['filterMins'] = (3, 3, 143)
        # params['filterMaxs'] = (94, 255, 255)
        # params['dilation'] = (12, 25)
        # params['erosion'] = (4, 4)
        #
        # """
        # img2 = objectDetection.filter(img, (3, 3, 143), (94, 255, 255))
        # print("img2")
        # print(img2)
        # img3 = objectDetection.postProcess(img2, (12, 25), (5, 5))
        # print("img3")
        # print(img3)
        # """
        # pts = self.getPointsForTransform()
        # img = imageWidget.filterImage(params)
        # img4 = imageTransform.four_point_transform(img, pts)
        # imageWidget.showCVImage(img4)
        # total = time.time() - start
        # print("Time to load and translate picture was 1/{} seconds".format(1.0 / total))
        #
        # exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Exit application')
        # exitAction.triggered.connect(self.close)
        #
        # self.statusBar()
        #
        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(exitAction)
        #
        # toolbar = self.addToolBar('Exit')
        # toolbar.addAction(exitAction)
        #
        # self.setGeometry(300, 300, 350, 250)
        # self.setWindowTitle('Main window')
        # self.showMaximized()

    def getPointsForTransform(self):
        return np.array(eval("[(869, 229), (1842, 238), (2613, 1396), (67, 1407)]"), dtype="float32")

class RobotBrainModel(QtGui.QStandardItemModel):
    def __init__(self, *args, **kwargs):
        super(RobotBrainModel, self).__init__(*args, **kwargs)
        self._slider_list = {}
        self.itemChanged.connect(self.on_item_changed)

    def add_slider(self,slider):
        if slider in self._slider_list:
            raise Exception('You cannot link a slider to the model twice')

        item = QtGui.QStandardItem(str(slider.value()))
        self._slider_list[slider] = item
        self.appendRow(item)
        slider.valueChanged.connect(lambda value: self.update_model(value,slider))

    def update_model(self,value,slider):
        if str(value) != self._slider_list[slider].text():
            self._slider_list[slider].setText(str(value))
            print 'update_model: %d'%value

    def on_item_changed(self,item):
        slider = self._slider_list.keys()[self._slider_list.values().index(item)]
        if slider.value() != int(item.text()):
            slider.setValue(int(item.text()))
            print 'on_item_changed: %s'%item.text()

app = QtGui.QApplication(sys.argv)
window = RobotUI()
window.show()

sys.exit(app.exec_())
