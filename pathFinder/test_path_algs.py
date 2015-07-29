import numpy as np

from path_bfs import PathFinderBFS
from path_as import PathFinderAStar
from path_dijkstra import PathFinderDijkstra


# Simple test for BFS algorithm
def test_path_bfs():
    
    grid = np.array([[0, 1, 0, 0, 0],
                     [0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0],
                     [0, 0, 0, 1, 0]])
    origin = (0, 0)
    dest = (4, 4)

    path_finder = PathFinderBFS(grid)
    path_length, path = path_finder.get_path(origin, dest)

    print("distance: " + str(path_length))
    print("path: " + str(path))

    assert path == [(0,0), (1,0), (2,0), (3,0), (4,1), (3,2), (2,2), (1,2), (0,3), (1,4), (2,4), (3,4), (4,4)]

# Simple test for A-Start algorithm
def test_path_as():

    grid = np.array([[0, 1, 0, 0, 0],
                     [0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0],
                     [0, 0, 0, 1, 0]])
    origin = (0, 0)
    dest = (4, 4)

    path_finder = PathFinderAStar(grid)
    path_length, path = path_finder.get_path(origin, dest)

    print("distance: " + str(path_length))
    print("path: " + str(path))

    assert path == [(0,0), (1,0), (2,0), (3,0), (4,1), (3,2), (2,2), (1,2), (0,3), (1,4), (2,4), (3,4), (4,4)]


# Simple test for Djikstra's algorithm
def test_path_dijkstra():

    grid = np.array([[0, 1, 0, 0, 0],
                     [0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0],
                     [0, 0, 0, 1, 0]])
    origin = (0, 0)
    dest = (4, 4)

    path_finder = PathFinderDijkstra(grid)
    path_length, path = path_finder.get_path(origin, dest)

    print("distance: " + str(path_length))
    print("path: " + str(path))

    assert path == [(0,0), (1,0), (2,0), (3,0), (4,1), (3,2), (2,2), (1,2), (0,3), (1,4), (2,4), (3,4), (4,4)]


# Run all tests...
test_path_bfs()
test_path_as()
test_path_dijkstra()
