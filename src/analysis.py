def check_hamiltonian_cycle(graph):
    """
    Determine if a Hamiltonian cycle is possible in the given graph.

    Args:
        graph (dict): A dictionary adjacency list representing the graph.

    Returns:
        str: 'EXIST', 'NOT EXIST', or 'POSSIBLE'.
    """
    n = len(graph)  # Number of nodes in the graph

    # Check for cardinality 1 nodes (isolated or degree 1 nodes)
    for node, neighbors in graph.items():
        if len(neighbors) < 2:
            return 'NOT EXIST'

    # Check Dirac's theorem: All nodes must have degree >= n/2 in an undirected graph
    # (For simplicity, we consider degree as the sum of in-degree and out-degree)
    for node in graph:
        degree = len(graph[node]) + sum(node in graph[neighbor] for neighbor in graph if neighbor != node)
        if degree < n / 2:
            return 'EXIST'

    # Check if the graph has a strongly connected component containing all nodes
    # This is a necessary (but not sufficient) condition for Hamiltonian cycle
    if not is_strongly_connected(graph):
        return 'NOT EXIST'

    # If no conditions fail, we assume it is possible
    return 'POSSIBLE'

def is_strongly_connected(graph):
    """
    Check if the graph is strongly connected using a DFS-based approach.

    Args:
        graph (dict): A dictionary adjacency list representing the graph.

    Returns:
        bool: True if the graph is strongly connected, False otherwise.
    """
    def dfs(start, visited, graph):
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(graph[node])
    
    # Check if all nodes are reachable from any start node
    for start_node in graph:
        visited = set()
        dfs(start_node, visited, graph)
        if len(visited) != len(graph):
            return False

    # Reverse the graph and check connectivity again
    reversed_graph = {node: [] for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            reversed_graph[neighbor].append(node)

    for start_node in reversed_graph:
        visited = set()
        dfs(start_node, visited, reversed_graph)
        if len(visited) != len(graph):
            return False

    return True

def main():
    grdodec = { 0: [1, 4, 5],
                1: [0, 7, 2],
                2: [1, 9, 3],
                3: [2, 11, 4],
                4: [3, 13, 0],
                5: [0, 14, 6],
                6: [5, 16, 7],
                7: [6, 8, 1],
                8: [7, 17, 9],
                9: [8, 10, 2],
                10: [9, 18, 11],
                11: [10, 3, 12],
                12: [11, 19, 13],
                13: [12, 14, 4],
                14: [13, 15, 5],
                15: [14, 16, 19],
                16: [6, 17, 15],
                17: [16, 8, 18],
                18: [10, 19, 17],
                19: [18, 12, 15] }
    
    result = check_hamiltonian_cycle(grdodec)
    print(result)

    grherschel = { 0: [1, 9, 10, 7],
                1: [0, 8, 2],
                2: [1, 9, 3],
                3: [2, 8, 4],
                4: [3, 9, 10, 5],
                5: [4, 8, 6],
                6: [5, 10, 7],
                7: [6, 8, 0],
                8: [1, 3, 5, 7],
                9: [2, 0, 4],
                10: [6, 4, 0] }
    
    result = check_hamiltonian_cycle(grherschel)
    print(result)

if __name__ == '__main__':
    main()