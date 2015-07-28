#! /usr/bin/python

from __future__ import division

import cameras
import transform
import ui
import sys
from os import path
from PyQt4 import QtCore, QtGui
import time
import settings
import tracker


class Loop(QtCore.QObject):
    image_ready = QtCore.pyqtSignal(object, object)

    @QtCore.pyqtSlot()
    def process_camera_frames(self):
        while True:
            frame = cameras.read()
            if frame is None:
                time.sleep(.25)
            else:
                if settings.track_bot:
                    if settings.maze['image'] is None:
                        settings.maze['image'] = transform.raw_to_map(frame, settings.maze, QtCore.Qt.white)
                    settings.bot_front['image'] = transform.raw_to_map(frame, settings.bot_front, QtCore.Qt.red)
                    settings.bot_back['image'] = transform.raw_to_map(frame, settings.bot_back, QtCore.Qt.green)
                    position, vector = tracker.get_bot_info()
                    processed = transform.overlay((settings.maze['image'], QtCore.Qt.white),
                                                  (settings.bot_front['image'], QtCore.Qt.red),
                                                  (settings.bot_back['image'], QtCore.Qt.green))
                else:
                    processed = transform.raw_to_map(frame, settings.maze)
                self.image_ready.emit(frame, processed)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    cameras.init()
    print cameras.detected
    if cameras.detected > 0:
        cameras.VideoCapture(cameras.detected - 1)
    else:
        cameras.VideoCapture(path.join('img', 'mousetraps.jpg'))
    main = ui.MainWindow()
    main.raw.right_click.connect(main.points_changed)
    main.processed.left_click.connect(main.set_bot_pos)
    main.processed.right_click.connect(main.set_goal_pos)
    thread = QtCore.QThread()
    work = Loop()
    work.image_ready.connect(main.on_image_ready)
    work.image_ready.connect(main.map_sliders.get_image)
    work.image_ready.connect(main.bot_front_sliders.get_image)
    work.image_ready.connect(main.bot_back_sliders.get_image)
    work.moveToThread(thread)
    thread.started.connect(work.process_camera_frames)
    thread.finished.connect(app.exit)
    thread.start()
    main.show()
    sys.exit(app.exec_())
