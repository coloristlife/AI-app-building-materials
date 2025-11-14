- https://graphacademy.neo4j.com/courses/graph-data-science-fundamentals/1-graph-algorithms/4-path-finding/
# Path Finding

## Introduction
Path finding algorithms find the shortest path between two or more nodes or evaluate the availability and quality of paths.

Common use cases of path finding are:

  - Supply chain analytics: Identifying the fastest path between an origin and a destination or between a raw material and a finished product
  
  - Customer Journey: Analyzing the events that make up a customer’s experience. In healthcare for example, this can be the experience of an in-patient from admission to discharge.


## Dijkstra Source-Target Shortest Path
A common, industry standard, path finding algorithm is Dijkstra. It computes the shortest path between a source and a target node. Like many other path finding algorithms in GDS, Dijkstra supports weighted relationships to account for distance or another cost property when comparing paths.

Below is an example of using Dijkstra source-target shortest path to find the shortest path between the actors "Kevin Bacon" and "Denzel Washington".

First, create the graph projection.

~~~~
CALL gds.graph.project('proj',
    ['Person','Movie'],
    {
        ACTED_IN:{orientation:'UNDIRECTED'},
        DIRECTED:{orientation:'UNDIRECTED'}
    }
);
~~~~
Then we can run Dijkstra’s shortest path.

~~~
MATCH (kevin:Actor{name : 'Kevin Bacon'})
MATCH (denzel:Actor{name : 'Denzel Washington'})

CALL gds.shortestPath.dijkstra.stream(
    'proj',
    {
        sourceNode:kevin,
        TargetNode:denzel
    }
)

YIELD sourceNode, targetNode, path
RETURN sourceNode, targetNode, nodes(path) as path;
~~~

This should give you a path consisting of four relationships between Kevin Bacon and Denzel Washington.

<img width="341" height="310" alt="image" src="https://github.com/user-attachments/assets/6449fbff-e2d5-47b8-9c28-bba93e969249" />

## Other Path Finding Algorithms

Other GDS production tier Path Finding algorithms can be split into a few different subcategories that are listed below:

Shortest path between two nodes:

  - A* Shortest Path: An extension of Dijkstra that uses a heuristic function to speed up computation.
  
  - Yen’s Algorithm Shortest Path: An extension of Dijkstra that allows you to find multiple, the top k, shortest paths.

Shortest path between a source node and multiple other target nodes:

  - Dijkstra Single-Source Shortest Path: Dijkstra implementation for shortest path between one source and multiple targets.
  
  - Delta-Stepping Single-Source Shortest Path: Parallelized shortest path computation. Computes faster than Dijkstra single-source shortest Path but uses more memory.

General path search between a source node and multiple other target nodes:

  - Breadth First Search: Searches paths in order of increasing distance from the source node on each iteration.
  
  - Depth First Search: Searches as far as possible along a single multi-hop path on each iteration. 

A full list of path finding algorithms across all product tiers can be found in the [Pathfinding documentation.](https://neo4j.com/docs/graph-data-science/current/algorithms/pathfinding/?_gl=1*f8yeci*_gcl_au*MTQ5ODIwNzc3Mi4xNzYxMTU1NjU3*_ga*NDUzMjA5MTk2LjE3NjExNTU2NTc.*_ga_DL38Q8KGQC*czE3NjI4OTQ0MTQkbzQkZzEkdDE3NjI5MDIwMjIkajE0JGwwJGgw*_ga_DZP8Z65KK4*czE3NjI4OTQ0MTQkbzQkZzEkdDE3NjI5MDE5NzckajU5JGwwJGgw)
