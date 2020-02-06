# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
import networkx as nx
import numpy as np
from .defined_histogram import DefinedHistogram
from typing import List, Union
from .make_cuts import MakeCuts, filter_function_for_make_cuts


def histogram_degree_centrality(
    graph: nx.Graph,
    bin_directive: Union[int, List[Union[float, int]], np.ndarray, str] = 10
) -> DefinedHistogram:
    """
    Generates a histogram of the vertex degree centrality of the provided graph.
    Histogram function is fundamentally proxied through to numpy's `histogram` function, and bin selection
    follows `numpy.histogram` processes.

    :param networkx.Graph graph: the graph.  No changes will be made to it.
    :param bin_directive: Is passed directly through to numpy's 
        "histogram" (and thus, "histogram_bin_edges") functions.
        See: https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.histogram_bin_edges.html#numpy.histogram_bin_edges
        In short description: if an int is provided, we use `bin_directive` number of equal range bins.
        If a sequence is provided, these bin edges will be used and can be sized to whatever size you prefer
        Note that the np.ndarray should be ndim=1 and the values should be float or int.
    :type bin_directive: Union[int, List[Union[float, int]], numpy.ndarray, str]
    :return: A named tuple that contains the histogram and the bin_edges used in the histogram
    :rtype: DefinedHistogram
    """  # noqa:501

    degree_centrality_dict = nx.degree_centrality(graph)
    histogram, bin_edges = np.histogram(
        list(degree_centrality_dict.values()),
        bin_directive
    )
    return DefinedHistogram(histogram=histogram, bin_edges=bin_edges)


def cut_vertices_by_degree_centrality(
    graph: nx.Graph,
    cut_threshold: Union[int, float],
    cut_process: MakeCuts
) -> nx.Graph:
    """
    Given a graph and a cut_threshold and a cut_process, return a copy of the graph with the vertices outside of the
    cut_threshold.

    :param networkx.Graph graph: The graph that will be copied and pruned.
    :param cut_threshold: The threshold for making cuts based on degree centrality.
    :type cut_threshold: Union[int, float]
    :param MakeCuts cut_process: Describes how we should make the cut; cut all edges larger or smaller than the
        cut_threshold, and whether exclusive or inclusive.
    :return: Pruned copy of the graph
    :rtype: networkx.Graph
    """
    graph_copy = graph.copy()
    degree_centrality_dict = nx.degree_centrality(graph_copy)
    filter_by = filter_function_for_make_cuts(cut_threshold, cut_process)
    vertices_to_cut = list(filter(filter_by, degree_centrality_dict.items()))
    for vertex, degree_centrality in vertices_to_cut:
        graph_copy.remove_node(vertex)

    return graph_copy
