import igraph as ig
from igraph import Graph

#instantiate graph with weight attributes
g = ig.Graph(n=5, edges=[['a', 'e', 5], ['a', 'b', 3], ['a', 'd', 2], ['b', 'e', 1], ['b', 'c', 4], ['b','d', 5], ['c', 'd', 3], ['c', 'e', 3], ['d','e', 2] ])


#delete duplicate edges. this method DOES NOT truly delete duplicates if input is every edge.
#for example, igraph doesnt recognize (1,2) and (2,1) as the same.
#either the user must omit those from input, or a function
#must be created to parse it a different way.

# this is for removing duplicates: may not be needed: g = g.simplify(multiple=True, loops=True)
#for edge in g.es:

#create working graph to delete edges from
g_working = g


#instantiate algo to be used on working graph

