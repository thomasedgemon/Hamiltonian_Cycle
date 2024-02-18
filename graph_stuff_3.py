import random
#using different storage types for perhaps easier parsing of vertices and their edges

A_edges = ["B", "C", "D", "E"]
B_edges = ["C", "D", "E"]
C_edges = ["D", "E"]
D_edges = ["E"]

A_weights = [3, 3, 5, 3]
B_weights = [2, 1, 5]
C_weights = [2, 3]
D_weights = [4]
#________________________
Edges =         ["AB", "AC", "AD", "AE", "BC", "BD", "BE", "CD", "CE", "DE"]
Edge_weights =  [  3,    3,   5,     3,    2,    1,   5,     2,    3,   4]
#________________________
graph = {
    "AB": 3,
    "AC": 3,
    "AD": 5,
    "AE": 3,
    "BC": 2,
    "BD": 1,
    "BE": 5,
    "CD": 2,
    "CE": 3,
    "DE": 4
}

working_graph = {}
new_graph = {}
#_______________________
#choose a vertex at random, since this is a complete graph.
random_edge = random.choice(list(graph.keys()))
print(f"random edge:", random_edge)
first_vertex = random_edge[0]
print(f"first vertex:", first_vertex)
# Filter edges connected to the vertex
edges_connected_to_vertex = {k: v for k, v in graph.items() if k[0] == first_vertex}
print(f"edges connected to vertex:", edges_connected_to_vertex)
#find MWE connected to first vertex.
min_weight_edge = min(edges_connected_to_vertex, key=edges_connected_to_vertex.get)
print("Edge with the lowest weight connected to vertex", first_vertex, ":", min_weight_edge)
#parse next vertex from MWE 
next_vertex = min_weight_edge[0]


