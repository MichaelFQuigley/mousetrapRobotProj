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
            if cameras.cap.isOpened():
                ret, frame = cameras.cap.read()
                if frame is not None:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    h, w = gray.shape
                    ratio = 640 / max(h, w)
                    if ratio < 1:
                        gray = cv2.resize(gray, (0,0), fx=ratio, fy=ratio)
                    self.image_ready.emit(gray, transform.bitmap_from_image(gray))
            else:
                time.sleep(.5)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    cameras.init()
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
