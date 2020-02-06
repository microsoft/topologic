# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import community
import networkx as nx
from . import assertions
from .louvain import best_partition
from .exceptions import InvalidGraphError
from .partitioned_graph import PartitionedGraph
from typing import Union


def q_score(
        graph: Union[nx.Graph, PartitionedGraph],
        weight_column: str = 'weight'
) -> float:
    """
    Given a networkx Graph or topologic PartitionedGraph, return the q score - or modularity of a graph.

    A PartitionedGraph will generate the appropriate partitions if not already provided.
    See topologic.PartitionedGraph for more details.

    See also: https://en.wikipedia.org/wiki/Modularity_(networks)

    :param graph: Partitioned graph contains a dictionary of all the
        communities in a graph, optimized for best modularity.  This partition structure is used when computing final
        q_score / modularity of graph.
    :type graph: Union[networkx.Graph, topologic.PartitionedGraph]
    :param str weight_column: weight column to use in computing modularity.
    :raise UnweightedGraphError: if graph does not contain weight_column in edge attributes
    :raise KeyError: If the partition is not a partition of all graph nodes.  This should not occur if PartitionedGraph
        is recently created and no changes occurred to the underlying networkx.Graph object.
    :raise ValueError: If the graph has no link.
    :raise TypeError: If partitioned_graph is not of type topologic.PartitionedGraph
    :return: q_score, or modularity, of this graph using the provided partitioning scheme.
    :rtype: float
    """
    if isinstance(graph, PartitionedGraph):
        assertions.assert_is_weighted(graph.graph)
        partition = graph.partition
        extracted_graph = graph.graph
    elif isinstance(graph, nx.Graph):
        partition = best_partition(graph)
        extracted_graph = graph
    else:
        raise InvalidGraphError('Expected type of nx.Graph or topologic.PartitionedGraph')

    return community.modularity(partition, extracted_graph, weight_column)
