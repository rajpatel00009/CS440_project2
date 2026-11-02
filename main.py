import random

GRID_SIZE = 10

K = 5 # radius for type a
A = 2 # alpha value for type b

possible_cells = []
impossible_cells = []


def type1_detactor(curr_locator_bot):
    cells = []
    r, c = curr_locator_bot

    if(curr_locator_bot == init_lost_bot):
        return (0, [])
    
    min_row = r - K if (r - K >= 0) else 0
    max_row = r + K if (r + K < GRID_SIZE) else GRID_SIZE - 1 

    min_col =  c - K if (c - K >= 0) else 0
    max_col = c + K if (c + K < GRID_SIZE) else GRID_SIZE - 1 
    
    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            if((i, j) not in impossible_cells):
                cells.append((i, j))

    for cell in cells:
        r1, c1 = cell
        if(grid[r1][c1] == 'l'):
            return (1, cells)
    return (-1, cells)
                
# intial grid with all open cells
grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


init_locator_bot = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
init_lost_bot = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

r1, c1 = init_locator_bot
r2, c2 = init_lost_bot

grid[r1][c1] = 'b'
grid[r2][c2] = 'l'

possible_cells = [
    (i, j)
    for i in range(GRID_SIZE)
    for j in range(GRID_SIZE)
]
ping = type1_detactor(init_locator_bot)

while (ping[0] != 0):

    if(ping[0] == 1):
        print('in range')
        possible_cells_2 = ping[1]
        possible_cells = list(set(possible_cells) & set(possible_cells_2)) # intersection of both lists 

        if not possible_cells:
            print("No possible cells left")
            break

        picked = random.choice(possible_cells)
        possible_cells.remove(picked)
        ping = type1_detactor(picked)
        
    else:
        print('not in range')
        impossible_cells.extend(ping[1])
        possible_cells = [item for item in possible_cells if item not in (ping[1])] # remove the list of impossible cells from possible cells 
        if not possible_cells:
            print("No possible cells left")
            break


        picked = random.choice(possible_cells)
        possible_cells.remove(picked)
        
        ping = type1_detactor(picked)

print("we won")

for i in range(GRID_SIZE):
    print(grid[i])




# def euclidean_dis(cell1, cell2):
   
# def type_a_ping():
    


# for the type one if k is 10 look in radius of 10 from current cell and if the device pings mark all cells in radius 10 possible. The move to nearest cell if multiple select random. Once you see any cell does not ping mark all the cells in radius impossible. If you move to next cell and cell pings mark the previous possible cells as impossible as losed bot is now in new radius.



