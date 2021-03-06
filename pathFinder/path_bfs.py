import numpy as np
from Queue import Queue

from path import PathFinder


class PathFinderBFS(PathFinder):
    """
    Breath First Search path finder.
    """
    def __init__(self, grid):
        super(PathFinderBFS, self).__init__(grid)

    def get_path(self, origin, dest, weights = None):
        """
        Compute path using BFS.
        """
        # Compute distances
        distance = [[float("inf") for col in range(self._grid_width)] for row in range(self._grid_height)]
        visited = [[False for col in range(self._grid_width)] for row in range(self._grid_height)]
        distance[origin[0]][origin[1]] = 0
        visited[origin[0]][origin[1]] = True
        q = Queue()
        q.put(origin)
        while q:
            node = q.get()
            # Check if destination reached
            if node == dest:
                break
            # Add neighbors
            neighbors = self.get_neighbors(node[0], node[1])
            for n in neighbors:
                if not visited[n[0]][n[1]]:
                    distance[n[0]][n[1]] = distance[node[0]][node[1]] + 1
                    q.put(n)
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

        self.visited = visited
        return path_length, path

    def get_visited(self):
        print "visited nodes"
        visited = None
        if self.visited:
            visited = set([])
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    visited.add((row, col))
        return visited
