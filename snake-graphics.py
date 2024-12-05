import tileGraphics
import ast
import time

# WIDTH = 6
# HEIGHT = 6

# RESTRICTED_TILES = [(1, 1), (2, 1), (3, 4), (4, 4)]

LOG_FILE = 'log-c3.txt'

def parse_line(line):
    # Determine the type of the line
    if line.startswith("SNAKE:"):
        data_type = "SNAKE"
        data_str = line[len("SNAKE:"):].strip()
    elif line.startswith("APPLE:"):
        data_type = "APPLE"
        data_str = line[len("APPLE:"):].strip()
    elif line.startswith("HAMIL:"):
        data_type = "HAMIL"
        data_str = line[len("HAMIL:"):].strip()
    elif line.startswith("OBJS:"):
        data_type = "OBJS"
        data_str = line[len("OBJS:"):].strip()
    elif line.startswith("SIZE:"):
        data_type = "SIZE"
        data_str = line[len("SIZE:"):].strip()
    else:
        raise ValueError("Unknown line format")
    
    # Parse the data part
    try:
        data = ast.literal_eval(data_str)
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"Invalid data format: {e}")
    
    return data_type, data

log_file = open(LOG_FILE, 'r')

_, (WIDTH, HEIGHT) = parse_line(log_file.readline())
_, RESTRICTED_TILES = parse_line(log_file.readline())

current_state = None
current_apple_pos = (WIDTH - 1, HEIGHT - 1)
current_path = []

g = tileGraphics.graphics(WIDTH, HEIGHT, roughPercent= .6)

sprites = tileGraphics.spriteManager(g, 'sprites')

for location in RESTRICTED_TILES:
    g.putSprite(*location, sprites.get('rock'))

g.outline(7)

while not g.checkKey(tileGraphics.keycodes['SPACE']):
    g.update()

def determine_tail_sprite(previous_pos, current_pos, next_pos):
    px, py = previous_pos
    cx, cy = current_pos
    nx, ny = next_pos

    if (px < cx and nx > cx) or (nx < cx and px > cx):
        # Horizontal Left-Right
        return 'tail24'
    elif (px < cx and ny > cy) or (nx < cx and py > cy):
        # Angle Left-Down
        return 'tail34'
    elif (py < cy and ny > cy) or (ny < cy and py > cy):
        # Vertical Up-Down
        return 'tail13'
    elif (py < cy and nx < cx) or (ny < cy and px < cx):
        # Angle Top-Left
        return 'tail14'
    elif (px > cx and ny < cy) or (nx > cx and py < cy):
        # Angle Right-Up
        return 'tail12'
    elif (py > cy and nx > cx) or (ny > cy and px > cx):
        # Angle Down-Right
        return 'tail23'

    return 'unknown'  # Default case if no condition matches

def single_direction(from_pos, to_pos):
    delta_x = to_pos[0] - from_pos[0]
    delta_y = to_pos[1] - from_pos[1]

    if delta_y == -1:
        return 1
    
    if delta_x == 1:
        return 2
    
    if delta_y == 1:
        return 3
    
    if delta_x == -1:
        return 4


log_file = open(LOG_FILE, 'r')

for line in log_file.readlines():
    data_type, data = parse_line(line)

    if data_type == "APPLE":
        current_apple_pos = data
    
    if data_type == 'SNAKE':
        current_state = data
    
    if data_type == 'HAMIL':

        current_path = data

    if current_state is None:
        continue

    g.fill(0)
        
    for x, y in RESTRICTED_TILES:
        g.putSprite(x, y, sprites.get('rock'))

    g.putSprite(*current_apple_pos, sprites.get('apple'))

    for tail_index in range(1, len(current_state) - 1):
        current_pos = current_state[tail_index]

        tile_name = determine_tail_sprite(current_state[tail_index - 1], current_state[tail_index], current_state[tail_index + 1])
    
        g.putSprite(*current_pos, sprites.get(tile_name))

    head_direction = single_direction(current_state[-2], current_state[-1])
    g.putSprite(*current_state[-1], sprites.get(f'head{head_direction}'))

    tail_direction = single_direction(current_state[0], current_state[1])
    g.putSprite(*current_state[0], sprites.get(f'rear{tail_direction}'))

    g.outline(7)

    t = time.time()

    if data_type == "APPLE":
        pass
    
    if data_type == 'SNAKE':
        while time.time() - t < .1:
            g.update()





t = time.time()
while time.time() - t < 2:
    g.update()





log_file = open(LOG_FILE, 'r')

for line in log_file.readlines():
    data_type, data = parse_line(line)

    if data_type == "APPLE":
        current_apple_pos = data
    
    if data_type == 'SNAKE':
        current_state = data
    
    if data_type == 'HAMIL':
        current_path = data

    g.fill(0)
        
    for x, y in RESTRICTED_TILES:
        g.putSprite(x, y, sprites.get('rock'))

    g.putSprite(*current_apple_pos, sprites.get('apple'))

    for tail_index in range(1, len(current_state) - 1):
        current_pos = current_state[tail_index]

        tile_name = determine_tail_sprite(current_state[tail_index - 1], current_state[tail_index], current_state[tail_index + 1])
    
        g.putSprite(*current_pos, sprites.get(tile_name))

    head_direction = single_direction(current_state[-2], current_state[-1])
    g.putSprite(*current_state[-1], sprites.get(f'head{head_direction}'))

    tail_direction = single_direction(current_state[0], current_state[1])
    g.putSprite(*current_state[0], sprites.get(f'rear{tail_direction}'))

    for index in range(len(current_path) - 1):
        g.line(current_path[index], current_path[index + 1], 1, width = 5)
    
    if len(current_path) != 0:
        g.line(current_path[0], current_path[-1], 1, 5)

    g.outline(7)

    t = time.time()

    if data_type == "APPLE":
        pass
    
    if data_type == 'SNAKE':
        while time.time() - t < .1:
            g.update()

    if data_type == 'HAMIL':
        while time.time() - t < .3:
            g.update()