
class PathFinder:
    """
    Base class for different path finding implementations.
    Override get_path in subclasses.
    """

    def __init__(self, grid):
        """
        The grid is a boolean array where False locations are blocked.
        """
        self._grid = grid
        self._grid_height = len(grid)
        self._grid_width = len(grid[0])
        
    def get_path(self, origin, dest):
        """
        Returns a tuple, where the first element is the path length,
        and the second element is the path as a list of cells.
        Returns (float("inf"), []) if there is no path to the destination.
        Cells are (row, column) tuples.
        """
        pass
