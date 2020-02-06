# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

# Reference implementation of node2vec.
# https://github.com/aditya-grover/node2vec/
#
# Author: Aditya Grover
#
# For more details, refer to the paper:
# node2vec: Scalable Feature Learning for Networks
# Aditya Grover and Jure Leskovec
#
# Knowledge Discovery and Data Mining (KDD), 2016


import logging
import time

import networkx as nx

from .embedding_container import EmbeddingContainer
from .node2vec_graph import _Node2VecGraph


def node2vec_embedding(
        graph: nx.Graph,
        num_walks: int = 10,
        walk_length: int = 80,
        return_hyperparameter: int = 1,
        inout_hyperparameter: int = 1,
        dimensions: int = 128,
        window_size: int = 10,
        workers: int = 8,
        iterations: int = 1,
        interpolate_walk_lengths_by_node_degree: bool = True
) -> EmbeddingContainer:
    """
    Generates a node2vec embedding from a given graph. Will follow the word2vec algorithm to create the embedding.

    :param networkx.Graph graph: A networkx graph. If the graph is unweighted, the weight of each edge will default to 1
    :param int num_walks: Number of walks per source. Default is 10.
    :param int walk_length: Length of walk per source. Default is 80.
    :param int return_hyperparameter: Return hyperparameter (p). Default is 1.
    :param int inout_hyperparameter: Inout hyperparameter (q). Default is 1.
    :param int dimensions: Dimensionality of the word vectors. Default is 128.
    :param int window_size: Maximum distance between the current and predicted word within a sentence. Default is 10.
    :param int workers: Use these many worker threads to train the model. Default is 8.
    :param int iterations: Number of epochs in stochastic gradient descent (SGD)
    :param bool interpolate_walk_lengths_by_node_degree: Use a dynamic walk length that corresponds to each nodes
        degree. If the node is in the bottom 20 percentile, default to a walk length of 1. If it is in the top 10
        percentile, use walk_length. If it is in the 20-80 percentiles, linearly interpolate between 1 and walk_length.

        This will reduce lower degree nodes from biasing your resulting embedding. If a low degree node has the same
        number of walks as a high degree node (which it will if this setting is not on), then the lower degree nodes
        will take a smaller breadth of random walks when compared to the high degree nodes. This will result in your
        lower degree walks dominating your higher degree nodes.
    :return: tuple containing a matrix, which itself contains the embedding for each node.  the tuple also contains
        a vector containing the corresponding vertex labels for each row in the matrix.  the matrix and vector are
        positionally correlated.
    :rtype: EmbeddingContainer
    """
    node2vec_graph = _Node2VecGraph(
        graph,
        return_hyperparameter,
        inout_hyperparameter
    )

    logging.info(
        f'Starting preprocessing of transition probabilities on graph with {str(len(graph.nodes()))} nodes and '
        f'{str(len(graph.edges()))} edges'
    )

    start = time.time()
    logging.info(f'Starting at time {str(start)}')

    node2vec_graph.preprocess_transition_probabilities()

    logging.info(f'Simulating walks on graph at time {str(time.time())}')
    walks = node2vec_graph.simulate_walks(num_walks, walk_length, interpolate_walk_lengths_by_node_degree)

    logging.info(f'Learning embeddings at time {str(time.time())}')
    model = _learn_embeddings(walks, dimensions, window_size, workers, iterations)

    end = time.time()
    logging.info(f'Completed. Ending time is {str(end)} Elapsed time is {str(start - end)}')

    return EmbeddingContainer(embedding=model.wv.vectors, vertex_labels=model.wv.index2word)


def _learn_embeddings(walks: list,
                      dimensions: int,
                      window_size: int,
                      workers,
                      iterations):
    """
    Learn embeddings by optimizing the skip-gram objective using SGD.
    """
    from gensim.models import Word2Vec

    walks = [list(map(str, walk)) for walk in walks]

    # Documentation - https://radimrehurek.com/gensim/models/word2vec.html
    model = Word2Vec(walks,
                     size=dimensions,
                     window=window_size,
                     min_count=0,
                     sg=1,  # Training algorithm: 1 for skip-gram; otherwise CBOW
                     workers=workers,
                     iter=iterations)

    return model
