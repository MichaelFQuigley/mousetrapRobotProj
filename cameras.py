import cv2

selected = 0
detected = 0
cap = None

def init():
    global detected
    good = True
    while good:
        cap = cv2.VideoCapture(detected)
        if cap.isOpened():
            detected = detected + 1
            good = False
        cap.release()

def VideoCapture():
    global cap
    if cap is not None:
        cap.release()
    cap = cv2.VideoCapture(selected)
    return cap
