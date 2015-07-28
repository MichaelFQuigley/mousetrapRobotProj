from __future__ import division

import cv2
import numpy as np
#import cameras
import time

from os import path
from Queue import Queue

import pathFinder



def read_image(file_name):
    """
    Get color image.
    """
    #cameras.init(1024)
    #cameras.VideoCapture(path.join("img", "map-small.png"))
    #img = cameras.read()
    #print img
    return cv2.imread(path.join("img", file_name), cv2.IMREAD_COLOR)

def get_map(img):
    """
    Get map as a NumPy array.
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img2 = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return np.array(img_gray)


def get_dilation_kernel(grid):
    """
    Based on robot size...
    """
    grid_width = len(grid[0])
    grid_height = len(grid)
    
    map_width = 9.0     # in feet
    map_height = 14.0   # in feet

    robot_radius = 0.35 # in feet -> ~ 4.2 inches

    kernel_width = robot_radius * grid_width / map_width
    kernel_height = robot_radius * grid_height / map_height

    print "kernel width:", kernel_width
    print "kernel height:", kernel_height
    
    return np.ones((kernel_height, kernel_width), np.uint8)

def dilate_map(grid):
    """
    Based on robot size...
    """
    kernel = get_dilation_kernel(grid)
    return cv2.dilate(grid, kernel, iterations = 1)


def display_image(window_name, img):
    window = cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)

def path_test():

    img = read_image("processed-small.png")
    the_map = get_map(img)

    h = len(the_map)
    w = len(the_map[0])
    origin = (h // 7 // 2, w // 3 // 2 * 5)
    dest = (h // 7 // 2 * 13, w // 3 // 2 * 3)

    print "dilating..."
    start_time = time.time()
    dilated_map = dilate_map(the_map)
    #dilated_map = the_map
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    dilated_map = cv2.threshold(dilated_map, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    print "computing weights..."
    start_time = time.time()
    weights = pathFinder.compute_map_weights(dilated_map)
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    print "computing path..."
    start_time = time.time()
    path_length, robot_path = pathFinder.find_path(dilated_map, origin, dest, weights)
    end_time = time.time()
    print("path lenth: " + str(path_length))
    print("Elapsed time: " + str(end_time - start_time))

    print "done!"
    
    # Draw path on image
    waypoints = pathFinder.sample_path(robot_path)
    for cell in waypoints:
        red = [0, 0, 255] # BGR
        img[cell[0]][cell[1]] = red
        img[cell[0] - 1][cell[1]] = red
        img[cell[0] + 1][cell[1]] = red
        img[cell[0]][cell[1] - 1] = red
        img[cell[0]][cell[1] + 1] = red
    
    #display_image("Map", the_map)
    display_image("Dilation", dilated_map)
    display_image("Weights", weights)
    display_image("Path", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

path_test()
