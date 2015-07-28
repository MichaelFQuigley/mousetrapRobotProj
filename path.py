from __future__ import division

import cv2
import numpy as np
import time

from os import path
from Queue import Queue

import pathFinder


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


def color_pixel(img, row, col, color):
    height = len(img)
    width = len(img[0])
    if row >= 0 and row < height and col >= 0 and col < width:
        img[row][col] = color

def mark_location(img, coordinates, color):
    # Draw a cross
    row = coordinates[0]
    col = coordinates[1]
    color_pixel(img, row, col, color) 
    color_pixel(img, row - 1, col, color) 
    color_pixel(img, row + 1, col, color) 
    color_pixel(img, row, col - 1, color) 
    color_pixel(img, row, col + 1, color) 
    
def display_image(window_name, img):
    window = cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)


def path_test():

    img = read_image("processed-small.png")
    the_map = get_map(img)
    the_map = threshold_img(the_map)

    h = len(img)
    w = len(img[0])
    origin = (h // 7 // 2, w // 3 // 2 * 5)
    dest = (h // 7 // 2 * 13, w // 3 // 2 * 3)

    print "dilating..."
    start_time = time.time()
    dilated_map = dilate_map(the_map)
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    print "Computing weights..."
    start_time = time.time()
    weights = pathFinder.compute_map_weights(dilated_map)
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    print "Computing path..."
    start_time = time.time()
    path_length, robot_path = pathFinder.find_path(dilated_map, origin, dest, weights)
    end_time = time.time()
    print("path lenth: " + str(path_length))
    print("Elapsed time: " + str(end_time - start_time))


    # Convert weights to an image that can be displayed
    weights_img = np.zeros(weights.shape, dtype = np.uint8)
    max_weight = 0
    for row in range(h):
        for col in range(w):
            if weights[row][col] > max_weight:
                max_weight = weights[row][col]
    for row in range(h):
        for col in range(w):
            weights_img[row][col] = int(weights[row][col] / float(max_weight) * 255)

    # Create diplay image with obstacles, weights, etc.
    display = np.copy(img)
    obstacle_color = [255, 255, 255]
    dilation_color = [194, 32, 0]
    for row in range(h):
        for col in range(w):
            if the_map[row][col] != 0:
                display[row][col] = obstacle_color
            elif dilated_map[row][col] != 0:
                display[row][col] = dilation_color
            else: # weights
                #x = weights_img[row][col] * 0.75
                #x = weights_img[row][col] ** 0.5 * (255 ** 0.5) * 0.5
                x = weights_img[row][col]
                display[row][col] = [x, x // 3, 0] 

    # Draw path on image
    waypoints = pathFinder.sample_path(robot_path, 10)
    for cell in waypoints:
        red = [0, 0, 255] # BGR
        mark_location(display, cell, red)

    # Mark origin and destination
    mark_location(display, origin, [0, 255, 0])
    mark_location(display, dest, [0, 255, 0])
    

    # Show images for all steps
    #display_image("Map", the_map)
    #display_image("Dilation", dilated_map)
    #display_image("Weights", weights_img)
    display_image("Path", display)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

path_test()
