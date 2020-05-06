# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
from .exceptions import UnweightedGraphError, InvalidGraphError


def assert_is_graph(graph: nx.Graph):
    """
    Asserts that an object is a networkx graph

    :param graph: Graph to check
    :raises TypeError: If graph is not a graph object
    """
    if not isinstance(graph, nx.Graph):
        raise TypeError('graph must be a networkx.Graph')


def assert_is_weighted(
        graph: nx.Graph,
        weight_column: str = 'weight'
):
    """
    Asserts that a graph object is a weighted graph

    :param graph: A graph to check
    :param weight_column: Weight column
    :raises UnweightedGraphError: Graph is not weighted by the requested weight column
    """
    if not nx.is_weighted(graph, weight=weight_column):
        raise UnweightedGraphError("Weight column [{0}] not found in every graph edge attribute".format(weight_column))


def assert_is_weighted_graph(
        graph: nx.Graph,
        weight_column: str = 'weight'
):
    """
    Asserts that an object is a networkx graph and that the graph object is a weighted graph.

    :param graph: A graph to check
    :param weight_column: Weight column
    :raises TypeError: If graph is not a networkx graph object
    :raises UnweightedGraphError: Graph is not weighted by the requested weight column
    """
    assert_is_graph(graph)
    assert_is_weighted(graph, weight_column)


def assert_single_connected_components(
        graph: nx.Graph,
        extended_message: str = ""
):
    """
    Asserts that there is only a single connected component in the graph.

    :param graph: A graph object
    :param extended_message: An optional message that, if specified, will be appended to the raises exception.
    """
    assert_is_graph(graph)

    if not nx.is_directed(graph):
        if nx.number_connected_components(graph) > 1:
            raise InvalidGraphError(
                "The graph provided has more than one connected component.  {0}".format(extended_message)
            )
    else:
        if nx.number_weakly_connected_components(graph) > 1:
            raise InvalidGraphError(
                "The graph provided has more than one weakly connected component.  {0}".format(extended_message)
            )


def validate_minimal_graph(
    graph: nx.Graph,
    weight_attribute: str = "weight"
):
    """
    Validates that every edge is weighted, contains nodes, and contains edges.

    :param networkx.Graph graph: A networkx graph object
    :param str weight_attribute: The attribute containing the weight of the edge.
    :raises ValueError: If the graph is not fully weighted, has no nodes, or has no edges.
    """
    if len(graph) == 0:
        raise ValueError("The graph provided has no nodes")
    if len(graph.edges()) == 0:
        raise ValueError("The graph provided has no edges")
    if not nx.is_weighted(graph, weight=weight_attribute):
        raise ValueError("The graph provided is not fully weighted")


def assert_is_undirected(graph: nx.Graph):
    """
    Asserts that an object is an undirected graph

    :param graph: Graph to check
    :raises ValueError: If a graph is not an undirected graph
    """
    if graph.is_directed():
        raise ValueError("graph must be an undirected graph")
