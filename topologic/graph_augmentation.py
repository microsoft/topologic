# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import Union

import networkx as nx
import numpy as np
from scipy.stats import rankdata

from . import assertions


def diagonal_augmentation(
        graph: Union[nx.Graph, nx.DiGraph],
        weight_column: str = 'weight'
) -> nx.Graph:
    """
    Replaces the diagonal of adjacency matrix of the graph with the
    weighted degree / number of vertices in graph. For directed graphs,
    the weighted in and out degree is averaged.

    Modifies the provided graph in place as well as returning it.

    :param: The networkx graph which will get a replaced diagonal
    :type graph: Union[nx.Graph, nx.DiGraph]
    :param str weight_column: The weight column of the edge
    :return: The networkx Graph or DiGraph object that was modified in place.
    :rtype: Union[nx.Graph, nx.DiGraph]
    """
    assertions.assert_is_graph(graph)

    vertices = graph.nodes()

    vertex_count = len(vertices)

    for vertex in vertices:
        # remove self loops
        if graph.has_edge(vertex, vertex):
            graph.remove_edge(vertex, vertex)

        if isinstance(graph, nx.DiGraph):
            in_degree = graph.in_degree(vertex, weight=weight_column)
            out_degree = graph.out_degree(vertex, weight=weight_column)
            weighted_degree = (in_degree + out_degree) / 2
        else:
            weighted_degree = graph.degree(vertex, weight=weight_column)

        # add the augmented weight back onto the diagonal
        graph.add_edge(vertex, vertex)
        graph[vertex][vertex][weight_column] = weighted_degree / (vertex_count - 1)

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

    edge_count = len(graph.edges())
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
