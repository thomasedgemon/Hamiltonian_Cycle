import numpy
import random


#instantiate empty square matrix to be filled by user. TL to BR should be null entries, as a vertex cannot be connected to itself.
# the values in the matrix are the weights themselves. 

vertex_total = int(input("how many vertices are there?: "))

graph_matrix = [[0 for _ in range(vertex_total)] for _ in range(vertex_total)]

#populate matrix
for i in range(0, vertex_total):
    for x in range(0, vertex_total):
        graph_matrix[i][x] = int(input("what is the next value in row? : "))


print(graph_matrix)
#print(min(graph_matrix))
HC = None
working_graph = graph_matrix



#algo
    #choose a row with lowest entry sum? choose the lowest sum across the entire matrix.
    #if-else within a for loop?
    #placeholder = NULL
    #for i in range(0, vertex_total):
        #for x in range(0, vertex_total):
            #if graph_matrix[i+1][x+1] < graph_matrix[i][x]
                #placeholder = [i][x]
                #HC equal what now? can append the value itself to list, but how to relate back to its vertices?

#alternatively:
    # use min(graph_matrix), but result might be several instances of the same number. how to eliminate the copies,
    #and therefore choose an edge-set of vertices?


#optimize algo via iteration and random module.



#output 


#down the road: 
    # import data from db, or use GUI for faster data input