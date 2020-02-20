# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
from . import assertions
from typing import Any, Callable, Generator, Set


def largest_connected_component(graph: nx.Graph, weakly: bool = True) -> nx.Graph:
    """
    Returns the largest connected component of the graph.

    :param networkx.Graph graph: The networkx graph object to select the largest connected component from.
      Can be either directed or undirected.
    :param bool weakly: Whether to find weakly connected components or strongly connected components for directed
      graphs.
    :return: A copy of the largest connected component as an nx.Graph object
    :rtype: networkx.Graph
    """
    connected_component_function = _connected_component_func(graph, weakly)
    largest_component = max(connected_component_function(graph), key=len)
    return graph.subgraph(largest_component).copy()


def connected_components_generator(graph: nx.Graph) -> Generator[nx.Graph, None, None]:
    """
    Returns a Generator that will provide each component as a networkx.Graph copy

    :param networkx.Graph graph: The networkx graph object to create a connected component generator from
    :return: A Generator that returns a copy of the subgraph corresponding to a connected component
      of `graph`
    :rtype: Generator[networkx.Graph]
    """
    connected_component_function = _connected_component_func(graph)
    for component in connected_component_function(graph):
        yield graph.subgraph(component).copy()


def number_connected_components(graph: nx.Graph) -> int:
    """
    Returns the number of connected components in the Graph.

    This function calls the appropriate newtorkx connected components function depending on whether it is Undirected
    or Directed.

    :param networkx.Graph graph: The networkx graph object to determine the number of connected components for
    :return: number of connected components (and in the case of a directed graph, strongly connected)
    :rtype: int
    """
    number_cc_func = _number_connected_components_func(graph)
    return number_cc_func(graph)


def _connected_component_func(
        graph: nx.Graph,
        weakly: bool = True
) -> Callable[[nx.Graph], Generator[Set[Any], None, None]]:
    assertions.assert_is_graph(graph)
    if not nx.is_directed(graph):
        return nx.connected_components
    elif weakly:
        return nx.weakly_connected_components
    else:
        return nx.strongly_connected_components


def _number_connected_components_func(graph: nx.Graph) -> Callable[[nx.Graph], int]:
    assertions.assert_is_graph(graph)
    if not nx.is_directed(graph):
        return nx.number_connected_components
    else:
        return nx.number_strongly_connected_components
