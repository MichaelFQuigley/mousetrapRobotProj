#! /usr/bin/python

import cv2
import cameras
import transform
import ui
import sys
from PyQt4 import QtCore, QtGui

class Loop(QtCore.QObject):
    image_ready = QtCore.pyqtSignal(object, object)

    @QtCore.pyqtSlot()
    def process_camera_frames(self):
        while True:
            ret, frame = cameras.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.image_ready.emit(frame, transform.bitmap_from_image(gray))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    cameras.init()
    cameras.VideoCapture()
    main = ui.MainWindow()
    thread = QtCore.QThread()
    work = Loop()
    work.image_ready.connect(main.on_image_ready);
    work.moveToThread(thread)
    thread.started.connect(work.process_camera_frames)
    thread.finished.connect(app.exit)
    thread.start()
    main.show()
    sys.exit(app.exec_())
