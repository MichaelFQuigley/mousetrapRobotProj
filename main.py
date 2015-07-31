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
import cv2
import robotBluetooth
import signal
from numpy import sqrt

robot = robotBluetooth.BTPeripheral()
settings.robot = robot

def sigint_handler(*args):
    settings.running = False

class Loop(QtCore.QObject):
    image_ready = QtCore.pyqtSignal(object, object)
    command_ready = QtCore.pyqtSignal(object, object)
    interval_sec  = 0.04 
    last_time     = time.time()

    @QtCore.pyqtSlot()
    def process_camera_frames(self):
        while settings.running:
            if not settings.processingPath:
                frame = cameras.read()
                if frame is None:
                    time.sleep(.25)
                else:
                    if settings.track_bot:
                        if settings.maze['image'] is None:
                            settings.maze['image'] = transform.raw_to_map(frame, settings.maze, QtCore.Qt.white)
                        settings.bot_front['image'] = transform.raw_to_map(frame, settings.bot_front, QtCore.Qt.red)
                        settings.bot_back['image'] = transform.raw_to_map(frame, settings.bot_back, QtCore.Qt.green)
                        position, front = tracker.get_bot_info()
                        settings.bot_position = position
                        # img = cv2.cvtColor(settings.maze['image'], cv2.COLOR_GRAY2BGR)
                        processed = transform.overlay(settings.maze['image'], transform.draw_bot(position, front))
                        current_time = time.time()
                        if settings.robo_go and abs(current_time - self.last_time) >= self.interval_sec:
                            dist_thresh = 0.3
                            if distance(settings.small_goal, settings.bot_position) < dist_thresh:
                                if not settings.path_q.empty():
                                    settings.small_goal = settings.path_q.get()
                                    print "small goal: " + str(settings.small_goal)
                                    print "position: " + str(position)
                                else:
                                    settings.robo_go = False
                                    robot.victory_dance()
                            robot.follow_command(position, front, settings.small_goal)
                    else:
                        processed = transform.raw_to_map(frame, settings.maze)
                    self.image_ready.emit(frame, processed)
        QtGui.qApp.quit()


def distance(a, b):
    return pixels_to_feet(sqrt(((a[0] - b[0])**2) + ((b[1] - a[1])**2)))


def pixels_to_feet(pixels):
    pixels_per_foot = settings.bot_front['image'].shape[1] / settings.maze_length
    return pixels / pixels_per_foot


class RobotLoop(QtCore.QObject):
    @QtCore.pyqtSlot()
    def read_command(self):
        global robot
        while settings.running:
            robot.read()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    app = QtGui.QApplication(sys.argv)
    cameras.init()
    print cameras.detected
    if cameras.detected > 0 and False:
        cameras.VideoCapture(cameras.detected - 1)
    else:
        cameras.VideoCapture(path.join('img', 'mousetraps.jpg'))
    main = ui.MainWindow()
    main.raw.right_click.connect(main.points_changed)
    main.processed.left_click.connect(main.set_bot_pos)
    main.processed.right_click.connect(main.set_goal_pos)
    thread = QtCore.QThread()
    robot_thread = QtCore.QThread()
    work = Loop()
    work.image_ready.connect(main.on_image_ready)
    work.image_ready.connect(main.map_sliders.get_image)
    work.image_ready.connect(main.bot_front_sliders.get_image)
    work.image_ready.connect(main.bot_back_sliders.get_image)
    work.command_ready.connect(robot.follow_command)
    work.moveToThread(thread)
    robot_loop = RobotLoop()
    robot_loop.moveToThread(robot_thread)
    thread.started.connect(work.process_camera_frames)
    thread.finished.connect(app.exit)
    thread.start()
    main.show()
    sys.exit(app.exec_())
