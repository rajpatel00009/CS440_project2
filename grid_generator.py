import random

GRID_SIZE = 30

# intial grid with all open cells
grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def reset_grid():
    global grid
    grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def update_dead_ends(dead_ends):
    for grid_row, row in enumerate(grid):
        for grid_column, val in enumerate(row):           
            r = (grid_row, grid_column)
            neighbors2 = get_neighbors(r)
            opened_neighbors = sum(
                1
                for r, c in neighbors2.values()
                if(grid[r][c] == '.')
            )
            if (opened_neighbors == 1) and (grid[grid_row][grid_column] == '.'):
                dead_ends.append((grid_row, grid_column))

def setup_grid():

    # the first cell to open
    open_cell = (random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2))
    row, column = open_cell
    grid[row][column] = '.' 

    # list of all cells which are valid and we can open (with exectly one neighbor)
    valid_cells = []
    valid_cells_set = set()
    for neighbor in get_neighbors(open_cell).values():
        valid_cells.append(neighbor)

    # look through each valid cell and randomlly open cell 
    while valid_cells:
        rand = random.randint(0, len(valid_cells) - 1)

        valid_cell_to_open = valid_cells.pop(rand)

        valid_cell_row, valid_cell_column = valid_cell_to_open

        if(grid[valid_cell_row][valid_cell_column] == '.'):
            continue

        neighbors = get_neighbors(valid_cell_to_open)
        opened_neighbors = sum(
            1
            for r, c in neighbors.values()
            if(grid[r][c] == '.')
        )

        if(opened_neighbors != 1):
            continue

        # open the selected cell
        grid[valid_cell_row][valid_cell_column] = '.'

        # add blocked neighbors as possible candidates
        for n in neighbors.values():
            r, c = n
            if(grid[r][c] == '*' and n not in valid_cells_set): 
                valid_cells.append(n)
                valid_cells_set.add(n)

    dead_ends = []
    update_dead_ends(dead_ends)
    dead_ends = set(dead_ends)

    to_remove = len(dead_ends) // 2
    while len(dead_ends) > to_remove:

        cell = random.choice(tuple(dead_ends))
        closed_neighbors = [] 
        for n in get_neighbors(cell).values():
            row = n[0]
            col = n[1]
            if (grid[row][col] == '*'):
                closed_neighbors.append(n)
        
        opened = random.choice(closed_neighbors)
        r, c = opened
        grid[r][c] = '.'
        changed = [opened, *get_neighbors(opened).values()]

        for i in changed:
            r1, c1 = i
            dead_ends.discard(i)
            if (grid[r1][c1] != '.'):
                continue
            open_count = sum (
                grid[nr][nc] == '.'
                for nr, nc in get_neighbors(i).values()
            )
            if(open_count == 1): 
                dead_ends.add(i)

# getting neighbots of given cell 
def get_neighbors(pos):
    x, y = pos
    neighbors = {}
    if x > 0: neighbors["top"] = (x - 1, y)
    if x < GRID_SIZE - 1: neighbors["bottom"] = (x + 1, y)
    if y > 0: neighbors["left"] = (x, y - 1)
    if y < GRID_SIZE - 1: neighbors["right"] = (x, y + 1)

    return neighbors

setup_grid()

for i in range (GRID_SIZE):
    print(grid[i])
