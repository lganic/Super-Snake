import sys
sys.path.append("..") # Expose src module so the file can be run in place

from src import gen_cycle

import tileGraphics

SIZE = 6

g = tileGraphics.graphics(SIZE, SIZE, roughPercent=.7)
g.fill(7)

g.outline(0)

sprt = tileGraphics.sprite(g, 'ball.png', backgroundColor=(255,255,255))

# for x in range(SIZE):
#     for y in range(SIZE):
#         g.putSprite(x, y, sprt)


grid = gen_cycle.Grid(SIZE, SIZE)

for y in range(SIZE):
    for x in range(SIZE):

        ids = grid.nodes[y][x].connection_ids()

        for x2, y2 in [grid.calculate_coordinate(k) for k in ids]:
            g.line((x, y), (x2, y2), 1, 5)

g.update()
g.screenshot('grid.png')

path = [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3)][::-1]

for i in range(len(path) - 1):
    g.line(path[i], path[i+1], (0, 200, 0), width = 25)


g.putSprite(2, 5, sprt)

g.update()
g.screenshot('snake.png')


tgt_path = [(1, 1), (1, 2), (2,2), (2,3), (2,4), (2, 5)]

for i in range(len(tgt_path) - 1):
    g.line(tgt_path[i], tgt_path[i+1], (235, 116, 52), width = 25)


g.update()
g.screenshot('path.png')


total_path = path[:-1] + tgt_path

grid.enforce_path(total_path)

g.fill(7)

g.outline(0)

# for x in range(SIZE):
#     for y in range(SIZE):
#         g.putSprite(x, y, sprt)


for y in range(SIZE):
    for x in range(SIZE):

        ids = grid.nodes[y][x].connection_ids()

        for x2, y2 in [grid.calculate_coordinate(k) for k in ids]:
            g.line((x, y), (x2, y2), 1, 5)

for i in range(len(path) - 1):
    g.line(path[i], path[i+1], (0, 200, 0), width = 25)

for i in range(len(tgt_path) - 1):
    g.line(tgt_path[i], tgt_path[i+1], (235, 116, 52), width = 25)

g.putSprite(2, 5, sprt)

g.screenshot('isolate.png')


ham = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (4, 1), (4, 2), (5, 2), (5, 3), (4, 3), (4, 4), (5, 4), (5, 5), (4, 5), (3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (2, 1), (1, 1), (1, 2), (2, 2), (2, 3), (2, 4), (2, 5), (1, 5), (0, 5), (0, 4), (1, 4), (1, 3), (0, 3), (0, 2), (0, 1), (0, 0)]


g.fill(7)

g.outline(0)


# for x in range(SIZE):
#     for y in range(SIZE):
#         g.putSprite(x, y, sprt)


for i in range(len(ham) - 1):
    g.line(ham[i], ham[i+1], 1, width = 10)

for i in range(len(path) - 1):
    g.line(path[i], path[i+1], (0, 200, 0), width = 25)


for i in range(len(tgt_path) - 1):
    g.line(tgt_path[i], tgt_path[i+1], (235, 116, 52), width = 25)

g.putSprite(2, 5, sprt)

g.screenshot('goodpath.png')

while True:
    g.update()
