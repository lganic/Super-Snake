from tqdm import tqdm

def hamilton_cycle(graph, use_progress_bar = False):
    """
    Finds a Hamiltonian cycle in a graph represented by an adjacency list.
    Returns a list of vertices representing the cycle, or an empty list if no cycle exists.
    """

    def is_valid(v, path):
        if v not in path:
            if len(path) == 0:
                return True
            elif v in graph[path[-1]]:
                return True
        return False

    def dfs(path):
        if len(path) == len(graph):
            if path[0] in graph[path[-1]]:
                return path
            else:
                return []

        for v in graph[path[-1]]:
            if is_valid(v, path):
                new_path = path + [v]
                cycle = dfs(new_path)
                if cycle:
                    return cycle
        return []

    vertex_wrapper = graph
    if use_progress_bar:
        vertex_wrapper = tqdm(graph)

    for start_vertex in vertex_wrapper:
        cycle = dfs([start_vertex])
        if cycle:
            return cycle
    return []

if __name__ == '__main__':
    # Example usage
    graph = {
        0: [1, 2],
        1: [0, 2, 3],
        2: [0, 1, 3],
        3: [1, 2]
    }

    cycle = hamilton_cycle(graph)
    if cycle:
        print("Hamiltonian cycle found:", cycle)
    else:
        print("No Hamiltonian cycle exists.")