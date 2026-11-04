from ipaddress import NetmaskValueError
import random
import math
from socket import TCP_NOTSENT_LOWAT
import random
import matplotlib.pyplot as plt


GRID_SIZE = 30

K = 10 # radius for type a
A = 2 # alpha value for type b
COST = 1 # cost per step
TOTAL_COST = 0


grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

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


def find_edges(cell):
    r, c = cell
    temp = []

    distances = [1, max(1, K // 2), max(1, K - 1)]

    for d in distances:
        directions = [
            (0, -d),  # left
            (0, d),   # right
            (-d, 0),  # up
            (d, 0)    # down
        ]

        for dr, dc in directions:
            new_r = r + dr
            new_c = c + dc

            if 0 <= new_r < GRID_SIZE and 0 <= new_c < GRID_SIZE:
                temp.append((new_r, new_c))

    return temp

def count_probability(curr_cell, result):

    for cell in cells_to_probs:
        if cell == curr_cell:
            cells_to_probs[cell] = 0
            continue
        dis = euclidean_distance(cell, curr_cell)
        ping_prob = math.exp((0 - A)*(dis - 1))
        if result == "PING":
            likelihood = ping_prob
        else:
            likelihood = 1 - ping_prob

        cells_to_probs[cell] *= likelihood
        
    total = sum(cells_to_probs.values())

    for cell in cells_to_probs:
        cells_to_probs[cell] = cells_to_probs[cell]/total
    
# find the nearset cell from the given list in case probability matched for type 2
def nearest_cell(cell, cells):
    return min(
        cells,
        key=lambda c: distance_between_cells(cell, c)
    )


def calculate_score(curr_cell, candidate, possible_cells):

    inside = 0
    for cell in possible_cells:
        r1, c1 = candidate
        r2, c2 = cell
        if abs(r1 - r2) <= K and abs(c1 - c2) <= K:
            inside += 1

    total = len(possible_cells)
    outside = total - inside

    if(total == 0):
        return 0

    if candidate in possible_cells:
        expected_eliminated = total - (
            (inside - 1)**2 + outside**2
        ) / total
    else:
        expected_eliminated = (2 * inside * outside) / total
    dist = distance_between_cells(curr_cell, candidate)
    score = expected_eliminated / (dist + 0.5)

    return score

def run_type1(init_locator_bot):
    global impossible_cells
    global TOTAL_COST


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

    
    return TOTAL_COST

def run_type2(init_locator_bot):
    global TOTAL_COST
    if(init_locator_bot == init_lost_bot):
        return TOTAL_COST


    while init_locator_bot != init_lost_bot:

        dist = euclidean_distance(init_locator_bot, init_lost_bot)
        ping_prob = math.exp(-A * (dist - 1))

        TOTAL_COST += COST * 0.5
        rand_num = random.random()
        if(rand_num < ping_prob):
            result = 'PING'
        else:
            result = 'NO PING'

        count_probability(init_locator_bot, result) 
        best_prob = max(cells_to_probs.values()) # the max probability

        best_cells = [] # cells having best probability
        for cell in cells_to_probs:
            if(cells_to_probs[cell] == best_prob):
                best_cells.append(cell)
        if(best_cells):
            best_cell = nearest_cell(init_locator_bot, best_cells)# pick the closest cell
        else:
            best_cell = cells_to_probs[best_prob] # if only one, pick it

        dist = distance_between_cells(init_locator_bot, best_cell)

        TOTAL_COST += COST * dist 
        init_locator_bot = best_cell

    return TOTAL_COST

def run_type1_improved(init_locator_bot):
    global impossible_cells
    global TOTAL_COST


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

            
            if len(possible_cells) == 1:
                picked = possible_cells[0]

            else:
                edge_cells = find_edges(init_locator_bot)
                candidates = list(set(edge_cells + nearest_cells))

                picked = max(
                    candidates,
                    key=lambda cell: calculate_score(
                        init_locator_bot, cell, possible_cells
                    )
                )

                # If no information can be gained, visit a possible cell
                if calculate_score(init_locator_bot, picked, possible_cells) <= 0:
                    picked = random.choice(nearest_cells)

            if picked in possible_cells:
                possible_cells.remove(picked)



            dist = distance_between_cells(init_locator_bot, picked)
            TOTAL_COST += COST * dist
            init_locator_bot = picked

            ping = type1_detector(picked)
            
        else:
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


            dist = distance_between_cells(init_locator_bot, picked)
            TOTAL_COST += COST * dist
            init_locator_bot = picked
            
            ping = type1_detector(picked)


    return TOTAL_COST


# instead of traveling to the cell with high prob, travel to the one which is near and run the detector more than one time in the start so that we can have 
#  better estimate in the start. ONce we have more data we can travel more, and we can do less detector operation 

def run_type2_improved(init_locator_bot):

    global TOTAL_COST
    if(init_locator_bot == init_lost_bot):
        return TOTAL_COST
    while init_locator_bot != init_lost_bot:

        dist = euclidean_distance(init_locator_bot, init_lost_bot)
        ping_prob = math.exp(-A * (dist - 1))

        TOTAL_COST += COST * 0.5
        rand_num = random.random()
        if(rand_num < ping_prob):
            result = 'PING'
        else:
            result = 'NO PING'

        weighted_prob = {}
        for cell in cells_to_probs:
            dis = distance_between_cells(init_locator_bot, cell)
            weighted_prob[cell] = cells_to_probs[cell] / (dis+0.5)
        
        count_probability(init_locator_bot, result) 
        best_prob = max(weighted_prob.values()) # the max probability

        best_cells = [] # cells having best probability
        for cell in weighted_prob:
            if(weighted_prob[cell] == best_prob):
                best_cells.append(cell)
        if(best_cells):
            best_cell = nearest_cell(init_locator_bot, best_cells) # pick the closest cell
        else:
            best_cell = weighted_prob[best_prob] # if only one, pick it

        dist = distance_between_cells(init_locator_bot, best_cell)
        TOTAL_COST += COST * dist 
        init_locator_bot = best_cell

    return TOTAL_COST

# intial grid with all open cells

# run_type1(init_locator_bot)
# run_type2(init_locator_bot)

regular_type1_results = []
improved_type1_results = []
regular_type2_results = []
improved_type2_results = []


for n in range(10):

    total_regular_type1 = 0
    total_impr_type1 = 0
    total_regular_type2 = 0
    total_impr_type2 = 0

    for i in range(100):

        init_locator_bot = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        init_lost_bot = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

        r1, c1 = init_locator_bot
        r2, c2 = init_lost_bot
        grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        grid[r1][c1] = 'b'
        grid[r2][c2] = 'l'

        cells_to_probs = {
            (i, j): 1/(GRID_SIZE**2)
            for i in range(GRID_SIZE)
            for j in range(GRID_SIZE)
        }
        TOTAL_COST = 0
        possible_cells = []
        impossible_cells = []
        total_regular_type1 += run_type1(init_locator_bot)

        init_locator_bot = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        init_lost_bot = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

        r1, c1 = init_locator_bot
        r2, c2 = init_lost_bot
        grid = [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        grid[r1][c1] = 'b'
        grid[r2][c2] = 'l'
        cells_to_probs = {
            (i, j): 1/(GRID_SIZE**2)
            for i in range(GRID_SIZE)
            for j in range(GRID_SIZE)
        }
        TOTAL_COST = 0
        possible_cells = []
        impossible_cells = []
        total_impr_type1 += run_type1_improved(init_locator_bot)

        cells_to_probs = {
            (i, j): 1/(GRID_SIZE**2)
            for i in range(GRID_SIZE)
            for j in range(GRID_SIZE)
        }
        TOTAL_COST = 0
        possible_cells = []
        impossible_cells = []
        total_regular_type2 += run_type2(init_locator_bot)



        cells_to_probs = {
            (i, j): 1/(GRID_SIZE**2)
            for i in range(GRID_SIZE)
            for j in range(GRID_SIZE)
        }
        TOTAL_COST = 0
        possible_cells = []
        impossible_cells = []
        total_impr_type2 += run_type2_improved(init_locator_bot)
    
    print(f'total regular type1   {total_regular_type1/100}')
    print(f'total improved type2  {total_impr_type1/100}')

    print(f'total regular type1   {total_regular_type2/100}')
    print(f'total improved type2  {total_impr_type2/100}\n')


    regular_type1_results.append(total_regular_type1/100)
    improved_type1_results.append(total_impr_type1/100)
    regular_type2_results.append(total_regular_type2/100)
    improved_type2_results.append(total_impr_type2/100)



experiments = range(1, 11)

plt.figure(figsize=(10, 6))

plt.plot(experiments, regular_type1_results,
         marker='o', label='Regular Type 1')

plt.plot(experiments, improved_type1_results,
         marker='s', label='Improved Type 1')

plt.plot(experiments, regular_type2_results,
         marker='^', label='Regular Type 2')

plt.plot(experiments, improved_type2_results,
         marker='D', label='Improved Type 2')

plt.xlabel('Experiment Number', fontsize=12)
plt.ylabel('Average Total Cost', fontsize=12)

plt.title('Comparison of Regular and Improved Algorithms', fontsize=14)

plt.xticks(range(1, 11))
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()