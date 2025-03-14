import itertools
import numpy as np

#gpt generated


def generate_complete_graph(num_nodes):
    """Generates a complete graph with random edge weights."""
    np.random.seed(42)
    graph = np.random.randint(10, 100, size=(num_nodes, num_nodes))
    np.fill_diagonal(graph, 0)
    return graph

def held_karp(graph):
    """Solves the TSP using Held-Karp (Dynamic Programming + Bitmasking)."""
    n = len(graph)
    dp = {}

    # Base case: Direct path from start node (0) to every other node
    for i in range(1, n):
        dp[(frozenset([0, i]), i)] = (graph[0][i], 0)

    # Iterate over subsets of increasing size
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            subset = frozenset([0] + list(subset))

            for j in subset - {0}:  # Exclude 0 as last node
                min_cost = float('inf')
                prev_node = None

                for k in subset - {0, j}:  # Transition from k -> j
                    if (subset - {j}, k) in dp:  # Ensure key exists
                        cost = dp[(subset - {j}, k)][0] + graph[k][j]
                        if cost < min_cost:
                            min_cost = cost
                            prev_node = k

                dp[(subset, j)] = (min_cost, prev_node)

    # Compute the minimum cost to return to node 0
    full_set = frozenset(range(n))
    min_cost = float('inf')
    last_node = None

    for j in range(1, n):
        if (full_set, j) in dp:  # Ensure key exists before lookup
            cost = dp[(full_set, j)][0] + graph[j][0]
            if cost < min_cost:
                min_cost = cost
                last_node = j

    if last_node is None:
        raise ValueError("Failed to determine the optimal last node!")

    # Reconstruct the optimal path
    path = [0]
    subset = full_set

    while last_node is not None:
        path.append(last_node)
        next_subset = subset - {last_node}

        if (subset, last_node) in dp:
            last_node = dp[(subset, last_node)][1]
        else:
            break  # Prevent KeyError

        subset = next_subset

    path.append(0)  # Return to start
    return min_cost, path[::-1]  # Reverse the path

if __name__ == "__main__":
    num_nodes = 20  # Adjust as needed
    graph = generate_complete_graph(num_nodes)

    print("Adjacency Matrix (Graph):")
    print(graph)

    min_cost, path = held_karp(graph)

    print("\nOptimal TSP Tour:", path)
    print("Minimum Cost of Tour:", min_cost)
