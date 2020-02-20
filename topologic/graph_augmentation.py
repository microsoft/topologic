# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
import numpy as np
from scipy.stats import rankdata

from . import assertions


def self_loop_augmentation(
        graph: nx.classes.graph.Graph,
        weight_column: str = 'weight'
) -> nx.Graph:
    """
    Generates a self loop for each vertex in the graph with a generated weight for each vertex that is the ratio
    between its degree in the graph and the total number of *other* vertices in the graph, excluding the original
    self loop.

    This should be used prior to Spectral Embedding techniques to ensure that there is a reasonable value for
    each vertex as it will appear in an adjacency matrix.

    Modifies the provided graph in place as well as returning it.

    :param networkx.Graph graph: The networkx graph to diagonally augment
    :param str weight_column: The weight column to augment
    :return: The networkx Graph object that was modified in place.
    :rtype: networkx.Graph
    """
    assertions.assert_is_graph(graph)

    vertices = graph.nodes()

    vertex_count = len(vertices)

    for vertex in vertices:
        # remove self loops
        if graph.has_edge(vertex, vertex):
            graph.remove_edge(vertex, vertex)

        degree = graph.degree(vertex)

        # add the augmented weight back onto the diagonal
        graph.add_edge(vertex, vertex)
        graph[vertex][vertex][weight_column] = degree / (vertex_count - 1)

    return graph


def __scale_edge_weights__(weight, edge_count):
    # This is meant to scale edge weights between 0 and 2
    return (weight * 2) / (edge_count + 1)


def rank_edges(
        graph: nx.Graph,
        weight_column: str = 'weight'
) -> nx.Graph:
    """
    Ranks the edges of a networkx.classes.graph.Graph object according to the values associated to the
    `weight_column` in the edge attributes

    :param networkx.Graph graph: The graph we will rank the edges in.  MUST contain an attribute that corresponds to
        `weight_column` (default value: `weight`)
    :param str weight_column: edge attribute that contains the weight value.  Default is `weight`
    :return: Updated graph with new weights between 0 and 2, exclusive.  Based on scipy.stats rankdata function.
    :rtype: networkx.Graph
    :raise UnweightedGraphException: if the graph not weighted by the provided `weight_column`
    :raise TypeError: If the `graph` provided is not an `nx.Graph`
    :examples:
        >>> g = nx.Graph()
        >>> g.add_edge("1", "2", weight=3)
        >>> g.add_edge("2", "3", weight=4)
        >>> g.add_edge("4", "5", weight=2)
        >>> g = rank_edges(g)
        >>> g.edges(data=True) #doctest: +NORMALIZE_WHITESPACE
        EdgeDataView([('1', '2', {'weight': 1.0}),
                ('2', '3', {'weight': 1.5}),
                ('4', '5', {'weight': 0.5})])
    """
    assertions.assert_is_weighted_graph(graph, weight_column)

    edge_count = len(graph.edges)
    edge_data = graph.edges(data=True)
    edges = np.array(
        list(
            map(
                lambda x: x[2][weight_column],
                edge_data
            )
        ),
        np.float64
    )
    ranked_values = rankdata(edges)
    i = 0
    for source, target, data in edge_data:
        data[weight_column] = __scale_edge_weights__(ranked_values[i], edge_count)
        i += 1

    return graph
