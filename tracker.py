import cv2
import settings
import numpy as np


def find_the_two_objects(img):
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    largest = None
    second = None

    if len(contours) > 0:
        lcont = contours[0]
        scont = lcont
        largest_area = 0
        second_largest_area = 0
        for contour in contours:
            a = cv2.contourArea(contour, False)
            if a > largest_area:
                second_largest_area = largest_area
                largest_area = a
                scont = lcont
                lcont = contour
            elif a > second_largest_area:
                second_largest_area = a
                scont = contour

        largest, radius = cv2.minEnclosingCircle(lcont)
        second, r = cv2.minEnclosingCircle(scont)

    return second, largest


def get_bot_info():
    front, back = find_the_two_objects(settings.bot_front['image'])
    # back = find_the_object(settings.bot_back['image'])
    if front is None or back is None:
        print "Tracking Error"
        if front is None and back is None:
            print "lost the bot"
            return None, None
        if front is None:
            print "lost the front"
            front = back
        else:
            print "lost the back"
            back = front
    v_adj = (settings.bot_height / settings.camera_height) * (settings.camera_distance + (settings.maze_length * (1 - (front[1] / settings.bot_front['image'].shape[1]))))
    pixels_per_foot = settings.bot_front['image'].shape[1] / settings.maze_length
    midpoint = ((front[0] + back[0]) / 2.0, ((front[1] + back[1]) / 2.0) + (v_adj * pixels_per_foot))
    front = (front[0], front[1] + v_adj * pixels_per_foot)
    return midpoint, front


def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y
    #
    # function find_clockwise(from, to, options) {
    #     var dy = Math.floor(to / 4) - Math.floor(from / 4);
    #     var dx = to % 4 - from % 4;
    #     var target = Math.atan2(dy, dx);
    #     var min = 7;
    #     var dir;
    #     for (var i = 0; i < options.length; i++) {
    #         var o = options[i];
    #         var r = o[0] - target;
    #         if (r < 0)
    #             r += 2 * Math.PI;
    #         if (r < min) {
    #             min = r;
    #             dir = o[1];
    #         }
    #     }
    #     return dir;
    # }