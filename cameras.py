from __future__ import division
import cv2
import settings

selected = -1
detected = 0
cap = None
last = None


def init():
    global detected
    good = True
    while good:
        cap = cv2.VideoCapture(detected)
        if cap.isOpened():
            detected += 1
        else:
            good = False
        cap.release()


def VideoCapture(ind):
    global cap
    frame_buf_size = 5
    if ind == selected:
        return cap

    cap = cv2.VideoCapture(ind)

def read():
    frame = read_frame()
    if frame is None:
        return None

    if settings.image_height is not None:
        h, w, c = frame.shape
        ratio = settings.image_height / max(h, w)
        if ratio < 1:
            frame = cv2.resize(frame, (int(w * ratio), int(h * ratio)), interpolation=cv2.INTER_AREA)

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
