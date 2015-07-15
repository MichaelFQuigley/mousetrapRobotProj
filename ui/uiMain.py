#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2
from PyQt4 import QtGui
from PyQt4 import Qt
from imgToQimg import toQImage
import time
sys.path.insert(0, '../imageTransform')
import imageTransform
sys.path.insert(0, '../objectDetection')
import objectDetection


class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        imageWidget = QtGui.QLabel()
        self.setCentralWidget(imageWidget)

        bigimg = cv2.imread('../img/mousetraps.jpg', cv2.IMREAD_COLOR)
        img = cv2.resize(bigimg, (0, 0), fx=0.5, fy=0.5)
        start = time.time()
        img2 = objectDetection.filter(img, (3, 3, 143), (94, 255, 255))
        print("img2")
        print(img2)
        img3 = objectDetection.postProcess(img2)
        print("img3")
        print(img3)
        pts = np.array(eval("[(869, 229), (1842, 238), (2613, 1396), (67, 1407)]"), dtype="float32")
        img4 = imageTransform.four_point_transform(img3, pts)
        imagePixmap = QtGui.QPixmap.fromImage(toQImage(img4))
        scaledPixmap = imagePixmap.scaled(imageWidget.size())
        imageWidget.setScaledContents(True)
        imageWidget.setPixmap(scaledPixmap)
        total = time.time() - start
        print("Time to load and translate picture was 1/{} seconds".format(1.0 / total))

        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.showMaximized()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
