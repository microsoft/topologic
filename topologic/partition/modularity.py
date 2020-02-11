# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import community
from .. import assertions
from ..partitioned_graph import PartitionedGraph


def q_score(
    partitioned_graph: PartitionedGraph,
    weight_column: str = 'weight'
) -> float:
    """
    Given a topologic PartitionedGraph, return the q score - or modularity of a graph.

    See also: https://en.wikipedia.org/wiki/Modularity_(networks)

    :param graph: Partitioned graph contains a dictionary of all the communities in a graph, optimized for
        best modularity.  This partition structure is used when computing final q_score / modularity of graph.
    :type partitioned_graph: topologic.PartitionedGraph
    :param str weight_column: weight column to use in computing modularity.
    :raise UnweightedGraphError: if graph does not contain weight_column in edge attributes
    :raise KeyError: If the partition is not a partition of all graph nodes.  This should not occur if PartitionedGraph
        is recently created and no changes occurred to the underlying networkx.Graph object.
    :raise ValueError: If the graph has no links.
    :raise TypeError: If partitioned_graph is not of type topologic.PartitionedGraph
    :return: q_score, or modularity, of this graph using the provided partitioning scheme.
    :rtype: float
    """
    if isinstance(partitioned_graph, PartitionedGraph):
        partition = partitioned_graph.community_partitions
        extracted_graph = partitioned_graph.graph
        assertions.assert_is_weighted(extracted_graph)
    else:
        raise TypeError('Expected type topologic.PartitionedGraph')

    return community.modularity(partition, extracted_graph, weight_column)
