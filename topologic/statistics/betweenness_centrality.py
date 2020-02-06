# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
import numpy as np
import random
from .defined_histogram import DefinedHistogram
from typing import List, Optional, Union
from .make_cuts import MakeCuts, filter_function_for_make_cuts


def histogram_betweenness_centrality(
    graph: nx.Graph,
    bin_directive: Union[int, List[Union[float, int]], np.ndarray, str] = 10,
    num_random_samples: Optional[int] = None,
    normalized: bool = True,
    weight_attribute: Optional[str] = None,
    include_endpoints: bool = False,
    random_seed: Optional[Union[int, random.Random]] = None
) -> DefinedHistogram:
    """
    Generates a histogram of the vertex betweenness centrality of the provided graph.
    Histogram function is fundamentally proxied through to numpy's `histogram` function, and bin selection
    follows `numpy.histogram` processes.
    
    The betweenness centrality calculation can take advantage of networkx' implementation of randomized sampling
    by providing num_random_samples (or k, in networkx betweenness_centrality nomenclature).
    
    See: https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.betweenness_centrality.html
    for more details. 

    :param networkx.Graph graph: the graph.  No changes will be made to it.
    :param bin_directive: Is passed directly through to numpy's 
        "histogram" (and thus, "histogram_bin_edges") functions.
        See: https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.histogram_bin_edges.html#numpy.histogram_bin_edges
        In short description: if an int is provided, we use `bin_directive` number of equal range bins.
        If a sequence is provided, these bin edges will be used and can be sized to whatever size you prefer. 
        Note that the np.ndarray should be ndim=1 and the values should be float or int.
    :type bin_directive: Union[int, List[Union[float, int]], numpy.ndarray, str]
    :param Optional[int] num_random_samples: Use num_random_samples for vertex samples to *estimate* betweeness.  
        num_random_samples should be <= len(graph.nodes).  The larger num_random_samples is, the better the 
        approximation.
    :param bool normalized: If True the betweenness values are normalized by 2/((n-1)(n-2)) for graphs, and 
        1/((n-1)(n-2)) for directed graphs where n is the number of vertices in the graph.
    :param Optional[str] weight_attribute: If None, all edge weights are considered equal. Otherwise holds the name of 
        the edge attribute used as weight.
    :param bool include_endpoints: If True include the endpoints in the shortest path counts.
    :param random_seed: Random seed or preconfigured random instance to be used for 
        randomly selecting random samples. Only used if num_random_samples is set.  None will generate a new random 
        state.  Specifying a random state will provide consistent results between runs.
    :type random_seed: Optional[Union[int, random.Random]]
    :return: A named tuple that contains the histogram and the bin_edges used in the histogram
    :rtype: DefinedHistogram
    """  # noqa:501

    betweenness_centrality_dict = nx.betweenness_centrality(
        G=graph,
        k=num_random_samples,
        normalized=normalized,
        weight=weight_attribute,
        endpoints=include_endpoints,
        seed=random_seed
    )
    histogram, bin_edges = np.histogram(
        list(betweenness_centrality_dict.values()),
        bin_directive
    )
    return DefinedHistogram(histogram=histogram, bin_edges=bin_edges)


def cut_vertices_by_betweenness_centrality(
    graph: nx.Graph,
    cut_threshold: Union[int, float],
    cut_process: MakeCuts,
    num_random_samples: Optional[int] = None,
    normalized: bool = True,
    weight_attribute: Optional[str] = None,
    include_endpoints: bool = False,
    random_seed: Optional[Union[int, random.Random]] = None
) -> nx.Graph:
    """
    Given a graph and a cut_threshold and a cut_process, return a copy of the graph with the vertices outside of the
    cut_threshold.
    
    The betweenness centrality calculation can take advantage of networkx' implementation of randomized sampling
    by providing num_random_samples (or k, in networkx betweenness_centrality nomenclature).
    
    See: https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.centrality.betweenness_centrality.html
    for more details. 
    
    :param networkx.Graph graph: The graph that will be copied and pruned.
    :param cut_threshold: The threshold for making cuts based on betweenness centrality.
    :type cut_threshold: Union[int, float]
    :param MakeCuts cut_process: Describes how we should make the cut; cut all edges larger or smaller than the
        cut_threshold, and whether exclusive or inclusive.
    :param Optional[int] num_random_samples: Use num_random_samples for vertex samples to *estimate* betweenness.  
        num_random_samples should be <= len(graph.nodes).  The larger num_random_samples is, the better the 
        approximation.
    :param bool normalized: If True the betweenness values are normalized by 2/((n-1)(n-2)) for graphs, and 1/((n-1)(n-2))
        for directed graphs where n is the number of vertices in the graph.
    :param Optional[str] weight_attribute: If None, all edge weights are considered equal. Otherwise holds the name of 
        the edge attribute used as weight.
    :param bool include_endpoints: If True include the endpoints in the shortest path counts.
    :param random_seed: Random seed or preconfigured random instance to be used for 
        randomly selecting random samples.
        Only used if num_random_samples is set.  None will generate a new random state.  Specifying a random state
        will provide consistent results between runs.
    :type random_seed: Optional[Union[int, random.Random]]
    :return: Pruned copy of the graph
    :rtype: networkx.Graph
    """  # noqa:501
    graph_copy = graph.copy()
    betweenness_centrality_dict = nx.betweenness_centrality(
        G=graph,
        k=num_random_samples,
        normalized=normalized,
        weight=weight_attribute,
        endpoints=include_endpoints,
        seed=random_seed
    )
    filter_by = filter_function_for_make_cuts(cut_threshold, cut_process)
    vertices_to_cut = list(filter(filter_by, betweenness_centrality_dict.items()))
    for vertex, degree_centrality in vertices_to_cut:
        graph_copy.remove_node(vertex)

    return graph_copy
