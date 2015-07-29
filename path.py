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

def get_map(img):
    """
    Get map as a NumPy array.
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return np.array(img_gray)

def threshold_img(gray_img):
    """
    Make image black and white (no grays).
    """
    img_thresh = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return np.array(img_thresh[1])


def display_image(window_name, img):
    window = cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)


def path_test():

    img = read_image("processed.png")

    h = len(img)
    w = len(img[0])

    print "Resizing map..."
    start_time = time.time()
    #dilated_map = preprocessing.dilate_map(the_map)
    small_img = cv2.resize(img, (w//2,h//2), interpolation = cv2.INTER_AREA)
    print img.shape
    print small_img.shape
    img = small_img
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))



    the_map = get_map(img)
    the_map = threshold_img(the_map)

    h = len(img)
    w = len(img[0])
    origin = (h // 7 // 2, w // 3 // 2 * 5)
    dest = (h // 7 // 2 * 13, w // 3 // 2 * 3)

    

    print "Dilating map..."
    start_time = time.time()
    dilated_map = preprocessing.dilate_map(the_map)
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    print "Computing weights..."
    start_time = time.time()
    weights = preprocessing.compute_map_weights(dilated_map)
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    print "Computing path..."
    start_time = time.time()
    path_length, robot_path = path_finder.find_path(dilated_map, origin, dest, weights)
    waypoints = path_finder.sample_path(robot_path, 10)
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))


    print "Creating image..."
    start_time = time.time()

    # Convert weights to an image that can be displayed
    weights_img = preprocessing.create_weights_image(weights)

    # Create diplay image with obstacles, weights, etc.
    display_img = preprocessing.create_display_image(the_map, dilated_map, weights_img)

    # Draw path on image
    preprocessing.draw_path(display_img, origin, dest, waypoints)
    
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    # Show images for all steps
    #display_image("Map", the_map)
    #display_image("Dilation", dilated_map)
    display_image("Weights", weights_img)
    display_image("Path", display_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()




path_test()
