# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import math
import networkx as nx
import community
from collections import defaultdict
from typing import Any, Dict
import warnings
from .. import assertions
from ..partitioned_graph import PartitionedGraph


def q_score(
    partitioned_graph: PartitionedGraph,
    weight_column: str = 'weight'
) -> float:
    """
    Deprecated: See modularity() for replacement.

    Given a topologic PartitionedGraph, return the q score - or modularity of a graph.

    See also: https://en.wikipedia.org/wiki/Modularity_(networks)

    :param partitioned_graph: Partitioned graph contains a dictionary of all the communities in a graph, optimized for
        best modularity.  This partition structure is used when computing final q_score / modularity of graph.
    :type partitioned_graph: Optional[topologic.PartitionedGraph]
    :param str weight_column: weight column to use in computing modularity.
    :raise UnweightedGraphError: if graph does not contain weight_column in edge attributes
    :raise KeyError: If the partition is not a partition of all graph nodes.  This should not occur if PartitionedGraph
        is recently created and no changes occurred to the underlying networkx.Graph object.
    :raise ValueError: If the graph has no links.
    :raise TypeError: If partitioned_graph is not of type topologic.PartitionedGraph
    :return: q_score, or modularity, of this graph using the provided partitioning scheme.
    :rtype: float
    """
    warnings.warn(
        "topologic.partition.q_score() has been deprecated in favor of topologic.partition.modularity()",
        DeprecationWarning
    )
    if isinstance(partitioned_graph, PartitionedGraph):
        partition = partitioned_graph.community_partitions
        extracted_graph = partitioned_graph.graph
        assertions.assert_is_weighted(extracted_graph)
    else:
        raise TypeError('Expected type topologic.PartitionedGraph')

    return community.modularity(partition, extracted_graph, weight_column)


def modularity(
    graph: nx.Graph,
    partitions: Dict[Any, int],
    weight_attribute: str = "weight",
    resolution: float = 1.0
) -> float:
    """
    Given an undirected graph and a dictionary of vertices to community ids, calculate the modularity.

    See also: https://en.wikipedia.org/wiki/Modularity_(networks)

    :param nx.Graph graph: An undirected graph
    :param Dict[Any, int] partitions: A dictionary representing a community partitioning scheme with the keys being the
        vertex and the value being a community id. Within topologic, these community ids are required to be ints.
    :param str weight_attribute: The edge data attribute on the graph that contains a float weight for the edge.
    :param float resolution: The resolution to use when calculating the modularity.
    :return: The modularity quality score for the given network and community partition schema.
    :raise TypeError: If the graph is not a networkx Graph
    :raise ValueError: If the graph is unweighted
    :raise ValueError: If the graph is directed
    """
    assertions.assert_is_graph(graph)
    assertions.assert_is_weighted(graph, weight_attribute)
    assertions.assert_is_undirected(graph)

    components = modularity_components(graph, partitions, weight_attribute, resolution)

    return sum(components.values())


def _modularity_component(
    intra_community_degree: float,
    total_community_degree: float,
    network_degree_sum: float,
    resolution: float
) -> float:
    community_degree_ratio = math.pow(total_community_degree, 2.0) / (2.0 * network_degree_sum)
    return (intra_community_degree - resolution * community_degree_ratio) / (2.0 * network_degree_sum)


def modularity_components(
    graph: nx.Graph,
    partitions: Dict[Any, int],
    weight_attribute: str = "weight",
    resolution: float = 1.0,
) -> Dict[int, float]:
    """
    Given an undirected, weighted graph and a community partition dictionary, calculates a modularity quantum for each
    community ID. The sum of these quanta is the modularity of the graph and partitions provided.

    :param nx.Graph graph: An undirected graph
    :param Dict[Any, int] partitions: A dictionary representing a community partitioning scheme with the keys being the
        vertex and the value being a community id. Within topologic, these community ids are required to be ints.
    :param str weight_attribute: The edge data attribute on the graph that contains a float weight for the edge.
    :param float resolution: The resolution to use when calculating the modularity.
    :return: A dictionary of the community id to the modularity component of that community
    :rtype: Dict[int, float]
    :raise TypeError: If the graph is not a networkx Graph
    :raise ValueError: If the graph is unweighted
    :raise ValueError: If the graph is directed
    """

    assertions.assert_is_graph(graph)
    assertions.assert_is_weighted(graph, weight_attribute)
    assertions.assert_is_undirected(graph)

    total_edge_weight = 0.0

    communities = set(partitions.values())

    degree_sums_within_community: Dict[int, float] = defaultdict(lambda: 0.0)
    degree_sums_for_community: Dict[int, float] = defaultdict(lambda: 0.0)
    for vertex, neighbor_vertex, weight in graph.edges(data=weight_attribute):
        vertex_community = partitions[vertex]
        neighbor_community = partitions[neighbor_vertex]
        if vertex_community == neighbor_community:
            if vertex == neighbor_vertex:
                degree_sums_within_community[vertex_community] += weight
            else:
                degree_sums_within_community[vertex_community] += weight * 2.0
        degree_sums_for_community[vertex_community] += weight
        degree_sums_for_community[neighbor_community] += weight
        total_edge_weight += weight

    return {comm: _modularity_component(
        degree_sums_within_community[comm],
        degree_sums_for_community[comm],
        total_edge_weight,
        resolution
    ) for comm in communities}
