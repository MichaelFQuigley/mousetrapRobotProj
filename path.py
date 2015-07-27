from __future__ import division

import cv2
import numpy as np
import cameras

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


def get_neighbors(row, col, height, width):
        """
        Get 8-adjacent neighbors.
        """
        n = []
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if r != 0 or c != 0:
                    n_row = row + r
                    n_col = col + c
                    if n_row >= 0 and n_row < height and n_col >= 0 and n_col < width:
                        # TODO: ignore blocked cells?
                        n.append((n_row, n_col))
        return n

def compute_map_weights(the_map):

    m = np.copy(the_map) # distance from obstacles
    h = len(the_map)
    w = len(the_map[0])

    print "map size:", h, w

    border = set([])
    for row in range(h):
        for col in range(w):
            if m[row][col] != 255:
                for n in get_neighbors(row, col, h, w):
                    if m[n[0]][n[1]] != 0:
                        border.add(n)
    for row, col in border:
        m[row][col] = 1

    q = Queue()
    for x in border:
        q.put(x)

    max_value = 0
    while not q.empty():
        row, col = q.get()
        for n in get_neighbors(row, col, h, w):
            if m[n[0]][n[1]] == 0:
                value = m[row][col] + 1
                m[n[0]][n[1]] = value
                if value > max_value:
                    max_value = value
                q.put(n)

    print "max value:", max_value

    weights = np.copy(the_map) # weights
    for row in range(h):
        for col in range(w):
            if weights[row][col] == 0:
                weights[row][col] = int(-255.0 / float(max_value) * m[row][col] + 255)

    return weights


def display_image(window_name, img):
    window = cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)

def path_test():

    img = read_image("map-small-2.png")
    the_map = get_map(img)

    h = len(the_map)
    w = len(the_map[0])
    origin = (h // 7 // 2, w // 3 // 2 * 5)
    dest = (h // 7 // 2 * 13, w // 3 // 2 * 3)

    dilated_map = dilate_map(the_map)
    weights = compute_map_weights(dilated_map)

    path_length, robot_path = pathFinder.find_path(dilated_map, origin, dest, weights)

    # Draw path on image
    for cell in robot_path:
        img[cell[0]][cell[1]] = [0, 0, 255] # BGR

    display_image("Map", the_map)
    display_image("Dilation", dilated_map)
    display_image("Weights", weights)
    display_image("Path", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# path_test()
