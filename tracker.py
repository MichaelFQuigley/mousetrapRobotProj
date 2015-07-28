import cv2
import settings
import numpy as np


def find_the_object(img):
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)

    if len(contours) > 0:
        cnt = contours[0]
        largest_area = 0
        for contour in contours:
            a = cv2.contourArea(contour, False)
            if a > largest_area:
                cnt = contour

        pnt, radius = cv2.minEnclosingCircle(cnt)
    return pnt


def get_bot_info():
    front = find_the_object(settings.bot_front['image'])
    back = find_the_object(settings.bot_back['image'])
    v_adj = (settings.bot_height / settings.camera_height) * (settings.camera_distance + (settings.maze_length * (1 - (front[1] / settings.bot_front['image'].shape[1]))))
    pixels_per_foot = settings.bot_front['image'].shape[1] / settings.maze_length
    midpoint = ((front[0] + back[0]) / 2.0, ((front[1] + back[1]) / 2.0) + (v_adj * pixels_per_foot))
    vector = (front[0] - back[0], front[1] - back[1])
    return midpoint, vector


def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y

