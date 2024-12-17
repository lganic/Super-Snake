import sys
sys.path.append("..") # Expose src module so the file can be run in place

import random

from matplotlib import pyplot as plt
from tqdm import tqdm

import data_collection
from src import pathfinding
from src import gen_cycle
from graphics_core import snake_graphics

TEST_COUNT = 1000

WIDTH = 6
HEIGHT = 6
INITIAL_POS = [(0, 0), (1, 0)]

random.seed(112358)

# g = snake_graphics.SnakeWindow(WIDTH, HEIGHT, rough_percent=.3)

def find_new_apple_pos(current_positions):
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)

    while (x, y) in current_positions:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
    
    return (x, y)

def data_collect():
    all_tracks = data_collection.All_Tracker()

    for _ in tqdm(range(TEST_COUNT), 'Running Hybrid Snake'):

        current_hamiltonian_cycle = []
        for x in range(WIDTH):
            current_hamiltonian_cycle.append((x, 0))

        for x in range(WIDTH - 1, -1, -2):
            for y in range(1, HEIGHT):
                current_hamiltonian_cycle.append((x, y))
            
            for y in range(HEIGHT - 1, 0, -1):
                current_hamiltonian_cycle.append((x - 1, y))

        current_snake_pos = INITIAL_POS.copy()

        hamilton_index = current_hamiltonian_cycle.index(current_snake_pos[-1]) + 1

        # g.update_snake_pos(current_snake_pos)

        recordkeeper = data_collection.Length_Tracker()
        recordkeeper.add(current_snake_pos)

        current_apple_pos = find_new_apple_pos(current_snake_pos)
        # g.update_apple_pos(current_apple_pos)

        found_optimal_cycle = False

        while len(current_snake_pos) < WIDTH * HEIGHT:

            if not found_optimal_cycle:
                optimal_path = pathfinding.astar(WIDTH, HEIGHT, current_snake_pos[-1], current_apple_pos, current_snake_pos)

                if optimal_path:
                    # Pathfinding success

                    # Merge the optimal path and the current snake locations to find the total path
                    optimal_path.pop(0)
                    snake_positions = current_snake_pos.copy()

                    full_path = snake_positions + optimal_path

                    grid = gen_cycle.Grid(WIDTH, HEIGHT) # create a new grid

                    # Force the hamiltonian cycle to follow this new path
                    grid.enforce_path(full_path)

                    # Try to find a new hamiltonian cycle
                    new_cycle = gen_cycle.solve_hamiltonian(grid)

                    if new_cycle is not None:
                        # Cycle was found!
                        current_hamiltonian_cycle = [grid.calculate_coordinate(node_id) for node_id in new_cycle]

                        test_index = current_hamiltonian_cycle.index(current_snake_pos[0])

                        next_index = test_index + 1
                        if next_index == WIDTH * HEIGHT:
                            next_index = 0


                        if len(current_hamiltonian_cycle) != 36:
                            print(grid.adjacency_list())
                            raise ValueError('An invalid cycle was found')

                        if current_hamiltonian_cycle[next_index] != current_snake_pos[1]:
                            # Path was given in reverse order

                            current_hamiltonian_cycle = current_hamiltonian_cycle[::-1]

                        hamilton_index = current_hamiltonian_cycle.index(current_snake_pos[-1]) + 1

                        found_optimal_cycle = True

            if hamilton_index >= WIDTH * HEIGHT:
                hamilton_index = 0

            try:
                current_snake_pos.append(current_hamiltonian_cycle[hamilton_index])
            except:
                print(current_hamiltonian_cycle)
                print(hamilton_index)
                raise ValueError('sdslf')

            if current_hamiltonian_cycle[hamilton_index] != current_apple_pos:
                current_snake_pos.pop(0) # Ignore O(n) time complexity here, this doesn't need to be performant

            elif len(current_snake_pos) != WIDTH * HEIGHT:

                current_apple_pos = find_new_apple_pos(current_snake_pos)
                found_optimal_cycle = False
                # g.update_apple_pos(current_apple_pos)

            hamilton_index += 1

            if hamilton_index >= WIDTH * HEIGHT:
                hamilton_index = 0

            recordkeeper.add(current_snake_pos)
            # g.update_snake_pos(current_snake_pos)

            # g.update_window()

            # import time
            # t = time.time()
            # while time.time() - t < 1:
            #     g.update_window()
            
        all_tracks.add_record(recordkeeper.records)
    
    return all_tracks


# for trace in all_tracks.all_records:
    
#     x = list(range(len(trace)))

#     plt.plot(x, trace)

# plt.title('Snake Length over A* Trials in 6x6 Grid')
# plt.show()

if __name__ == '__main__':
    all_tracks = data_collect()

    avgs = all_tracks.avg_track()

    plt.plot(list(range(len(avgs))), avgs)
    plt.title('Average Snake Length over Hybrid Trials in 6x6 Grid')
    plt.show()


    plt.hist(all_tracks.max_lengths())
    plt.title('Snake Lengths for 6x6 Hybrid Trials')
    plt.xlabel('Final Length')
    plt.ylabel('Number of Times')
    plt.show()