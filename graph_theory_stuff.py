import random
import numpy as np

original_graph = np.array([[0,0,0,0,0],
                          [3,0,0,0,0],
                          [3,2,0,0,0],
                          [5,1,2,0,0],
                          [3,5,3,4,0]])

working_graph = np.array([[0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0]])

new_graph = np.array([[0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0]])



##for complete graphs only
#algo 1: 
    #1. choose node at random  
    #2. choose it's lowest weighted edge
    #3. select that edge, add to new graph
    #4. is new graph full?
        #if yes, stop, return hamiltonian cycle
        #if no, continue. 

#choose node at random from nonzero elements:
      
# Flatten the array
flat_array = original_graph.flatten()

# Filter out zero elements
nonzero_indices = np.nonzero(flat_array)[0]
nonzero_elements = flat_array[nonzero_indices]

# Choose a random non-zero element
random_index = np.random.choice(len(nonzero_indices))
random_element = nonzero_elements[random_index]

# Get the location (row, column) of the randomly chosen element
random_row, random_col = np.unravel_index(nonzero_indices[random_index], original_graph.shape)

random_elt_loc = (random_row, random_col)
print("random element", random_element)
print("Location of random element", random_row, ",", random_col)
print(random_elt_loc)

ordered_pair = random_elt_loc
#if i is greater than j - - if there's more elts in its row vs column:
if ordered_pair[0] > ordered_pair[1]:
    #use random elt's row to pull next node
    next_choice_row = ordered_pair[0]
    next_selection = original_graph[next_choice_row,:]
else:
    next_choice_column = ordered_pair[1]
    next_selection = original_graph[:,next_choice_column]


#choose random neighbor from it's row or column depending on which has more
