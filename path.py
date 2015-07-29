from __future__ import division

import cv2
import numpy as np
import time

from os import path
from Queue import Queue

import settings
import pathFinder as path_finder
from pathFinder import preprocessing


def read_image(file_name):
    """
    Get color image.
    """
    return cv2.imread(path.join("img", file_name), cv2.IMREAD_COLOR)


def display_image(window_name, img):
    """
    Display 
    """
    window = cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)


def path_test():

    img = read_image("processed.png")

    h = len(img)
    w = len(img[0])

    origin = (h // 7 // 2, w // 3 // 2 * 5)
    dest = (h // 7 // 2 * 13, w // 3 // 2 * 3)

    path, display_img = path_finder.find_path_from_image(img, origin, dest)

    # Show images for all steps
    #display_image("Map", the_map)
    #display_image("Dilation", dilated_map)
    #display_image("Weights", weights_img)
    display_image("Path", display_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

path_test()
