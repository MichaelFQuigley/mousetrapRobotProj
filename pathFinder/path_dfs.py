from collections import deque

# Grid size
WIDTH = 100
HEIGHT = 100

# Start and end locations
origin = (0, 0)
dest = (HEIGHT - 1, WIDTH - 1)

# Grid map
grid = [[0 for col in range(WIDTH)] for row in range(HEIGHT)]


# Just for debugging...
def print_grid(grid):
    for row in range(HEIGHT):
        print(grid[row])


# Get 8-adjacent neighbors
def get_neighbors(row, col):
    n = []
    for r in [-1, 0, 1]:
        for c in [-1, 0, 1]:
            if r != 0 or c != 0:
                n_row = row + r
                n_col = col + c
                if n_row >= 0 and n_row < HEIGHT and n_col >= 0 and n_col < WIDTH:
                    n.append((n_row, n_col))
    return n


def init_grid(width, height):

    global WIDTH, HEIGHT
    global origin, dest
    global grid

    WIDTH = width
    HEIGHT = height

    origin = (0, 0)
    dest = (HEIGHT - 1, WIDTH - 1)

    grid = [[0 for col in range(WIDTH)] for row in range(HEIGHT)]


# Path finding algorithm 1
def get_path_bfs(origin, dest):
    """
    Compute shortest path using BFS.
    Returns path length, and path as a list of nodes.
    """
    # Compute distances
    visited = [[False for col in range(WIDTH)] for row in range(HEIGHT)]
    visited[origin[0]][origin[1]] = True
    q = deque()
    q.appendleft(origin)
    while q:
        node = q.pop()

        # Check node
        if node == dest:
            break
        
        # Add neighbors
        neighbors = get_neighbors(node[0], node[1])
        for n in neighbors:
            if not visited[n[0]][n[1]]:
                grid[n[0]][n[1]] = grid[node[0]][node[1]] + 1
                q.appendleft(n)
                visited[n[0]][n[1]] = True

    # Determine path
    dist = grid[dest[0]][dest[1]]
    row = dest[0]
    col = dest[1]
    path = [(row, col)]
    while row != origin[0] and col != origin[1]:
        neighbors = get_neighbors(row, col)
        for n in neighbors:
            if grid[n[0]][n[1]] < grid[row][col]:
                row = n[0]
                col = n[1]
                path.append((row, col))
                break
    path.reverse()

    return dist, path



#print_map(grid)

path_length, path = get_path_bfs(origin, dest)

print("distance: " + str(path_length))
print("path: " + str(path))

 
