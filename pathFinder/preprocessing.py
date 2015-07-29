"""
Pre-processing functions for path finder.
"""

import cv2
import numpy as np
from Queue import Queue

import settings


def get_dilation_kernel(grid):
    """
    Get dilation kernel, based on robot size...
    """
    grid_height, grid_width = grid.shape
    
    kernel_width = settings.bot_radius * grid_width / settings.maze_width
    kernel_height = settings.bot_radius * grid_height / settings.maze_length

    print "kernel width:", kernel_width
    print "kernel height:", kernel_height
    
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
