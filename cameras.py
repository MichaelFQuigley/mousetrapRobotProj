import cv2

selected = -1
detected = 0
cap = None

def init():
    global detected
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
