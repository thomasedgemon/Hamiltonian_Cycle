import numpy as np
import pandas as pd

graph1 = [[0,0,0,0,0],
          [3,0,0,0,0],
          [0,4,0,0,0],
          [2,5,3,0,0],
          [5,1,3,2,0]]

graph2 = [('a','e',5), ('a','b',3), ('a','d',2), 
          ('b','e',1), ('b','c',4), ('b','d',5), 
          ('c','d',3),('c','e',2), ('d','e',2)]

graph3 = {'A':[0,3,0,2,5], 'B':[0,0,4,5,1], 'C':[0,0,0,3,3], 'D':[0,0,0,0,2], 'E':[0,0,0,0,0]}
graph3_df = pd.DataFrame(graph3, index=['A', 'B', 'C', 'D', 'E'])
print(graph3_df)
#for x in graph2:
#    if 3 in x:
#        print(x)

