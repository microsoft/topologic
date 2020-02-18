# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
import numpy as np
from scipy.spatial.distance import cdist
from ..embedding_container import EmbeddingContainer


def mean_average_precision(
        graph: nx.Graph,
        embedding_container: EmbeddingContainer,
        distance_metric: str = 'euclidean'
) -> float:
    """ Mean Average Precision (mAP)

    A fidelity measure to evaluate the quality of embedding generated with respect to the original unweighted Graph.

    Higher mAP value corresponds to a better quality embedding.

    :param networkx.Graph G: The unweighted graph for which the embedding is generated
    :param EmbeddingContainer embedding_container: The embedding container generated for the graph for
        which the mean average precision will be calculated
    :param str distance_metric: The distance metric to be used to find shortest path between nodes
        in the graph and embedding space. Default value for this param is 'euclidean', but all distance
        metrics available to the scipy.spatial.distance.cdist function are valid.
    :return: The mean average precision (mAP <= 1) representing the quality of the embedding
    :rtype: float
    """
    if graph is None:
        raise ValueError('graph must be specified but was None')
    if embedding_container is None:
        raise ValueError('embedding must be specified but was None')

    numerator = 0

    for source in graph.nodes:
        source_degree = graph.degree(source)
        neighbors = [n for n in graph.neighbors(source)]
        inner_sum = 0.0

        for neighbor in neighbors:
            nodes_closer_than_neighbor_in_embedding_space = _calculate_set_of_nodes_closer_than_given_node(
                src_vertex=source,
                dest_vertex=neighbor,
                embedding_container=embedding_container,
                distance_metric=distance_metric
            )
            common_nodes = set(neighbors).intersection(set(nodes_closer_than_neighbor_in_embedding_space))
            inner_sum += len(common_nodes) / len(nodes_closer_than_neighbor_in_embedding_space)

        numerator += inner_sum / source_degree

    mAP = numerator / len(graph)

    return mAP


def _calculate_set_of_nodes_closer_than_given_node(
    src_vertex,
    dest_vertex,
    embedding_container,
    distance_metric
):
    label_to_index_map = {label: indx for indx, label in enumerate(embedding_container.vertex_labels)}
    embedding = embedding_container.embedding

    src_index = label_to_index_map[src_vertex]
    dest_index = label_to_index_map[dest_vertex]

    distance_matrix = cdist([embedding[src_index]], embedding, distance_metric)[0]
    sorted_indices = np.argsort(distance_matrix)
    closest_nodes = []

    for vertex_index in sorted_indices:
        if vertex_index == src_index:
            continue

        if distance_matrix[vertex_index] > distance_matrix[dest_index]:
            break

        vertex_label = embedding_container.vertex_labels[vertex_index]
        closest_nodes.append(vertex_label)

    return closest_nodes
