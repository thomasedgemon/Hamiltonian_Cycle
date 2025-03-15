this project contains two primary tasks:
  1. attempt to develop an optimized version of the Held-Karp algorithm, which is currently the fastest exact
     algorithm for TSP, with a time complexity of O(n^2(2^n)).
  2. develop python script to run optimized algorithm.


HK, boiled down:
  1. make dictionary of all node subsets
  2. find all routes from starting node (i) to another node (j). for a complete graph, this is superfluous, as every node is connected to every other node. store in dict.
  3. add another node (k). find all routes starting at i, going to j, and ending at k. save shortest route to dict.
  4. iterate this for all route subsets, saving the shortest to the dict for comparison to the next iteration, rather than having to
     continue to calculate all subsets with every iteration.

calculating all optimal subsets is the majority of time complexity for this algorithm.

