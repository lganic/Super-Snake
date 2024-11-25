from src import gen_cycle
import random

WIDTH = 6
HEIGHT = 6

initial_state = [(0, 0), (1, 0), (2, 0)]

restricted_tiles = [(1, 1), (2, 1), (3, 4), (4, 4)]

grid = gen_cycle.Grid(WIDTH , HEIGHT)

grid.enforce_path(initial_state)

for x, y in restricted_tiles:
    grid.nodes[y][x].disconnect_from_all_but(())

path = gen_cycle.solve_hamiltonian(grid)

print(path)