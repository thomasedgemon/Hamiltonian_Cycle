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
#__________________________________________________________________
#recursive function to choose lowest weighted edges for each subsequent vertex. 
## or a for loop of length n+1 since the first vertex must also be used for the end

    #1. starting with the vertex chosen above, choose its edge which has the lowest weight
    #2. delete edge from working graph, add that edge to new graph.
    #(subsequent steps can be iterated via for loop or recursion)
    #3. choose lowest edge of next vertex. add that edge to the new graph, delete it from working graph
    #4. delete that vertex's other edges from working graph
    #5. go back to number three. choose any edge except that which goes to the starting vertex.
    
    #does the new graph contain every vertex? does it contain n+1 edges? if so, done. if not, start over. 
    #(is there a way to go back a few steps rather than starting over from scratch? would be faster. what is probability
    # of getting HC on the first try )

    #to avoid (O)n^2, how do we avoid checking the same route twice? what are the odds the same one will be randomly chosen again? what about a very similar one? what are the odds of choosing
        #the first N same vertices?

    #at what point do we check that one even exists, much less an optimal one?
#____________________________________________________________________
#find all of first_vertex edges
incident_edges = original_graph.incident(first_vertex)
