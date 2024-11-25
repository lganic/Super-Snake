import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y) coordinates on the grid
        self.parent = parent      # Parent node in the path

        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost to goal
        self.f = 0  # Total cost

    def __lt__(self, other):
        return self.f < other.f

def astar(grid_size, start, end, blocked_nodes):
    """
    Perform A* pathfinding on a grid.
    """
    # Convert blocked_nodes to a set for faster lookup
    blocked_set = set(blocked_nodes)

    # Initialize the open and closed lists
    open_list = []
    closed_set = set()

    # Create the start node and add it to the open list
    start_node = Node(start)
    heapq.heappush(open_list, start_node)

    while open_list:
        # Get the node with the lowest f score
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)

        # Check if we have reached the goal
        if current_node.position == end:
            # Reconstruct the path by retracing parents
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        # Generate neighbors (adjacent squares)
        x, y = current_node.position
        neighbors = [
            (x - 1, y),  # Left
            (x + 1, y),  # Right
            (x, y - 1),  # Up
            (x, y + 1)   # Down
        ]

        for neighbor_pos in neighbors:
            # Check if neighbor is within bounds
            if (0 <= neighbor_pos[0] < grid_size) and (0 <= neighbor_pos[1] < grid_size):
                # Skip if the node is blocked or already evaluated
                if neighbor_pos in blocked_set or neighbor_pos in closed_set:
                    continue

                # Create a neighbor node
                neighbor_node = Node(neighbor_pos, current_node)
                neighbor_node.g = current_node.g + 1
                # Use Manhattan distance as heuristic
                neighbor_node.h = abs(neighbor_pos[0] - end[0]) + abs(neighbor_pos[1] - end[1])
                neighbor_node.f = neighbor_node.g + neighbor_node.h

                # Check if this neighbor is in the open list with a lower g score
                skip_neighbor = False
                for open_node in open_list:
                    if neighbor_node.position == open_node.position and neighbor_node.g >= open_node.g:
                        skip_neighbor = True
                        break

                if not skip_neighbor:
                    heapq.heappush(open_list, neighbor_node)

    # If we reach here, no path was found
    return None

if __name__ == "__main__":
    n = 10  # Grid size (10x10 grid)
    start = (0, 0)
    end = (7, 7)
    blocked_nodes = [
        (1, 1), (1, 2), (1, 3), (1, 4),
        (2, 1), (3, 1), (4, 1),
        (5, 5), (5, 6), (5, 7),
        (6, 5), (7, 5)
    ]

    path = astar(n, start, end, blocked_nodes)
    if path:
        print("Path found:")
        for step in path:
            print(step)
    else:
        print("No path found.")

    # Visualization
    # Initialize the grid
    grid = [['.' for _ in range(n)] for _ in range(n)]
    for x, y in blocked_nodes:
        grid[y][x] = '#'  # Note: grid[y][x] because y is row index, x is column index

    if path:
        for x, y in path:
            grid[y][x] = 'O'
        x_s, y_s = start
        x_e, y_e = end
        grid[y_s][x_s] = 'S'
        grid[y_e][x_e] = 'E'

    print("\nGrid:")
    for row in grid:
        print(' '.join(row))
