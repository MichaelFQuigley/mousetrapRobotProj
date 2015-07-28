import time
import numpy as np
from Queue import Queue

from pathFinderDijkstra import PathFinderDijkstra as Dijkstra
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
    p = []
    for x in range(0, len(path), step):
        p.append(path[x])
    return p
        

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
    Add comment here...
    """
                        
    h, w = the_map.shape
    print "map size:", the_map.shape

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

    # Determine weights from distances (scaled to [0, 255])
    weights = np.copy(the_map)
    for row in range(h):
        for col in range(w):
            #weights[row][col] = int( 255 - 255 * dist[row][col] // max_dist )
            #weights[row][col] = int( (weights[row][col] ** 0.5) * 255 / float(255 ** 0.5) )
            x = 1.0 - dist[row][col] / float(max_dist)
            x = x ** 0.5
            x = x * 255
            weights[row][col] = int(x)

    return weights

