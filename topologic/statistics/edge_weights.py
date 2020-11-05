# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
import numpy as np
from typing import Any, List, Tuple, Union
import logging
from .defined_histogram import DefinedHistogram
from .make_cuts import MakeCuts, filter_function_for_make_cuts


def histogram_edge_weight(
    graph: nx.Graph,
    bin_directive: Union[int, List[Union[float, int]], np.ndarray, str] = 10,
    weight_attribute: str = "weight",
) -> DefinedHistogram:
    """
    Generates a histogram of the edge weights of the provided graph.
    Histogram function is fundamentally proxied through to numpy's `histogram` function, and bin selection
    follows `numpy.histogram` processes.

    *Note*: Edges without a `weight_attribute` field will be excluded from this histogram.  Enable logging to view any
    messages about edges without weights.

    :param networkx.Graph graph: the graph.  No changes will be made to it.
    :param bin_directive: Is passed directly through to numpy's
        "histogram" (and thus, "histogram_bin_edges") functions.
        See: https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.histogram_bin_edges.html#numpy.histogram_bin_edges
        In short description: if an int is provided, we use `bin_directive` number of equal range bins.
        If a sequence is provided, these bin edges will be used and can be sized to whatever size you prefer
        Note that the np.ndarray should be ndim=1 and the values should be float or int.
    :type bin_directive: Union[int, List[Union[float, int]], numpy.ndarray, str]
    :param str weight_attribute: The weight attribute name in the data dictionary.  Default is `weight`.
    :return: A named tuple that contains the histogram and the bin_edges used in the histogram
    :rtype: DefinedHistogram
    """  # noqa:501
    logger = logging.getLogger(__name__)
    edge_weights: List[Union[int, float, None]] = [
        weight for _, _, weight in graph.edges(data=weight_attribute)
    ]
    none_weights: List[None] = [weight for weight in edge_weights if weight is None]
    actual_weights: List[Union[int, float]] = [weight for weight in edge_weights if weight is not None]

    if len(none_weights) != 0:
        logger.warning(f"Graph contains {len(none_weights)} edges with no {weight_attribute}." +
                       " Histogram excludes these values.")

    histogram, bin_edges = np.histogram(
        actual_weights,
        bin_directive
    )

    return DefinedHistogram(histogram=histogram, bin_edges=bin_edges)


def cut_edges_by_weight(
    graph: nx.Graph,
    cut_threshold: Union[int, float],
    cut_process: MakeCuts,
    weight_attribute: str = "weight",
    prune_isolates: bool = False
) -> nx.Graph:
    """
    Given a graph, a cut threshold, and a cut_process, create a new Graph that contains only the edges that are not
    pruned.

    *Note*: Edges without a `weight_attribute` field will be excluded from these cuts.  Enable logging to view any
    messages about edges without weights.

    :param networkx.Graph graph: The graph that will be copied and pruned.
    :param cut_threshold: The threshold for making cuts based on weight.
    :type cut_threshold: Union[int, float]
    :param MakeCuts cut_process: Describes how we should make the cut; cut all edges larger or smaller than the
        cut_threshold, and whether exclusive or inclusive.
    :param str weight_attribute: The weight attribute name in the data dictionary.  Default is `weight`.
    :param bool prune_isolates: If true, remove any vertex that no longer has an edge.  Note that this only prunes
        vertices which have edges to be pruned; any isolate vertex prior to any edge cut will be retained.
    :return: Pruned copy of the graph
    :rtype: networkx.Graph
    """
    logger = logging.getLogger(__name__)
    graph_copy = graph.copy()
    edge_weights: List[Tuple[Tuple[Any, Any], Union[int, float, None]]] = [
        ((source, target), weight) for source, target, weight in graph.edges(data=weight_attribute)
    ]
    none_weights: List[Tuple[Tuple[Any, Any], None]] = [
        (edge, weight) for edge, weight in edge_weights if weight is None
    ]
    actual_weights: List[Tuple[Tuple[Any, Any], Union[int, float]]] = [
        (edge, weight) for edge, weight in edge_weights if weight is not None
    ]

    if len(none_weights) != 0:
        logger.warning(f"Graph contains {len(none_weights)} edges with no {weight_attribute}." +
                       "Ignoring these when cutting by weight")

    filter_by = filter_function_for_make_cuts(cut_threshold, cut_process)
    edges_to_cut = [x for x in actual_weights if filter_by(x)]
    for edge, weight in edges_to_cut:
        source, target = edge
        if source in graph_copy and target in graph_copy and target in graph_copy[source]:
            graph_copy.remove_edge(source, target)
        if prune_isolates:
            if len(graph_copy[source]) == 0:
                graph_copy.remove_node(source)
            if len(graph_copy[target]) == 0:
                graph_copy.remove_node(target)

    return graph_copy
