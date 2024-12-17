from typing import List, Tuple, Union
# from .hamilton import gencon
#from .superlight import hamilton_cycle
# import z3
from hamilton_cycle_module import hamilton_cycle
from .analysis import check_hamiltonian_cycle

class Restrictable_Node:
    '''
    Track a single grid space, and what tiles
    that space can connect to
    '''

    def __init__(self, id: int):
        self.id = id

        self.connections = set()

    # NOTE: I am overriding hash and eq here because it makes instancing 
    # duplicate nodes FAR easier. Doing it this way means that two nodes
    # can be created seperately, but with the same id, and if added to a 
    # dictionary / hashmap, will reference the same key / value pair

    def __hash__(self):
        return self.id.__hash__()
    
    def __eq__(self, other_node: 'Restrictable_Node'):
        return self.id == other_node.id

    def connect(self, other_node: 'Restrictable_Node'):
        '''
        Connect this node to another
        '''

        self.connections.add(other_node)
        other_node.connections.add(self)
    
    def disconnect(self, other_node: 'Restrictable_Node'):
        '''
        Disconnect this node from another
        '''

        self.connections.remove(other_node)
        other_node.connections.remove(self)
    
    def disconnect_from_all_but(self, other_nodes: Union[List['Restrictable_Node'], Tuple['Restrictable_Node']]):
        '''
        Disconnect this node from all others,
        except for the ones specified
        '''

        for currently_connected_node in list(self.connections): # Use list to avoid runtime error

            if currently_connected_node in other_nodes:
                continue 

            self.disconnect(currently_connected_node)

    def connection_ids(self):
        '''
        Return a list of the ids of all nodes connected to this one
        '''

        return [k.id for k in self.connections]
        

class Grid:
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.nodes: List[List[Restrictable_Node]] = []

        for y in range(height):

            current_row = [Restrictable_Node(self.calculate_node_id(x, y)) for x in range(width)]

            self.nodes.append(current_row)
        
        # Grid is now created, we now need to inform the nodes of their neighbors

        # Create downward / upward connections

        for y in range(height - 1):
            for x in range(width):
                self.nodes[y][x].connect(self.nodes[y + 1][x])
        
        # Create left / right connections

        for y in range(height):
            for x in range(width - 1):
                self.nodes[y][x].connect(self.nodes[y][x + 1])
    
    def calculate_node_id(self, x, y):
        '''
        Given an x, and y, return the id of the node at that grid space
        '''

        return self.width * y + x
    
    def calculate_coordinate(self, id):
        '''
        Given the id of a node, return its coordinate
        '''

        y = id // self.width
        x = id % self.width

        return x, y

    def enforce_path(self, coordinate_list: List[Tuple[int, int]]):
        '''
        When given a path of coordinates, ensure that the nodes at
        the specified coordinates are only linked to the ones in the path

        The ends of the path are left as is
        '''

        for path_index, (x, y) in enumerate(coordinate_list):

            if path_index == 0 or path_index == len(coordinate_list) - 1:
                # We are at one of the ends
                # do nothing to this point
                
                continue

            prev_x = coordinate_list[path_index - 1][0]
            prev_y = coordinate_list[path_index - 1][1]

            next_x = coordinate_list[path_index + 1][0]
            next_y = coordinate_list[path_index + 1][1]

            prev_node = self.nodes[prev_y][prev_x]
            next_node = self.nodes[next_y][next_x]

            self.nodes[y][x].disconnect_from_all_but((next_node, prev_node))

    def adjacency_list(self):
        '''
        Represent the current state of the grid graph 
        as an adjaceny list
        '''

        output = {}

        for row in self.nodes:

            for node in row:

                output[node.id] = node.connection_ids()
                
        return output
    
def extract_cycle(model, variable_prefix='cv'):
    '''
    Extracts the Hamiltonian cycle from the Z3 model.
    Returns A list of nodes in the order they appear in the Hamiltonian cycle.
    '''
    # Extract the node positions from the model
    node_positions = {}
    for var in model.decls():
        if var.name().startswith(variable_prefix):
            node_index = int(var.name()[len(variable_prefix):])
            position = model[var].as_long()
            node_positions[node_index] = position
    # Sort the nodes by their positions
    sorted_nodes = sorted(node_positions.items(), key=lambda x: x[1])
    # Get the list of nodes in order
    cycle = [node for node, pos in sorted_nodes]
    return cycle


def solve_hamiltonian(grid: Grid) -> Union[None, List[Tuple[int, int]]]:

    adjaceny = grid.adjacency_list()

    # First, simplify the adjaceny by removing inaccessible nodes
    mapping = {}

    k = 0

    for node_id in adjaceny:
        if len(adjaceny[node_id]) == 0:
            continue

        mapping[node_id] = k
        k += 1

    new_adjaceny = {}

    for node_id in adjaceny:
        if len(adjaceny[node_id]) == 0:
            continue

        new_id = mapping[node_id]
        new_adjaceny[new_id] = [mapping[j] for j in adjaceny[node_id]]

    if check_hamiltonian_cycle(adjaceny) == 'NOT EXIST':
        # print('Ignored on analytical basis')

        return None

    # constraints = gencon(new_adjaceny)

    # # Run the SAT solver

    # status = constraints.check()

    adjacency_list = []

    for node in new_adjaceny:

        if len(new_adjaceny[node]) < 2:
            return None

        adjacency_list.append(new_adjaceny[node])

    cycle = hamilton_cycle(adjacency_list)

    if cycle:
        # Solver reached SAT
        # Path exists

        # Decompose path from model variable data
    
        # Reverse the mapping from before
        reverse_mapping = {v: k for k, v in mapping.items()}

        return [reverse_mapping[c] for c in cycle]

    else:
        # Solver did not reach SAT

        # Path probably doesn't exist

        return None


def main():

    grid = Grid(4, 4)

    test_path = [(2,0), (2,1), (2,2)]

    grid.enforce_path(test_path)

    solution = solve_hamiltonian(grid)

    if solution is None:
        print('No solution')
    else:
        print(solution)

if __name__ == '__main__':
    main()