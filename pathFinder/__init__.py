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
    print "instance", instance
    return instance.get_path(origin, dest, weights)

set_type('AStar')
