# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
import community
from typing import Any, Dict
import logging


def induce_graph_by_communities(
    graph: nx.Graph,
    communities: Dict[Any, int],
    weight_attribute: str = 'weight'
) -> nx.Graph:
    """
    Creates a community graph with nodes from the communities dictionary
    and using the edges of the original graph to form edges between communities.

    Weights are aggregated; you may need to normalize the resulting graph
    after calling this function.

    Note: logs a warning if the size of the community dictionary is less than
    the size of the provided graph's vertexset.

    :param networkx.Graph graph: The original graph that contains the edges that will be
        used to formulate a new induced community graph
    :param communities: The communities dictionary provides a mapping of
        original vertex ID to new community ID.
    :type communities: dict[Any, int]
    :param str weight_attribute: The weight attribute on the original graph's edges to use
        when aggregating the weights of the induced community graph.  Default is `weight`.
    :return: The induced community graph.
    :rtype: networkx.Graph
    :raises ValueError: If the graph is None
    :raises ValueError: If the communities dictionary is None
    """
    logger = logging.getLogger(__name__)
    if graph is None:
        raise ValueError("graph cannot be None")
    if communities is None:
        raise ValueError("communities cannot be None")
    if len(communities) < len(graph.nodes()):
        logger.warning(
            f"Length of communities provided ({len(communities)}) is less than the " +
            f"total number of nodes in the graph ({len(graph.nodes())})"
        )

    return community.induced_graph(
        communities,
        graph,
        weight_attribute
    )
