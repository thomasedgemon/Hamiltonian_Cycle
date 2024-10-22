import networkx as nx
import numpy as np
import random
from itertools import islice, permutations
from concurrent.futures import ProcessPoolExecutor
import math  # Import the standard math library directly
import h5py
import os

save_directory = r"C:\Users\twedgemo\Desktop\TSP_work"
filename = os.path.join(save_directory, 'graph_cycle_pairs.h5')
# Create a fully connected graph with 10 nodes
num_nodes = 10

# Function to generate a fully connected graph with random weights
def generate_fully_connected_graph(num_nodes):
    G = nx.complete_graph(num_nodes)
    for (u, v) in G.edges():
        G[u][v]['weight'] = random.randint(1, 10)
    return G

# Function to convert a graph to an adjacency matrix
def graph_to_adj_matrix(G):
    return nx.to_numpy_array(G, weight='weight')

# Function to calculate the Hamiltonian cycle weight for a given cycle
def cycle_weight(graph, cycle):
    return sum(graph[cycle[i]][cycle[i + 1]]['weight'] for i in range(len(cycle) - 1))

# Function to find the shortest Hamiltonian cycle in a given chunk of permutations
def find_shortest_cycle(graph, start_node, perm_start, perm_end):
    min_weight = float('inf')
    best_cycle = None

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
    total_permutations = math.factorial(num_nodes - 1)
    chunk_size = total_permutations // num_workers

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(
                find_shortest_cycle, graph, start_node, i, i + chunk_size
            ) for i in range(0, total_permutations, chunk_size)
        ]
        results = [future.result() for future in futures]

    shortest_cycle, min_weight = min(results, key=lambda x: x[1])
    return shortest_cycle, min_weight

# Function to generate and save graph-cycle pairs
def generate_and_save_pairs(num_pairs, filename, num_workers=8):
    # Open the HDF5 file in append mode ('a'), so it doesn't overwrite existing data
    with h5py.File(filename, 'a') as f:
        # Get the current number of pairs already in the file
        existing_pairs = len(f.keys())
        
        for i in range(num_pairs):
            G = generate_fully_connected_graph(num_nodes)
            adj_matrix = graph_to_adj_matrix(G)
            shortest_cycle, _ = parallel_find_shortest_hamiltonian_cycle(G, num_workers=num_workers)
            
            # Create a subgraph for the Hamiltonian cycle
            cycle_edges = [(shortest_cycle[i], shortest_cycle[i + 1]) for i in range(len(shortest_cycle) - 1)]
            hamiltonian_cycle_adj_matrix = np.zeros((num_nodes, num_nodes))
            for u, v in cycle_edges:
                weight = G[u][v]['weight']
                hamiltonian_cycle_adj_matrix[u, v] = weight
                hamiltonian_cycle_adj_matrix[v, u] = weight
            
            # Save the graph and cycle adjacency matrices, ensuring unique group names
            grp = f.create_group(f'pair_{existing_pairs + i}')
            grp.create_dataset('graph_matrix', data=adj_matrix)
            grp.create_dataset('cycle_matrix', data=hamiltonian_cycle_adj_matrix)

if __name__ == '__main__':
    # Number of pairs to generate
    num_pairs = 100  # You can specify this number based on your needs
    
    # Specify the filename where data will be saved
    filename = 'graph_cycle_pairs.h5'

    num_workers = 8

    # Generate and save graph-cycle pairs
    generate_and_save_pairs(num_pairs, filename)

    print(f"Saved {num_pairs} graph-cycle pairs to {filename}")

