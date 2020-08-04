# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import Optional

import networkx as nx
import numpy as np
import scipy as sp

from .embedding_container import EmbeddingContainer
from .spectral_embedding import _create_augmented_adjacency_matrix, \
    _generate_embedding
from .. import assertions


def laplacian_embedding(
        graph: nx.Graph,
        maximum_dimensions: int = 100,
        elbow_cut: Optional[int] = 1,
        weight_column: str = 'weight',
        svd_seed: Optional[int] = None,
        num_iterations: int = 5,
        power_iteration_normalizer: str = 'QR',
        num_oversamples: int = 10
) -> EmbeddingContainer:
    """
    Generates a spectral embedding based upon the Laplacian matrix of the graph.

    See also: https://csustan.csustan.edu/~tom/Clustering/GraphLaplacian-tutorial.pdf

    :param networkx.Graph graph: A networkx Graph object containing no more than one connected component.  Note that if
        the graph is a directed graph, the resulting dimensionality of the embedding will be twice that of an
        undirected graph
    :param int maximum_dimensions: Maximum dimensions of embeddings that will be returned - defaults to 100.  Actual
        dimensions of resulting embeddings should be significantly smaller, but will never be over this value.
    :param Optional[int] elbow_cut: scree plot elbow detection will detect (usually) many elbows.  This value specifies
        which elbow to use prior to filtering out extraneous dimensions. If None, then an embedding of size
        `maximum_dimensions` will be returned.
    :param str weight_column: The weight column to use in the Graph.
    :param Optional[int] svd_seed: If not provided, uses a random number every time, making consistent results difficult
        Set this to a random int if you want consistency between executions over the same graph.
    :param int num_iterations: The number of iterations to be used in the svd solver.
    :param int num_oversamples: Additional number of random vectors to sample the range of M so as
        to ensure proper conditioning. The total number of random vectors
        used to find the range of M is n_components + n_oversamples. Smaller
        number can improve speed but can negatively impact the quality of
        approximation of singular vectors and singular values.
    :param Optional[str] power_iteration_normalizer:
        Whether the power iterations are normalized with step-by-step
        QR factorization (the slowest but most accurate), 'none'
        (the fastest but numerically unstable when `n_iter` is large, e.g.
        typically 5 or larger), or 'LU' factorization (numerically stable
        but can lose slightly in accuracy). The 'auto' mode applies no
        normalization if `num_iterations` <= 2 and switches to LU otherwise.

        Options: 'auto' (default), 'QR', 'LU', 'none'
    :return: EmbeddingContainer containing a matrix, which itself contains the embedding for each node.  the tuple also
        contains a vector containing the corresponding vertex labels for each row in the matrix.  the matrix and vector
        are positionally correlated.
    :rtype: EmbeddingContainer
    """
    assertions.assert_single_connected_components(
        graph,
        "Run this algorithm over the largest connected component (see: topologic.largest_connected_component()) or " +
        "run it over every connected component separately."
    )

    working_graph = graph.copy()

    augmented_graph, graph_matrix, sorted_vertices = _create_augmented_adjacency_matrix(weight_column, working_graph)

    minimum_matrix_dimension = min(graph_matrix.shape)

    # make Laplacian matrix (DAD)
    in_degree = graph_matrix.sum(axis=0).astype(float)
    out_degree = graph_matrix.sum(axis=1).T.astype(float)

    in_degree_array = np.squeeze(np.asarray(in_degree))
    out_degree_array = np.squeeze(np.asarray(out_degree))

    in_diagonal = sp.sparse.diags(in_degree_array ** (-0.5))
    out_diagonal = sp.sparse.diags(out_degree_array ** (-0.5))

    lse_matrix = out_diagonal.dot(graph_matrix).dot(in_diagonal)

    embedding = _generate_embedding(
        elbow_cut,
        nx.is_directed(graph),
        lse_matrix,
        maximum_dimensions,
        minimum_matrix_dimension,
        num_oversamples,
        num_iterations,
        power_iteration_normalizer,
        svd_seed
    )

    result = EmbeddingContainer(embedding=embedding, vertex_labels=sorted_vertices)

    return result
