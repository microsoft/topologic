# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging

import networkx as nx
import numpy as np
from sklearn.utils.extmath import randomized_svd

from .elbow_finder import find_elbows
from ..graph_augmentation import rank_edges, \
    diagonal_augmentation


def _create_augmented_adjacency_matrix(weight_column, working_graph):
    logging.debug("rank edges")
    ranked_graph = rank_edges(working_graph, weight_column)

    logging.debug("add self loops and sensible weights")
    augmented_graph = diagonal_augmentation(ranked_graph, weight_column)

    sorted_vertices = sorted(augmented_graph.nodes())
    graph_matrix = nx.to_scipy_sparse_matrix(augmented_graph, nodelist=sorted_vertices)

    return augmented_graph, graph_matrix, sorted_vertices


def _generate_embedding(
        elbow_cut,
        is_directed,
        graph_matrix,
        maximum_dimensions,
        minimum_matrix_dimension,
        num_oversamples,
        num_iterations,
        power_iteration_normalizer,
        svd_seed
):
    logging.debug("spectral embedding into %d dimensions" % maximum_dimensions)
    left_singular_values, eigenvector, right_singular_values = randomized_svd(
        graph_matrix,
        n_components=min(maximum_dimensions, minimum_matrix_dimension - 1),
        n_iter=num_iterations,
        power_iteration_normalizer=power_iteration_normalizer,
        n_oversamples=num_oversamples,
        random_state=svd_seed
    )

    logging.debug("dimension reduction (elbow selection)")
    reduced_dimension = _get_reduced_dimensions(eigenvector, elbow_cut, maximum_dimensions)

    logging.debug("dimension is %d" % reduced_dimension)
    embedding = _project_and_reduce_embedding(
        eigenvector,
        is_directed,
        left_singular_values,
        reduced_dimension,
        right_singular_values
    )

    return embedding


def _project_and_reduce_embedding(eigenvector, is_directed, left_singular_values, reduced_dim, right_singular_values):
    sigma_sqrt = np.sqrt(eigenvector)

    sigma_sqrt_reduced_dimensions = sigma_sqrt[:reduced_dim]
    u_reduced_dimensions = left_singular_values[:, :reduced_dim]
    vt_reduced_dimensions = right_singular_values[:reduced_dim, :]

    xhat1 = np.multiply(sigma_sqrt_reduced_dimensions, u_reduced_dimensions)
    xhat2 = np.array([]).reshape(xhat1.shape[0], 0) if not is_directed else \
        np.multiply(np.transpose(vt_reduced_dimensions), sigma_sqrt_reduced_dimensions)

    return np.concatenate((xhat1, xhat2), axis=1)


def _get_reduced_dimensions(eigenvector, elbow_cut, maximum_dimensions):
    if elbow_cut is not None:
        rank_graph = find_elbows(eigenvector, num_elbows=elbow_cut)
        reduced_dim = rank_graph[(elbow_cut - 1)]
    else:
        reduced_dim = maximum_dimensions

    return reduced_dim
