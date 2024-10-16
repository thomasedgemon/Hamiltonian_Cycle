import networkx as nx
import numpy as np
import random
from itertools import islice, permutations
from concurrent.futures import ProcessPoolExecutor
import math  # Import the standard math library directly

# Create a fully connected graph with 10 nodes
num_nodes = 10
G = nx.complete_graph(num_nodes)

# Assign random weights between 1 and 10 to each edge
for (u, v) in G.edges():
    G[u][v]['weight'] = random.randint(1, 10)

# Convert the graph to a numpy array (adjacency matrix)
adj_matrix = nx.to_numpy_array(G, weight='weight')

# Function to calculate the Hamiltonian cycle weight for a given cycle
def cycle_weight(graph, cycle):
    return sum(graph[cycle[i]][cycle[i + 1]]['weight'] for i in range(len(cycle) - 1))

# Function to find the shortest Hamiltonian cycle in a given chunk of permutations
def find_shortest_cycle(graph, start_node, perm_start, perm_end):
    min_weight = float('inf')
    best_cycle = None

    # Generate only a chunk of permutations at a time
    nodes = list(graph.nodes)
    nodes.remove(start_node)
    for perm in islice(permutations(nodes), perm_start, perm_end):
        cycle = [start_node] + list(perm) + [start_node]
        weight = cycle_weight(graph, cycle)

        if weight < min_weight:
            min_weight = weight
            best_cycle = cycle

    return best_cycle, min_weight

# Main function to find the shortest Hamiltonian cycle using multiprocessing
def parallel_find_shortest_hamiltonian_cycle(graph, start_node=0, num_workers=2):
    total_permutations = math.factorial(num_nodes - 1)  # Use math.factorial instead of np.math.factorial
    chunk_size = total_permutations // num_workers

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(
                find_shortest_cycle, graph, start_node, i, i + chunk_size
            ) for i in range(0, total_permutations, chunk_size)
        ]
        results = [future.result() for future in futures]

    # Find the minimum cycle among all results
    shortest_cycle, min_weight = min(results, key=lambda x: x[1])
    return shortest_cycle, min_weight

# Use the __name__ guard
if __name__ == '__main__':
    shortest_cycle, min_cycle_weight = parallel_find_shortest_hamiltonian_cycle(G)

    # Create a subgraph for the Hamiltonian cycle
    cycle_edges = [(shortest_cycle[i], shortest_cycle[i + 1]) for i in range(len(shortest_cycle) - 1)]
    hamiltonian_cycle_graph = nx.Graph()
    hamiltonian_cycle_graph.add_edges_from(cycle_edges)

    # Add weights to the Hamiltonian cycle adjacency matrix
    hamiltonian_cycle_adj_matrix = np.zeros((num_nodes, num_nodes))
    for u, v in cycle_edges:
        weight = G[u][v]['weight']
        hamiltonian_cycle_adj_matrix[u, v] = weight
        hamiltonian_cycle_adj_matrix[v, u] = weight  # Since the graph is undirected

    # Print the numpy arrays
    print("Original Graph Adjacency Matrix:\n", adj_matrix)
    print("Hamiltonian Cycle Adjacency Matrix with Weights:\n", hamiltonian_cycle_adj_matrix)
