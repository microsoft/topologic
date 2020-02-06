Using and Understanding Graph Community Structure with `topologic`
===================

`topologic` exposes a few of the most commonly used community related functions.  The core of these functions come
from the excellent `python-louvain` library, and in most cases are only exposed via the `topologic` module for 
consistency in finding these essential functions.

## Q-Score
The `q score` of a graph is a float between 0 and 1 that represents a graph's community structure quality.
Communities can be identified through many different ways, and their normal representation is a dictionary of `vertex`: 
`community`.  If you have not identified your own community, the `topologic.q_score` function will attempt to 
determine the best community structure via the `community.best_partition` function (from 
[python-louvain](https://github.com/taynaud/python-louvain))

```python
import networkx as nx
from topologic import q_score

my_graph = nx.Graph()
# load graph with data 

q_score = q_score(my_graph)
```

## Best Partitions
The `topologic.best_partition` is nothing more than a pass through to the `community.best_partition` function.  It
exists primarily to aid discovery and to incorporate it into the centralized documentation, and because the library
is such a crucial part of quickly determining a reasonable community structure for a graph.

```python
import networkx as nx
from topologic import best_partition

my_graph = nx.Graph()
# load graph with data

communities = best_partition(my_graph, random_state=1234)
```

`random_state` is an optional value, but setting it will ensure that the communities determined by best_partition for
the same graph are deterministic.

## Induced Graph for Best Partition
One common use case for finding the community structure of a graph is to `induce` a graph from those communities.

This function will take in a graph (and, optionally, the previously calculated partition dictionary).

If no community dictionary is provided, `best_partition` is executed over the graph and that partition is used.

The induced graph will be a high level view of the community structure of the initial graph.  Vertices in community 
`0` that also have connections to vertices in community `5` will result in the induced graph vertex `0` having a 
connection to the induced graph vertex `5`.  For other vertices with an identical arrangement, their edges are 
summed and used as the weight between induced graph vertex `0` and induced graph vertex `5`.

This induced graph has many of the same characteristics as the much larger initial graph, and can be used as a
reasonable approximation in some very expensive graph analytics.

```python
import networkx as nx
from topologic import induced_graph_for_best_partition

my_graph = nx.Graph()
# load graph with data
induced = induced_graph_for_best_partition(my_graph)
```
