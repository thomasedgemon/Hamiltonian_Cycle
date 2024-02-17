#####utilizing igraph#####
import igraph as ig
import numpy as np
import random
#import matplotlib.pyplot as plt

#instantiate original graph
original_graph = ig.Graph()

#instantiate new graph to be built as we go
new_graph = ig.Graph(5)

original_graph.add_vertices(5)
original_graph.vs["name"] = ["A", "B", "C", "D", "E"]

#add weighted edges
original_graph.add_edge(0,1, weight = 7)
original_graph.add_edge(0,2, weight = 5)
original_graph.add_edge(0,3, weight = 1)
original_graph.add_edge(0,4, weight = 9)
original_graph.add_edge(1,2, weight = 5)
original_graph.add_edge(1,3, weight = 7)
original_graph.add_edge(1,4, weight = 3)
original_graph.add_edge(2,3, weight = 7)
original_graph.add_edge(2,4, weight = 2)
original_graph.add_edge(3,4, weight = 4)

#instantiate working graph after edges are added to original. both will start the same. 
working_graph = original_graph

#since we are using a complete graph, we can choose a starting vertex at random,
#as none of them are more connected than any other one

first_vertex = random.choice(original_graph.vs)
print(first_vertex)
#add this vertex to the new graph, and delete it from the working graph


#recursive function to choose lowest weighted edges for each subsequent vertex. 
    #starting with the vertex chosen above, choose its edge which has the lowest weight