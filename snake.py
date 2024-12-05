from src import gen_cycle
from src import pathfinding
import random
from snake_logger import Log_Stream

# WIDTH = 7
# HEIGHT = 7

# RESTRICTED_TILES = [(0, 3), (1, 3), (0, 4), (1, 4), (4, 0), (5, 0), (4, 4), (5, 4)]

# WIDTH = 8
# HEIGHT = 8

WIDTH = 8
HEIGHT = 8

# RESTRICTED_TILES = [(4,4),(3,4),(4,3),(5,4),(4,5)]
# RESTRICTED_TILES = [(1, 1), (2, 1), (3, 4), (4, 4)]
RESTRICTED_TILES = []


AVAILABLE_TILES = WIDTH * HEIGHT - len(RESTRICTED_TILES)

print('+' + WIDTH * '-' + '+')

for y in range(HEIGHT):

    print('|', end = '')

    for x in range(WIDTH):
        if (x, y) in RESTRICTED_TILES:
            print('X', end = '')
        else:
            print('.', end = '')

    print('|')


print('+' + WIDTH * '-' + '+')

print('Doofus Checking Grid...')
# Determine initial cycle
g = gen_cycle.Grid(WIDTH, HEIGHT)
for x, y in RESTRICTED_TILES:
    g.nodes[y][x].disconnect_from_all_but(())

# Try to find hamiltonian cycle
# new_cycle = gen_cycle.solve_hamiltonian(g)

# if new_cycle is None:
#     raise ValueError('No Hamiltonian Cycle exists for this graph')

# current_hamiltonian_cycle = [g.calculate_coordinate(node_id) for node_id in new_cycle]

current_hamiltonian_cycle = []
for x in range(WIDTH):
    current_hamiltonian_cycle.append((x, 0))

for x in range(WIDTH - 1, -1, -2):
    for y in range(1, HEIGHT):
        current_hamiltonian_cycle.append((x, y))
    
    for y in range(HEIGHT - 1, 0, -1):
        current_hamiltonian_cycle.append((x - 1, y))

output_stream = Log_Stream()

current_state = [current_hamiltonian_cycle[0], current_hamiltonian_cycle[1]]

found_optimal_cycle = False

current_apple_position = None

# output_stream.log_new_apple_pos(current_apple_position)
output_stream.log_size((WIDTH, HEIGHT))
output_stream.log_restrictions(RESTRICTED_TILES)
output_stream.log_new_snake_pos(current_state)
output_stream.log_new_hamilton(current_hamiltonian_cycle)


def find_new_apple_position():
    '''
    Find a new position for the apple that is not a restricted space, or part of the snake
    '''
    found_new_pos = False

    while not found_new_pos:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)

        found_new_pos = (x, y) not in RESTRICTED_TILES and (x,y) not in current_state
    
    return (x, y)

while len(current_state) < AVAILABLE_TILES:

    if current_apple_position is None:
        # Apple has been eaten, spawn a new one

        current_apple_position = find_new_apple_position()

        output_stream.log_new_apple_pos(current_apple_position) # log the new apple position

        found_optimal_cycle = False

    if not found_optimal_cycle:
        # We have not found a new cycle based on a optimal a* path

        # find the optimal path to the apple
        optimal_path = pathfinding.astar(WIDTH, HEIGHT, current_state[-1], current_apple_position, RESTRICTED_TILES)

        if optimal_path:
            # Pathfinding succeded!

            # Merge the optimal path and the current snake locations to find the total path
            optimal_path.pop(0)
            snake_positions = current_state.copy()

            full_path = snake_positions + optimal_path

            grid = gen_cycle.Grid(WIDTH, HEIGHT) # create a new grid

            # Force the hamiltonian cycle to follow this new path
            grid.enforce_path(full_path)

            # Force the hamiltonian cycle to go around the restricted tiles
            for r_x, r_y in RESTRICTED_TILES:
                grid.nodes[r_y][r_x].disconnect_from_all_but(())

            # Try to find a new hamiltonian cycle
            new_cycle = gen_cycle.solve_hamiltonian(grid)

            if new_cycle is not None:
                # Cycle was found!
                current_hamiltonian_cycle = [grid.calculate_coordinate(node_id) for node_id in new_cycle]

                output_stream.log_new_hamilton(current_hamiltonian_cycle)

                found_optimal_cycle = True
    
    if current_hamiltonian_cycle is None:
        current_apple_position = None
        continue

    # Apply the next step of the hamiltonian path
    # locate the head in the path
    head_index = current_hamiltonian_cycle.index(current_state[-1])

    next_index = head_index + 1
    if next_index == len(current_hamiltonian_cycle):
        next_index = 0

    next_position = current_hamiltonian_cycle[next_index]

    if next_position in current_state:
        # Special case! hamiltonian cycle was given in reverse order to the direction of the snake
        # We will just reverse the cycle, and retry

        current_hamiltonian_cycle = current_hamiltonian_cycle[::-1]

        head_index = current_hamiltonian_cycle.index(current_state[-1])

        next_index = head_index + 1
        if next_index == len(current_hamiltonian_cycle):
            next_index = 0

        next_position = current_hamiltonian_cycle[next_index]

    if next_position == current_apple_position:
        current_apple_position = None
    else:
        current_state.pop(0)

    current_state.append(next_position)

    output_stream.log_new_snake_pos(current_state)
