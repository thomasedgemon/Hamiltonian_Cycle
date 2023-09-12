python script using weights, undirected graphs stored in igraph objects in order to utilize an algorithm for TSP problem. 
The Greedy Algorithm is used and then iterated in order to optimize. It's computational complexity is suboptimal and considerably higher than alternative (but considerably more complex) algorithms. 

NetworkX library was considered, but it's speed is similar to igraph's according to https://graph-tool.skewed.de/performance using very large and highly connected graphs. 

the primary challenge is storing edges (which is to say, storing graphs via their composite edges) with their weights in such a way as to make parsing them (especially with respect to duplicate edges) as straightforward as possible. every TSP algorithm involves "deleting" edges from a graph, as well as inspecting the neighbors of every vertex. Dicts, arrays, and tuples were all considered, and may be revisited in the future. 

an interesting consideration for later work would be to find a novel way to storing graphs and their attributes, as well as a GUI for user input, as manually editing code for >10 vertices on a well-connected graph is not feasible and is mistake-prone. this can perhaps include the ability to import directly from a csv or Pandas DataFrame. 
