from pathFinderDijkstra import PathFinderDijkstra as Dijkstra
from path_as import PathFinderAStar as AStar
from path_bfs import PathFinderBFS as BFS

types = {
    'Dijkstra': Dijkstra,
    'AStar': AStar,
    'BFS': BFS}

current = None
solver = None

def get_types():
    return types.keys()

def set_type(t):
    global current, solver
    if types.has_key(t):
        solver = types[t]
        current = t

def find_path(grid, origin, dest, weights=None):
    global solver
    inst = solver(grid)
    return inst.get_path(origin, dest, weights)

set_type('AStar')
