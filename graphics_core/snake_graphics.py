from . import tileGraphics
import ast
import os
import time

# WIDTH = 6
# HEIGHT = 6

# RESTRICTED_TILES = [(1, 1), (2, 1), (3, 4), (4, 4)]

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

class SnakeWindow:
    def __init__(self, width, height, rough_percent = .5):
        self.width = width
        self.height = height
        
        self.window = tileGraphics.graphics(width, height, roughPercent=rough_percent)

        self.current_snake_pos = []
        self.current_apple_pos = None

        self.sprites = tileGraphics.spriteManager(self.window, os.path.join(os.path.dirname(__file__), 'sprites'))

        self.run_path_overlay = False
        self.path = []

        self.loop_path = True

        self.pathcolor = 1
        self.path_on_top = False

        self.obstacles = []

    def update_snake_pos(self, position_list):

        # First, remove the old snake position
        for x, y in self.current_snake_pos:
            self.window.removeSprite(x, y)

        # Update with the new snake position
        self.current_snake_pos = position_list.copy()

        self.draw_snake()
    
    def draw_snake(self):

        # Render the new snake pos

        # Render body
        for tail_index in range(1, len(self.current_snake_pos) - 1):
            current_pos = self.current_snake_pos[tail_index]

            tile_name = determine_tail_sprite(self.current_snake_pos[tail_index - 1], self.current_snake_pos[tail_index], self.current_snake_pos[tail_index + 1])
        
            self.window.putSprite(*current_pos, self.sprites.get(tile_name))

        # Render head
        head_direction = single_direction(self.current_snake_pos[-2], self.current_snake_pos[-1])
        self.window.putSprite(*self.current_snake_pos[-1], self.sprites.get(f'head{head_direction}'))

        # Render tail
        tail_direction = single_direction(self.current_snake_pos[0], self.current_snake_pos[1])
        self.window.putSprite(*self.current_snake_pos[0], self.sprites.get(f'rear{tail_direction}'))
        self.path_on_top = False

        self.check_path_render() # Since we just updated some sprites, make sure the path is still rendered right
    
    def update_apple_pos(self, new_apple_position):

        if self.current_apple_pos is not None:
            self.window.removeSprite(*self.current_apple_pos)

        self.current_apple_pos = new_apple_position

        self.draw_apple()
    
    def draw_apple(self):

        if self.current_apple_pos is None:
            return

        self.window.putSprite(*self.current_apple_pos, self.sprites.get('apple'))
        self.path_on_top = False
    
        self.check_path_render() # Since we just updated some sprites, make sure the path is still rendered right

    def check_path_render(self):

        if not self.run_path_overlay:
            return
        
        self.draw_path()

    def update_path(self, path):
        self.path = path
        self.run_path_overlay = True

        self.window.fill(0) # Clear old path

        # Re-render objects:
        self.draw_snake()
        self.draw_obstascles()
        self.draw_apple()

        self.draw_path()

    def draw_path(self):

        if self.path_on_top:
            return

        for index in range(len(self.path) - 1):
            self.window.line(self.path[index], self.path[index + 1], self.pathcolor, width = 5)
        
        if self.loop_path and len(self.path) != 0:
            self.window.line(self.path[0], self.path[-1], self.pathcolor, 5)

        self.path_on_top = True
    
    def update_window(self):
        self.window.update()

    def update_obstacles(self, positions):

        self.obstacles = positions

        self.draw_obstascles()

    def draw_obstascles(self):

        for pos in self.obstacles:
            self.window.putSprite(*pos, self.sprites.get('rock'))

        self.path_on_top = False
