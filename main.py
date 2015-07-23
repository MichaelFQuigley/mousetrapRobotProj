#! /usr/bin/python

from __future__ import division
import cv2
import cameras
import transform
import ui
import sys
from os import path
from PyQt4 import QtCore, QtGui
import time

class Loop(QtCore.QObject):
    image_ready = QtCore.pyqtSignal(object, object)

    @QtCore.pyqtSlot()
    def process_camera_frames(self):
        while True:
            frame = cameras.read()
            if frame is None:
                time.sleep(.25)
            else:
                self.image_ready.emit(frame, transform.bitmap_from_image(frame))
            time.sleep(.25)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    cameras.init(1024)
    if cameras.detected > 0:
        cameras.VideoCapture(0)
    else:
        cameras.VideoCapture(path.join('img', 'mousetraps.jpg'))
    main = ui.MainWindow()
    thread = QtCore.QThread()
    work = Loop()
    work.image_ready.connect(main.on_image_ready)
    work.moveToThread(thread)
    thread.started.connect(work.process_camera_frames)
    thread.finished.connect(app.exit)
    thread.start()
    main.show()
    sys.exit(app.exec_())
