# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import numpy
import operator
import networkx
from typing import Any, Iterator, Optional


def node2vec_random_walk_iterator(
        graph: networkx.Graph,
        node: Any,
        p: float,
        q: float,
        weight_attr: Optional[str] = 'weight'
) -> Iterator[Any]:
    """
    This function returns an iterator which executes a random walk of a graph according to the procedure
    specified in node2vec[0].

    [0] https://snap.stanford.edu/node2vec/

    :param networkx.Graph graph: the graph
    :param Any node: starting node in G for the walk
    :param float p: the return parameter. p < 1.0 means that the walk is more likely to return along an edge that was
        just traversed. p > 1.0 means that the walk is less likely to return
    :param float q: the in-out parameter. q < 1.0 means that the walk is more likely to explore outward. p > 1.0 means
        that the walk is less likely to explore outward
    :param Optional[str] weight_attr: the name of the edge weight attribute in G. If None, a weight of 1 is used for all
        edges
    :return: a lazy iterator of nodes in G that comprise the walk. The first value returned is always the starting node.
    :rtype: Iterator[Any]
    """
    _, maxdegree = max(networkx.degree(graph), key=operator.itemgetter(1))
    probs = numpy.zeros(maxdegree)
    neighbors = [None] * maxdegree

    last_visited = None

    while True:
        num_neighbors = 0
        for i, v in enumerate(graph[node]):
            num_neighbors = i + 1
            neighbors[i] = v

            if weight_attr is None:
                weight = 1.0
            else:
                weight = graph[node][v][weight_attr]

            if last_visited == v:
                probs[i] = weight / p
            elif last_visited is not None and v in graph[last_visited]:
                probs[i] = weight
            else:
                probs[i] = weight / q

        neighbor_slice = neighbors[:num_neighbors]
        probs_slice = probs[:num_neighbors]

        neighbor_probs = probs_slice / numpy.linalg.norm(probs_slice, ord=1)
        next_node = numpy.random.choice(neighbor_slice, p=neighbor_probs)

        yield node

        last_visited = node
        node = next_node
