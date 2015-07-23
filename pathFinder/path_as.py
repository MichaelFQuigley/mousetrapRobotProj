#from math import abs

from Queue import Queue
from Queue import PriorityQueue

from path import PathFinder


# For debugging...
def print_grid(grid):
    for row in range(len(grid)):
        print(grid[row])



class PathFinderAStar(PathFinder):
    """
    A* Search path finder.
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
        """
        Compute path using A*.
        """
        # Compute distances
        q = PriorityQueue()
        distance = [[float("inf") for col in range(self._grid_width)] for row in range(self._grid_height)]
        visited = [[False for col in range(self._grid_width)] for row in range(self._grid_height)]
        distance[origin[0]][origin[1]] = 0
        visited[origin[0]][origin[1]] = True
        q.put((0, origin))
        while not q.empty():
            node = q.get()[1]
            #print node
            
            if node == dest:
                #print("Reached destination!")
                break

            neighbors = self.get_neighbors(node[0], node[1])
            for n in neighbors:
                #new_cost = cost_so_far[current] + graph.cost(current, next)
                #distance[n[0]][n[1]] = distance[node[0]][node[1]] + 1

                new_cost = distance[node[0]][node[1]] + 1 # this 1 may not be a constant
                if not visited[n[0]][n[1]] or new_cost < distance[n[0]][n[1]]:
                    distance[n[0]][n[1]] = new_cost
                    priority = new_cost + self.heuristic(dest, n)
                    #print priority, n
                    q.put((priority, n))
                    #came_from[next] = current
                    visited[n[0]][n[1]] = True

        # Determine path
        if not visited[dest[0]][dest[1]]:
            return float("inf"), []

        path_length = distance[dest[0]][dest[1]]
        row = dest[0]
        col = dest[1]
        path = [(row, col)]
        while row != origin[0] or col != origin[1]:
            neighbors = self.get_neighbors(row, col)
            for n in neighbors:
                if distance[n[0]][n[1]] < distance[row][col]:
                    row = n[0]
                    col = n[1]
                    path.append((row, col))
                    break
        path.reverse()

        self.visited = visited  # temporary, for the UI
        return path_length, path


#Simple test...
def run_test():

    grid = [[False, True,  False, False, False],
            [False, True,  False, True,  False],
            [False, True,  False, True,  False],
            [False, True,  False, True,  False],
            [False, False, False, True,  False]]
    origin = (0, 0)
    dest = (4, 4)

    path_finder = PathFinderAStar(grid)
    path_length, path = path_finder.get_path(origin, dest)

    print("distance: " + str(path_length))
    print("path: " + str(path))

    assert path == [(0,0), (1,0), (2,0), (3,0), (4,1), (3,2), (2,2), (1,2), (0,3), (1,4), (2,4), (3,4), (4,4)]

run_test()
 
