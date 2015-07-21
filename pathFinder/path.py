
class PathFinder:
    """
    Base class for different path finding implementations.
    Override get_path in subclasses.
    """

    def __init__(self, grid):
        self.grid = grid
        
    def get_path(self, origin, dest):
        pass
