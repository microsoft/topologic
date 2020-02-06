# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
from sklearn.metrics.cluster import adjusted_rand_score
import numpy as np
from typing import Any, Iterable
from .assertions import assert_is_graph


def calculate_ari_scores(
        graph: nx.Graph,
        reference_cluster_attribute: Any,
        predicted_clusters: Iterable[str]
) -> np.ndarray:
    """
    Calculates Adjusted Rand Index for a graph.

    The Rand index is a measure of similarity between two clusters.  See https://en.wikipedia.org/wiki/Rand_index

    This method assumes that multiple clustering algorithms have been run over the graph and the cluster IDs
    are stored in the graph nodes as integers.

    :param networkx.Graph graph: NetworkX graph
    :param Any reference_cluster_attribute: Attribute on the node that contains the cluster ID.  Value of attribute
        should be an integer
    :param Iterable[str] predicted_clusters: Iterable of node attribute names that contain cluster IDs.  Value at each
        attribute should be an integer.  If we are only comparing the reference cluster with one predicted cluster then
        this is an iterable with a single value.
    :return: Array of scores.  One score will be returned for each predicted cluster in the predicted_clusters
        input iterable.
    :raises ValueError: When conversion node[reference_cluster_attribute] or node[predicted_clusters[x]] cannot be
        converted to an int.
    :raises KeyError: When reference_cluster_attribute or any attribute in predicted_clusters is not defined
        on any of the graph nodes.
    :raises TypeError: When graph is not a networkx.Graph object
    """

    assert_is_graph(graph)

    clusters_reference: np.ndarray = []
    for node in graph.nodes():
        clusters_reference = np.append(clusters_reference, int((graph.nodes()[node][reference_cluster_attribute])))

    ari_scores_list: np.ndarray = []
    for cluster_id_attribute in predicted_clusters:
        louvain_clusters: np.ndarray = []
        for node in graph.nodes():
            louvain_clusters = np.append(louvain_clusters, int((graph.nodes()[node][cluster_id_attribute])))

        ari_scores_list = np.append(ari_scores_list, calculate_ari(clusters_reference, louvain_clusters))
    return ari_scores_list


def calculate_ari(
        reference_clusters: Iterable[int],
        predicted_clusters: Iterable[int]
) -> float:
    """
    Calculates Adjusted Rand Index for two lists.

    The Rand index is a measure of similarity between two clusters.  See https://en.wikipedia.org/wiki/Rand_index

    This method assumes that multiple clustering algorithms have been run over the graph and the cluster IDs
    are stored in the graph nodes as integers.

    :param Iterable[int] reference_clusters: An Iterable[int] of values
    :param Iterable[int] predicted_clusters: An Iterable[int] of values
    :return: The adjusted rand index for the two lists
    :rtype float:
    """
    return adjusted_rand_score(reference_clusters, predicted_clusters)
