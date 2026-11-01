import random

#from grid_generator import GRID_SIZE, grid 

# this function would look for lost bot in radius k and return 1 on sucess otherwise -1
def type1_detactor(curr_locator_bot):
    r, c = curr_locator_bot
    
    min_row = r - K if (r - K >= 0) else 0
    max_row = r + K if (r + K < GRID_SIZE) else GRID_SIZE - 1 

    min_col =  c - K if (c - K >= 0) else 0
    max_col = c + K if (c + K < GRID_SIZE) else GRID_SIZE - 1 

    for i in range(min_row, max_row):
        for j in range(min_col, max_col):
            if(grid[i][j] == 'l'):
                return 1
    return -1
                


GRID_SIZE = 10

# intial grid with all open cells
grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


K = 5 # radius for type a
A = 2 # alpha value for type b

possible_cells = []
impossible_cells = []

#initially all cells are possible
possible_cells = grid

init_locator_bot = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

init_lost_bot = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

r1, c1 = init_locator_bot
r2, c2 = init_lost_bot

grid[r1][c1] = 'b'
grid[r2][c2] = 'l'

ping = type1_detactor(init_locator_bot)

if(ping == 1):
    print('in range')
else:
    print('not in range')


for i in range(GRID_SIZE):
    print(grid[i])




# def euclidean_dis(cell1, cell2):
   
# def type_a_ping():
    


# for the type one if k is 10 look in radius of 10 from current cell and if the device pings mark all cells in radius 10 possible. The move to nearest cell if multiple select random. Once you see any cell does not ping mark all the cells in radius impossible. If you move to next cell and cell pings mark the previous possible cells as impossible as losed bot is now in new radius.



