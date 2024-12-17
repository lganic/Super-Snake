from graphics_core import snake_graphics
import ast
import time

# WIDTH = 6
# HEIGHT = 6

# RESTRICTED_TILES = [(1, 1), (2, 1), (3, 4), (4, 4)]

LOG_FILE = 'log-big.txt'

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

graphics = snake_graphics.SnakeWindow(WIDTH, HEIGHT)

graphics.update_obstacles(RESTRICTED_TILES)

log_file = open(LOG_FILE, 'r')

for line in log_file.readlines():
    data_type, data = parse_line(line)

    if data_type == "APPLE":
        graphics.update_apple_pos(data)
    
    if data_type == 'SNAKE':
        graphics.update_snake_pos(data)
    
    if data_type == 'HAMIL':
        graphics.update_path(data)
        pass

    t = time.time()

    if data_type == 'SNAKE':
        while time.time() - t < .1:
            graphics.update_window()
