# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import collections

import networkx as nx
from typing import Dict, Tuple, List, Any


def calculate_internal_external_densities(
        graph: nx.Graph,
        partitions: Dict[Any, Any],
        weight_attribute: str = 'weight'
) -> Tuple[Dict[Any, List[float]], Dict[Any, List[float]]]:
    """
    Calculates the internal and external densities given a graph and a node membership dictionary. Density is defined
    by 'How to Make the Team: Social Networks vs. Demography as Criteria for Designing Effective Teams' as being
    the mean strength of tie between members of the set. In other words, density is the normalized average of edge
    weights by node.

    For a given node, the density is the sum of all edge weights divided by the maximum edge weight for that node.

    For internal density, only the edge's whose target node is in the same membership group will be summed. Similarly,
    for external density, only the edge's whose target node is not in the same membership group will be summed.

    See also:
    Reagans, R., Zuckerman, E., & McEvily, B. (2004).
    How to Make the Team: Social Networks vs. Demography as Criteria for Designing Effective Teams.
    Administrative Science Quarterly, 49(1), 101–133. https://doi.org/10.2307/4131457

    :param graph: A weighted graph that the internal density will be calculated over
    :param Dict[any, int] partitions: A dictionary for the graph with each key being a node id and each value is
        the membership for that node id. Often this will be a partition dictionary calculated from
        topologic.louvain.best_partition
    :param str weight_attribute: The key to the weight column on the graph's edges

    :return: A tuple of two dictionaries. The first is the internal density and the second is the external density
    :rtype: Tuple[Dict[Any, List[float]], Dict[Any, List[float]]]
    """
    if not nx.is_weighted(graph, weight=weight_attribute):
        raise ValueError('The graph must be weighted.')

    # build a dictionary where the key is a membership_id and the value is a list of nodes that belong to that
    # membership
    membership_inverted: Dict[Any, List[Any]] = collections.defaultdict(list)
    for key in partitions.keys():
        membership_inverted[partitions[key]].append(key)

    internal_density: Dict[Any, List[float]] = collections.defaultdict(list)
    external_density: Dict[Any, List[float]] = collections.defaultdict(list)

    for partition_id in membership_inverted.keys():
        for node in membership_inverted[partition_id]:
            max_weight = max((weight for source, target, weight in graph.edges(node, data=weight_attribute)))

            for source, target, weight in graph.edges(node, data=weight_attribute):
                target_partition = partitions[target]
                density_for_node = weight / max_weight

                if target_partition == partition_id:
                    internal_density[partition_id].append(density_for_node)
                else:
                    external_density[partition_id].append(density_for_node)

    return internal_density, external_density
