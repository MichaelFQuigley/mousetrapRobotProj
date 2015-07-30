"""
Pre-processing functions for path finder.
"""
from __future__ import division
import os, sys

# For importing settings module from parent directory
currentdir = os.path.dirname(__file__)
parentdir = os.path.join(currentdir, os.pardir)
sys.path.append(parentdir)

import cv2
import numpy as np
from Queue import Queue

import settings

def downsize_image(img):
    """
    Downsize to a maximum size for faster processing.
    Returns downsize ration, and new image.
    """
    max_width = settings.path_finder_max_img_width
    max_height = settings.path_finder_max_img_height

    h, w = img.shape[:2]
    print("size: " + str((w, h)))

    ratio = min(1.0, min(max_height / h, max_width / w))
    print("ratio: " + str(ratio))
    
    new_size = (int(w * ratio), int(h * ratio))
    print("new size: " + str(new_size))

    return ratio, cv2.resize(img, new_size, interpolation = cv2.INTER_AREA)    

def get_map_img(img):
    """
    Get map as a NumPy array.
    """
    if len(img.shape) > 2:
        return np.array(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    return np.array(img)

def threshold_img(gray_img):
    """
    Make image black and white (no grays).
    """
    img_thresh = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return np.array(img_thresh[1])


def get_dilation_kernel(grid):
    """
    Get dilation kernel, based on robot size...
    """
    grid_height, grid_width = grid.shape
    
    kernel_width = settings.bot_radius * grid_width / settings.maze_width
    kernel_height = settings.bot_radius * grid_height / settings.maze_length

    print("kernel width: " + str(kernel_width))
    print("kernel height: " + str(kernel_height))
    
    return np.ones((kernel_height, kernel_width), np.uint8)

def dilate_map(grid):
    """
    Dilate map, based on robot size, to mark spots that are too close
    to obstacles as blocked spots.
    """
    kernel = get_dilation_kernel(grid)
    return cv2.dilate(grid, kernel, iterations = 1)


# Predetermined neighbor coordinates
neighbor_cords_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
neighbor_cords_4 = [(-1, 0), (0, -1), (0, 1), (1, 0)]

def get_neighbors(row, col, height, width):
    """
    Get adjacent neighbors.
    """
    neighbors = []
    for r, c in neighbor_cords_4:
        n_row = row + r
        n_col = col + c
        if n_row >= 0 and n_row < height and n_col >= 0 and n_col < width:
            neighbors.append((n_row, n_col))
    return neighbors

def compute_map_weights(the_map):
    """
    Compute map weidhts to be used by path finding algorith.
    Returns a 2D array with the same dimensions as the map, 
    where the value at (row, col) is the extra cost of
    stepping on (row, col).
    """
                        
    h, w = the_map.shape
    print("map size:" + str(the_map.shape))

    dist = np.zeros(the_map.shape, dtype = np.uint) # distance from obstacles

    # Start with all locations next to an obstacle
    border = set([])
    for row in range(h):
        for col in range(w):
            if the_map[row][col] == 0:
                for n in get_neighbors(row, col, h, w):
                    if the_map[n[0]][n[1]] != 0 and dist[n[0]][n[1]] == 0:
                        dist[n[0]][n[1]] = 1
                        border.add(n)
    frontier = Queue()
    for x in border:
        frontier.put(x)

    # Compute distance to obstacles for all free locations
    max_dist = 0
    while not frontier.empty():
        row, col = frontier.get()
        for n in get_neighbors(row, col, h, w):
            if the_map[n[0]][n[1]] == 0 and dist[n[0]][n[1]] == 0:
                d = dist[row][col] + 1
                dist[n[0]][n[1]] = d
                if d > max_dist:
                    max_dist = d
                frontier.put(n)

    print("max distance: " + str(max_dist))

    # Determine weights from distances
    weights = np.zeros(the_map.shape)
    for row in range(h):
        for col in range(w):
            x = 1.0 - dist[row][col] / float(max_dist)
            x *= w + h
            weights[row][col] = x

    return weights


def create_weights_image(weights):
    """
    Convert weights 2D array to an image that can be displayed.
    """
    h, w = weights.shape
    weights_img = np.zeros(weights.shape, dtype = np.uint8)

    max_weight = 0
    for row in range(h):
        for col in range(w):
            if weights[row][col] > max_weight:
                max_weight = weights[row][col]

    for row in range(h):
        for col in range(w):
            weights_img[row][col] = int(weights[row][col] / float(max_weight) * 255)

    return weights_img

def create_display_image(the_map, dilated_map, weights_img):
    """
    Create image for display, including obstacles, dilation, and visual representation of weights.
    """
    obstacle_color = [255, 255, 255]
    dilation_color = [194, 32, 0]

    h, w = the_map.shape
    display_img = np.zeros((h,w,3), dtype = np.uint8)
    
    for row in range(h):
        for col in range(w):
            if the_map[row][col] != 0:
                display_img[row][col] = obstacle_color
            elif dilated_map[row][col] != 0:
                display_img[row][col] = dilation_color
            else: # weights
                #x = weights_img[row][col] * 0.75
                #x = weights_img[row][col] ** 0.5 * (255 ** 0.5) * 0.5
                x = weights_img[row][col]
                display_img[row][col] = [x, x // 3, 0]

    return display_img

def draw_path(img, origin, dest, path_waypoints):
    """
    Draw path waypoints, and mark origin and destination.
    """
    path_color = [0, 0, 255]
    endpoints_color = [0, 255, 0]
    
    # Draw path on image
    for cell in path_waypoints:
        mark_location(img, cell, path_color)

    # Mark origin and destination
    mark_location(img, origin, endpoints_color)
    mark_location(img, dest, endpoints_color)

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

    
# This is actually post-processing, but left in here for now.
# TODO: decide where is the best place to put it.
def sample_path(the_map, path):
    h, w = the_map.shape
    step = int(w * (settings.bot_radius / 2) / settings.maze_width)
    print("step: " + str(step))
    return [path[i] for i in range(0, len(path), step)]

