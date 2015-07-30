from __future__ import division

import time
import cv2
import numpy as np
from Queue import Queue

import preprocessing
from path_dijkstra import PathFinderDijkstra as Dijkstra
from path_as import PathFinderAStar as AStar
from path_bfs import PathFinderBFS as BFS

types = {
    'Dijkstra': Dijkstra,
    'AStar': AStar,
    'BFS': BFS}

current = None
solver = None
instance = None

def get_types():
    return types.keys()

def set_type(t):
    global current, solver, instance
    if types.has_key(t):
        solver = types[t]
        current = t
        instance = None

def find_path(grid, origin, dest, weights=None):
    global solver, instance
    instance = solver(grid)
    return instance.get_path(origin, dest, weights)

set_type('AStar')


def sample_path(path, step):
    return [path[i] for i in range(0, len(path), step)]

def find_path_from_image(img, origin, dest):
    """
    Find path, given a map image.
    Returns the path, and an image to display.
    """
    h, w, c = img.shape # save original image size
    
    # For now just downsizing to half the original size
    print "Resizing image..."
    start_time = time.time()
    ratio, small_img = preprocessing.downsize_image(img)
    origin = (int(origin[0] * ratio), int(origin[1] * ratio))   # map origin to new scale
    dest = (int(dest[0] * ratio), int(dest[1] * ratio))         # map destination to new scale
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    print "Cleaning up map..."
    start_time = time.time()
    the_map = preprocessing.get_map_img(small_img)
    the_map = preprocessing.threshold_img(the_map)
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    print "Dilating map..."
    start_time = time.time()
    dilated_map = preprocessing.dilate_map(the_map)
    dilated_map = preprocessing.threshold_img(dilated_map)
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    print "Computing weights..."
    start_time = time.time()
    weights = preprocessing.compute_map_weights(dilated_map)
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    print "Computing path..."
    start_time = time.time()
    set_type('AStar')
    path_length, robot_path = find_path(dilated_map, origin, dest, weights)
    waypoints = sample_path(robot_path, 10)
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    print "Creating image..."
    start_time = time.time()
    weights_img = preprocessing.create_weights_image(weights)
    display_img = preprocessing.create_display_image(the_map, dilated_map, weights_img)
    preprocessing.draw_path(display_img, origin, dest, waypoints)
    end_time = time.time()
    print("Elapsed time: " + str(end_time - start_time))

    # Show images for all steps
    #display_image("Map", the_map)
    #display_image("Dilation", dilated_map)
    #display_image("Weights", weights_img)
    #display_image("Path", display_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Map path points and display image back to original scale
    path_waypoints = []
    for wp in path_waypoints:
        path_waypoints.append(wp[0] / ratio, wp[1] / ratio)
    display_img = cv2.resize(display_img, (w, h), interpolation = cv2.INTER_AREA)

    return path_waypoints, display_img


def display_image(window_name, img):
    window = cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)
       
