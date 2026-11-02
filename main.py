import random
import math

GRID_SIZE = 3

K = 5 # radius for type a
A = 2 # alpha value for type b
COST = 2 # cost per step
TOTAL_COST = 0


possible_cells = []
impossible_cells = []

cells_to_probs = {
    (i, j): 1/(GRID_SIZE**2)
    for i in range(GRID_SIZE)
    for j in range(GRID_SIZE)
}

def distance_between_cells(cell1, cell2):
    r1, c1 = cell1
    r2, c2 = cell2

    return abs(r2 - r1) + abs(c2 - c1)

def euclidean_distance(cell1, cell2):
    r1, c1 = cell1
    r2, c2 = cell2

    return math.sqrt((r2 - r1)**2 + (c2 - c1)**2)

# this detector will ping when the bot we are looking for is in radius of K 
def type1_detector(curr_locator_bot):
    global COST
    global TOTAL_COST
    cells = []
    r, c = curr_locator_bot
    TOTAL_COST += COST * 0.5

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

def count_probability(curr_cell, result):

    for cell in cells_to_probs:
        dis = euclidean_distance(cell, curr_cell)
        ping_prob = math.exp((0 - A)*(dis - 1))
        if result == "PING":
            likelihood = ping_prob
        else:
            likelihood = 1 - ping_prob

            
        cells_to_probs[cell] = likelihood
        
    total = sum(cells_to_probs.values())

    for cell in cells_to_probs:
        cells_to_probs[cell] = cells_to_probs[cell]/total 


# # this detector will ping with high prob. when the losted bot iis near by, 
# def type2_detector(curr_locator_bot):


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
ping = type1_detector(init_locator_bot)

while (ping[0] != 0):
    
    if init_locator_bot in possible_cells:
        possible_cells.remove(init_locator_bot)
    if(ping[0] == 1):
        print('in range')
        possible_cells_2 = ping[1]
        possible_cells = list(set(possible_cells) & set(possible_cells_2)) # intersection of both lists 

        if not possible_cells:
            print("No possible cells left")
            break


        min_dist = min(distance_between_cells(init_locator_bot, cell)
            for cell in possible_cells
        )

        nearest_cells = [cell for cell in possible_cells
            if distance_between_cells(init_locator_bot, cell) == min_dist
        ]

        picked = random.choice(nearest_cells)


        possible_cells.remove(picked)
        dist = distance_between_cells(init_locator_bot, picked)
        TOTAL_COST += COST * dist
        init_locator_bot = picked

        ping = type1_detector(picked)
        
    else:
        print('not in range')
        impossible_cells.extend(ping[1])
        possible_cells = [item for item in possible_cells if item not in (ping[1])] # remove the list of impossible cells from possible cells 
        if not possible_cells:
            print("No possible cells left")
            break


        min_dist = min(distance_between_cells(init_locator_bot, cell)
            for cell in possible_cells
        )

        nearest_cells = [cell for cell in possible_cells
            if distance_between_cells(init_locator_bot, cell) == min_dist
        ]

        picked = random.choice(nearest_cells)

        possible_cells.remove(picked)

        dist = distance_between_cells(init_locator_bot, picked)
        TOTAL_COST += COST * dist
        init_locator_bot = picked
        
        ping = type1_detector(picked)

print("we won")
print(TOTAL_COST)


print('type 2 testing')

result = "PING"
raj = count_probability(init_locator_bot, result)
print(cells_to_probs.values())


for i in range(GRID_SIZE):
    print(grid[i])




   
    


# for the type one if k is 10 look in radius of 10 from current cell and if the device pings mark all cells in radius 10 possible. The move to nearest cell if multiple select random. Once you see any cell does not ping mark all the cells in radius impossible. If you move to next cell and cell pings mark the previous possible cells as impossible as losed bot is now in new radius.



