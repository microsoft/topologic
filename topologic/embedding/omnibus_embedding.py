# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import copy
import logging
from typing import List, Union, Optional, Tuple

import networkx as nx
import numpy as np
import scipy as sp

from .embedding_container import EmbeddingContainer
from .spectral_embedding import _generate_embedding
from ..connected_components import largest_connected_component
from ..embedding import EmbeddingMethod
from ..graph_augmentation import rank_edges, \
    diagonal_augmentation


def omnibus_embedding(
        graphs: List[nx.Graph],
        maximum_dimensions: int = 100,
        elbow_cut: Optional[int] = 1,
        embedding_method: EmbeddingMethod = EmbeddingMethod.LAPLACIAN_SPECTRAL_EMBEDDING,
        svd_seed: Optional[int] = None,
        num_iterations: int = 5,
        power_iteration_normalizer: str = 'QR',
        num_oversamples: int = 10
) -> List[Tuple[EmbeddingContainer, EmbeddingContainer]]:
    """
    Generates a pairwise omnibus embedding for each pair of graphs in a list of graphs. If given graphs A, B, and C,
    the embeddings will be computed for A,B and B,C.

    There should be exactly the same number of nodes in each graph with exactly the same labels. The list of graphs
    should represent a time series and should be in an order such that time is continuous through the list of graphs.

    If the labels differ between each pair of graphs, then those nodes will _not_ be found in the resulting embedding.

    :param List[networkx.Graph] graphs: A list of graphs that will be used to generate the omnibus embedding. Each graph
        should have exactly the same vertices as each of the other graphs. The order of the graphs in the list matter.
        The first graph will be at time 0 and each following graph will increment time by 1.
    :param int maximum_dimensions: Maximum dimensions of embeddings that will be returned - defaults to 100.  Actual
        dimensions of resulting embeddings should be significantly smaller, but will never be over this value.
    :param int elbow_cut: scree plot elbow detection will detect (usually) many elbows.  This value specifies which
        elbow to use prior to filtering out extraneous dimensions.
    :param topologic.embedding.EmbeddingMethod embedding_method: The embedding technique used to generate the Omnibus
        embedding.
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
    :return: A List of EmbeddingContainers each containing a matrix, which itself contains the embedding for each node.
        the tuple also contains a vector containing the corresponding vertex labels for each row in the matrix.  the
        matrix and vector are positionally correlated.
    :rtype: List[(EmbeddingContainer, EmbeddingContainer)]
    """
    logger = logging.getLogger(__name__)

    if not graphs:
        raise ValueError('Graphs must be provided but was None')

    if len(graphs) <= 1:
        raise ValueError('You must provide at least two graphs to compute the Omnibus embedding but there were only '
                         f'{len(graphs)} graphs.')
    is_directed = nx.is_directed(graphs[0])
    for graph in graphs[1:]:
        if nx.is_directed(graph) != is_directed:
            raise ValueError('All graphs must be either directed or all must be undirected.')

    logger.info('Generating adjacency matrices from list of graphs')
    if embedding_method == EmbeddingMethod.ADJACENCY_SPECTRAL_EMBEDDING:
        get_matrices_function = _get_adjacency_matrices
    elif embedding_method == EmbeddingMethod.LAPLACIAN_SPECTRAL_EMBEDDING:
        get_matrices_function = _get_laplacian_matrices
    else:
        raise TypeError(f'Unexpected EmbeddingMethod for argument embedding_method: {embedding_method}.')

    logger.info('Generating the omnibus embedding')

    embedding_containers = []

    starting_graph = largest_connected_component(graphs[0])
    starting_graph = rank_edges(starting_graph)
    starting_graph = diagonal_augmentation(starting_graph)

    previous_graph = starting_graph
    count = 1

    for graph in graphs[1:]:
        logging.debug(f'Calculating omni for graph {count} of {len(graphs) - 1}')
        count = count + 1
        current_graph = largest_connected_component(graph)
        current_graph = rank_edges(current_graph)
        current_graph = diagonal_augmentation(current_graph)

        pairwise_graphs = [previous_graph] + [current_graph]
        pairwise_graphs_reduced = _reduce_to_common_nodes(pairwise_graphs)

        labels, pairwise_matrices = get_matrices_function(pairwise_graphs_reduced)
        omnibus_matrix = generate_omnibus_matrix(pairwise_matrices)

        embedding = _generate_embedding(
            elbow_cut,
            is_directed,
            omnibus_matrix,
            maximum_dimensions,
            min(omnibus_matrix.shape),
            num_oversamples,
            num_iterations,
            power_iteration_normalizer,
            svd_seed
        )

        number_of_nodes = len(pairwise_graphs_reduced[0].nodes())
        embeddings = [embedding[x: x + number_of_nodes] for x in range(0, embedding.shape[0], number_of_nodes)]

        previous_graph = graph

        embedding_containers.append(
            (EmbeddingContainer(embeddings[0], labels),
             EmbeddingContainer(embeddings[1], labels))
        )

    return embedding_containers


def _reduce_to_common_nodes(graphs: List[nx.Graph]):
    """
    Reduces each graph in the provided list to only the nodes contained in each and every other graph. In other words,
    reduce each graph to be the intersection of nodes of all other graphs.

    :param graphs: The list of graphs to reduce
    :return: A list of pruned graphs
    """
    sets = []
    graphs_copy = copy.deepcopy(graphs)
    for graph in graphs_copy:
        sets.append(set(graph.nodes()))

    set_of_all_common_nodes = set.intersection(*sets)

    # reduce graphs to only have nodes contained in all other graphs
    for graph in graphs_copy:
        to_remove = []
        for node in graph.nodes():
            if node not in set_of_all_common_nodes:
                to_remove.append(node)

        for node in to_remove:
            graph.remove_node(node)

    return graphs_copy


def _get_unstacked_embeddings(embedding, graphs, labels):
    containers = []

    # unstack embeddings and labels
    number_of_nodes = len(graphs[0].nodes())
    embeddings = [embedding[x: x + number_of_nodes] for x in range(0, embedding.shape[0], number_of_nodes)]
    vertex_labels = [labels[x: x + number_of_nodes] for x in range(0, embedding.shape[0], number_of_nodes)]

    for i, embedding in enumerate(embeddings):
        containers.append(
            EmbeddingContainer(
                embedding=embedding,
                vertex_labels=vertex_labels[i]
            )
        )

    return containers


def _get_adjacency_matrices(graphs):
    matrices = []
    labels = []
    for graph in graphs:
        sorted_nodes = sorted(graph.nodes())
        matrices.append(nx.to_scipy_sparse_matrix(graph, nodelist=sorted_nodes))

        for node in sorted_nodes:
            labels.append(node)
    return labels, matrices


def _get_laplacian_matrices(graphs):
    labels, adjacency_matrices = _get_adjacency_matrices(graphs)

    laplacian_matrices = []
    for matrix in adjacency_matrices:
        laplacian_matrices.append(_get_lse_matrix(matrix))

    return labels, laplacian_matrices


def _get_lse_matrix(adjacency_matrix: np.ndarray):
    in_degree = adjacency_matrix.sum(axis=0).astype(float)
    out_degree = adjacency_matrix.sum(axis=1).T.astype(float)

    in_degree_array = np.squeeze(np.asarray(in_degree))
    out_degree_array = np.squeeze(np.asarray(out_degree))

    in_diagonal = sp.sparse.diags(in_degree_array ** (-0.5))
    out_diagonal = sp.sparse.diags(out_degree_array ** (-0.5))

    lse_matrix = out_diagonal.dot(adjacency_matrix).dot(in_diagonal)

    return lse_matrix


def generate_omnibus_matrix(
        matrices: List[Union[np.ndarray, sp.sparse.csr_matrix]]
) -> np.ndarray:
    """
    Generate the omnibus matrix from a list of adjacency or laplacian matrices as described by 'A central limit theorem
    for an omnibus embedding of random dot product graphs.'

    Given an iterable of matrices a, b, ... n then the omnibus matrix is defined as::

        [[           a, .5 * (a + b), ..., .5 * (a + n)],
         [.5 * (b + a),            b, ..., .5 * (b + n)],
         [         ...,          ..., ...,          ...],
         [.5 * (n + a),  .5 * (n + b, ...,            n]
        ]

    The current iteration of this function operates in O(n) but a further optimization could take it to O(.5 * n)

    See also:
        The original paper - https://arxiv.org/abs/1705.09355

    :param matrices: The list of matrices to generate the Omnibus matrix
    :type matrices: List[Union[numpy.ndarray, scipy.sparse.csr_matrix]]
    :return: An Omnibus matrix
    """
    horizontal_stacker, vertical_stacker = _get_stacker_functions(matrices[0])

    rows = []

    # Iterate over each column
    for column_index in range(0, len(matrices)):

        current_row = []
        current_matrix = matrices[column_index]

        for row_index in range(0, len(matrices)):
            if row_index == column_index:
                # we are on the diagonal, we do not need to perform any calculation and instead add the current matrix
                # to the current_row
                current_row.append(current_matrix)
            else:
                # otherwise we are not on the diagonal and we average the current_matrix with the matrix at row_index
                # and add that to our current_row
                matrices_averaged = (current_matrix + matrices[row_index]) * .5
                current_row.append(matrices_averaged)

        # an entire row has been generated, we will create a horizontal stack of each matrix in the row completing the
        # row
        rows.append(horizontal_stacker(current_row))

    return vertical_stacker(rows)


def _get_stacker_functions(matrix):
    if sp.sparse.issparse(matrix):
        horizontal_stacker = sp.sparse.hstack
        vertical_stacker = sp.sparse.vstack
    else:
        horizontal_stacker = np.hstack
        vertical_stacker = np.vstack

    return horizontal_stacker, vertical_stacker
