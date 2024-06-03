python script using weighted, undirected graphs stored in igraph objects in order to utilize an algorithm for TSP problem. 

NetworkX library was considered, but it's speed is similar to igraph's according to https://graph-tool.skewed.de/performance using very large and highly connected graphs. 

the primary challenge is storing edges (which is to say, storing graphs via their composite edges) with their weights in such a way as to make parsing them (especially with respect to duplicate edges) as straightforward as possible. every TSP algorithm involves "deleting" edges from a graph, as well as inspecting the neighbors of every vertex. Dicts, arrays, and tuples were all considered, and may be revisited in the future. 

an interesting consideration for later work would be to find a novel way to storing graphs and their attributes, as well as a GUI for user input, as manually editing code for >10 vertices on a well-connected graph is not feasible and is mistake-prone. this can perhaps include the ability to import directly from a csv or Pandas DataFrame. 

downside(?) to using a matrix is that half of it remains empty even for a fully connected graph. searching must avoid cells which are known to be null.

**when represented as 2d matrices, what properties, if any, do cycles and minimum cycles display? 
  -data representation could be a key. 

current best exact algo: Ambainis et al with O(1.728^n)
other algos use MWST's, linear programming, ant colony routing, etc

general conception:
1.instantiate graph
2.instantiate working graph, from which edges and vertices will be removed
3.instantiate new graph, which will be built newly with every iteration.
3.apply algorithm
  -if vertices still exist, continue
  -else, stop, check length of new cycle, store lenth in var
4. iterate algorithm: re-instantiate working graph, delete new graph, perform algorithm again

general conception for each algorithm
-develop algorithm
-write algorithm as simply as possible
-test algorithm
-determine time complexity


if matrices are used to represent the graphs, is there some property that hamiltonian cycles share when represented as matrices???


idea 1: choose most-connected node first
  (what if there are vertices of equal connections? randomly choose one?)

current algos:
  simulated annealing: make random walk as starting total distance. make small changes until the overall length decreases, and then finds an average lowest value. if new route is worse, accept it with increasingly             lowering probability. 
  brute force: self explanatory. worst possible O(n)
  Held-Karp:...
  branch and bound: 
  nearest neighbor: starts randomly and visits nearest new city until done. fast, but not exact or optimal
  greedy: repeatedly adds shortest available edge.
  Christofides: makes MWST, finds MW matching for odd degree vertices, and combines them
  genetic: ...
  ant colony:...
  tabu: local search with memory that escapes local minima by allowing non-improving moves while preventing cycling
  particle swarm:...
  MST:...
  k-opt: iteratively removes edges
