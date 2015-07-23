import numpy as np
from Queue import PriorityQueue

from path import PathFinder


# For debugging...
def print_grid(grid):
    for row in range(len(grid)):
        print(grid[row])


class PathFinderAStar(PathFinder):
    """
    A* Search path finder.
    See: http://www.redblobgames.com/pathfinding/a-star/introduction.html
    """
    def __init__(self, grid):
        PathFinder.__init__(self, grid)

    def heuristic(self, dest, node):
        """
        A* heuristic from node to destination.
        """
        dy = abs(dest[0] - node[0])
        dx = abs(dest[1] - node[1])
        return abs(dx) + abs(dy) # Manhattan distance
        #return dy * dy + dx * dx # Squared Euclidean distance

    def get_path(self, origin, dest):

        # Compute path costs
        q = PriorityQueue()
        q.put((0, origin)) # store (priority, node)
        path_cost = {}
        prev_node = {} # for backtracking
        path_cost[origin] = 0
        prev_node[origin] = None

        while not q.empty():
            node = q.get()[1]
            
            if node == dest:
                break

            neighbors = self.get_neighbors(node[0], node[1])
            for n in neighbors:
                step_cost = 1 # TODO: this may not be a constant (diagonals should be different)
                new_cost = path_cost[node] + step_cost
                if n not in path_cost or new_cost < path_cost[n]:
                    path_cost[n] = new_cost
                    priority = new_cost + self.heuristic(dest, n)
                    prev_node[n] = node
                    q.put((priority, n))

        # No path found
        if dest not in path_cost:
            return float("inf"), []

        # Determine path
        path_length = path_cost[dest]
        node = dest
        path = [dest]
        while node != origin:
            node = prev_node[node]
            path.append(node)
        path.reverse()

        self.visited = path_cost  # temporary, for the UI
        return path_length, path


#Simple test...
def run_test():

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

run_test()
 