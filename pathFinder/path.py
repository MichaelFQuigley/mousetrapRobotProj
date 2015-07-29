from copy import copy


# For debugging...
def print_grid(grid):
    for row in range(len(grid)):
        print(grid[row])


class PathFinder(object):
    """
    Base class for different path finding implementations.
    Override get_path in subclasses.
    """

    def __init__(self, grid):
        """
        The grid is a NumPy array where cells with a value of zero
        are free, and locations with any other value are blocked.
        """
        self._grid = copy(grid)
        self._grid_height = len(grid)
        self._grid_width = len(grid[0])
        
    def within_bounds(self, row, col):
        """
        Determine if a cell is within the bounds of the map.
        """
        return row >= 0 and row < self._grid_height and col >= 0 and col < self._grid_width

    def is_blocked(self, row, col):
        """
        Determines if a cell is blocked and cannot be traversed.
        """
        return self._grid[row][col] != 0

    def get_neighbors(self, row, col):
        """
        Get 8-adjacent neighbors.
        Ignores blocked cells.
        """
        n = []
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if r != 0 or c != 0:
                    n_row = row + r
                    n_col = col + c
                    if self.within_bounds(n_row, n_col):
                        if not self.is_blocked(n_row, n_col): # ignore blocked cells
                            n.append((n_row, n_col))
        return n

    def get_path(self, origin, dest, weights = None):
        """
        Returns a tuple, where the first element is the path length,
        and the second element is the path as a list of cells.
        Returns (float("inf"), []) if there is no path to the destination.

        Cells are (row, column) tuples.

        The weights parameter is an array with the same dimmensions as the grid,
        and with the cost of stepping on each free cell.
        Some implementations may ignore this parameter.
        """
        pass

    def get_visited(self):
        """
        Return all cells visited by the algorithm after caling get_path.
        Implementing this method is optional.
        """
        pass
