from __future__ import division
import cv2

selected = -1
detected = 0
cap = None
last = None
max_size = None

def init(desired_size):
    global detected, max_size
    max_size = desired_size
    good = True
    while good:
        cap = cv2.VideoCapture(detected)
        if cap.isOpened():
            detected = detected + 1
        else:
            good = False
        cap.release()


def VideoCapture(ind):
    global cap, selected
    if ind == selected:
        return cap

    selected = ind
    old = cap
    cap = cv2.VideoCapture(selected)
    if old is not None:
        old.release()
    return cap

def read():
    global max_size
    frame = read_frame()
    if frame is None:
        return None

    if max_size is not None:
        h, w, c = frame.shape
        ratio = max_size / max(h, w)
        if ratio < 1:
            frame = cv2.resize(frame, (int(w*ratio),int(h*ratio)), interpolation = cv2.INTER_AREA)

    return frame

def read_frame():
    global last
    if cap.isOpened():
        ret, frame = cap.read()
        if frame is None:
            return last
        else:
            last = frame
            return frame
