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
edges_and_weights = {
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
#_______________________
print(Edge_weights)