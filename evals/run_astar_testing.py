import sys
sys.path.append("..") # Expose src module so the file can be run in place

import random

from matplotlib import pyplot as plt
from tqdm import tqdm

import data_collection
from src import pathfinding
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

    for _ in tqdm(range(TEST_COUNT), 'Running A* Snake'):

        current_snake_pos = INITIAL_POS.copy()

        # g.update_snake_pos(current_snake_pos)

        recordkeeper = data_collection.Length_Tracker()
        recordkeeper.add(current_snake_pos)

        while len(current_snake_pos) < WIDTH * HEIGHT:
            current_apple_pos = find_new_apple_pos(current_snake_pos)
            # g.update_apple_pos(current_apple_pos)

            path = pathfinding.astar(WIDTH, HEIGHT, current_snake_pos[-1], current_apple_pos, current_snake_pos)

            if path is None:
                break

            path = path[1:] # Remove redundant head node

            while path:
                new_item = path.pop(0)

                if path:
                    current_snake_pos.pop(0) # Ignore O(n) time complexity here, this doesn't need to be performant

                current_snake_pos.append(new_item) # More O(n)

                recordkeeper.add(current_snake_pos)
                # g.update_snake_pos(current_snake_pos)


                # g.update_window()

                # import time
                # t = time.time()
                # while time.time() - t < .1:
                #     g.update_window()
            
        all_tracks.add_record(recordkeeper.records)
    
    return all_tracks


# for trace in all_tracks.all_records:
    
#     x = list(range(len(trace)))

#     plt.plot(x, trace)

# plt.title('Snake Length over A* Trials in 6x6 Grid')
# plt.show()

if __name__ == '__main__':
    N = 100000

    all_tracks = data_collect()

    avgs = all_tracks.avg_track()

    plt.plot(list(range(len(avgs))), avgs)
    plt.title('Average Snake Length over A* Trials in 6x6 Grid')
    plt.xlabel('Final Length')
    plt.ylabel('Number of Times')
    plt.show()


    plt.hist(all_tracks.max_lengths())
    plt.title('Snake Lengths for 6x6 A* Trials')
    plt.xlabel('Final Length')
    plt.ylabel('Number of Times')
    plt.show()