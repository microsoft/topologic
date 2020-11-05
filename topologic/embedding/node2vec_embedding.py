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
import math
import random
import time
from typing import List

import networkx
import networkx as nx
import numpy as np

from .embedding_container import EmbeddingContainer


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

    node2vec_graph._preprocess_transition_probabilities()

    logging.info(f'Simulating walks on graph at time {str(time.time())}')
    walks = node2vec_graph._simulate_walks(num_walks, walk_length, interpolate_walk_lengths_by_node_degree)

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
    model = Word2Vec(
        walks,
        size=dimensions,
        window=window_size,
        min_count=0,
        sg=1,  # Training algorithm: 1 for skip-gram; otherwise CBOW
        workers=workers,
        iter=iterations
    )

    return model


class _Node2VecGraph:
    def __init__(
            self,
            graph: nx.Graph,
            return_hyperparameter: float,
            inout_hyperparameter: float
    ):
        """
        :param graph: A networkx graph
        :param return_hyperparameter: Return hyperparameter
        :param inout_hyperparameter: Inout hyperparameter
        """
        self.graph: nx.Graph = graph
        self.is_directed = self.graph.is_directed()
        self.p = return_hyperparameter
        self.q = inout_hyperparameter

    def _node2vec_walk(self, walk_length, start_node, degree_percentiles):
        """
        Simulate a random walk starting from start node.
        """
        graph = self.graph
        alias_nodes = self.alias_nodes
        alias_edges = self.alias_edges

        walk = [start_node]

        # Percentiles will be provided if we are using the 'interpolate_walk_lengths_by_node_degree' feature.
        # the intent of the code is to default the bottom 20% of to a minimal walk length, default the top 10% to a
        # maximum walk length, and interpolate the inner 70% linearly from min to max.

        # This is to avoid having your random walks be dominated by low degree nodes. If the low degree nodes have the
        # same number of walks as the high degree nodes, the low degree nodes will take a smaller breadth of paths
        # (due to their being less nodes to choose from) and will bias your resulting Word2Vec embedding
        if degree_percentiles is not None:
            degree = nx.degree(graph, start_node)
            walk_length = self._get_walk_length_interpolated(degree, degree_percentiles, walk_length)

        while len(walk) < walk_length:
            current = walk[-1]
            current_neighbors = sorted(graph.neighbors(current))

            if len(current_neighbors) > 0:
                if len(walk) == 1:
                    walk.append(current_neighbors[_alias_draw(alias_nodes[current][0], alias_nodes[current][1])])
                else:
                    prev = walk[-2]
                    next = current_neighbors[_alias_draw(alias_edges[(prev, current)][0],
                                                         alias_edges[(prev, current)][1])]
                    walk.append(next)
            else:
                break

        return walk

    @staticmethod
    def _get_walk_length_interpolated(
            degree: int,
            percentiles: List[float],
            max_walk_length: int
    ):
        """
        Given a node's degree, determine the length of a walk that should be used. If the degree is less than the
        first element of the percentiles list, default the walk length to 1. Otherwise, if the degree is greater
        than the last element of the list, default it to the max_walk_length. If it falls in the middle, do a linear
        interpolation to decide the length of the walk.
        """

        new_walk_length = None

        for i, percentile in enumerate(percentiles):
            # if we are below the first percentile in the list, default to a walk length of 1
            if i == 0 and degree < percentile:
                return 1

            # otherwise, find which bucket we are going to be in.
            if degree <= percentile:
                new_walk_length = max_walk_length * ((i * .1) + .2)
                break

        # the degree is above the last percentile
        if not new_walk_length:
            new_walk_length = max_walk_length

        # a walk length of 0 is invalid but can happen depending on the percentiles used
        if new_walk_length < 1:
            new_walk_length = 1

        return math.floor(new_walk_length)

    def _simulate_walks(self, num_walks, walk_length, interpolate_walk_lengths_by_node_degree=False):
        """
        Repeatedly simulate random walks from each node.
        """
        graph = self.graph
        walks = []
        nodes = list(graph.nodes())

        degree_percentiles = None
        if interpolate_walk_lengths_by_node_degree:
            degree_percentiles = np.percentile(
                [degree for _, degree in graph.degree()],
                [x for x in range(20, 90, 10)]
            )

        for walk_iteration in range(num_walks):
            logging.info('Walk iteration: ' + str(walk_iteration + 1) + '/' + str(num_walks))
            random.shuffle(nodes)
            for node in nodes:
                walks.append(self._node2vec_walk(
                    walk_length=walk_length,
                    start_node=node,
                    degree_percentiles=degree_percentiles
                ))

        return walks

    def _get_alias_edge(self, source, destination):
        """
        Get the alias edge setup lists for a given edge.
        """
        graph = self.graph
        p = self.p
        q = self.q

        unnormalized_probs = []
        for destination_neighbor in sorted(graph.neighbors(destination)):
            if destination_neighbor == source:
                unnormalized_probs.append(graph[destination][destination_neighbor].get('weight', 1) / p)
            elif graph.has_edge(destination_neighbor, source):
                unnormalized_probs.append(graph[destination][destination_neighbor].get('weight', 1))
            else:
                unnormalized_probs.append(graph[destination][destination_neighbor].get('weight', 1) / q)
        norm_const = sum(unnormalized_probs)
        normalized_probs = [float(u_prob) / norm_const for u_prob in unnormalized_probs]

        return _alias_setup(normalized_probs)

    def _preprocess_transition_probabilities(
            self,
            weight_default=1
    ):
        """
        Preprocessing of transition probabilities for guiding the random walks.
        """
        graph = self.graph
        is_directed = self.is_directed

        alias_nodes = {}
        total_nodes = len(graph.nodes())
        bucket = 0
        current_node = 0
        quotient = int(total_nodes / 10)

        logging.info(f'Beginning preprocessing of transition probabilities for {total_nodes} vertices')
        for node in graph.nodes():
            current_node += 1
            if current_node > bucket * quotient:
                bucket += 1
                logging.info(f'Completed {current_node} / {total_nodes} vertices')

            unnormalized_probs = [graph[node][nbr].get('weight', weight_default)
                                  for nbr in sorted(graph.neighbors(node))]
            norm_const = sum(unnormalized_probs)
            normalized_probs = [float(u_prob) / norm_const for u_prob in unnormalized_probs]
            alias_nodes[node] = _alias_setup(normalized_probs)
        logging.info('Completed preprocessing of transition probabilities for vertices')

        alias_edges = {}

        total_edges = len(graph.edges())
        bucket = 0
        current_edge = 0
        quotient = int(total_edges / 10)

        logging.info(f'Beginning preprocessing of transition probabilities for {total_edges} edges')
        if is_directed:
            for edge in graph.edges():
                current_edge += 1
                if current_edge > bucket * quotient:
                    bucket += 1
                    logging.info(f'Completed {current_edge} / {total_edges} edges')

                alias_edges[edge] = self._get_alias_edge(edge[0], edge[1])
        else:
            for edge in graph.edges():
                current_edge += 1
                if current_edge > bucket * quotient:
                    bucket += 1
                    logging.info(f'Completed {current_edge} / {total_edges} edges')

                alias_edges[edge] = self._get_alias_edge(edge[0], edge[1])
                alias_edges[(edge[1], edge[0])] = self._get_alias_edge(edge[1], edge[0])

        logging.info('Completed preprocessing of transition probabilities for edges')

        self.alias_nodes = alias_nodes
        self.alias_edges = alias_edges

        return


def _alias_setup(probabilities):
    """
    Compute utility lists for non-uniform sampling from discrete distributions.
    Refer to
     https://lips.cs.princeton.edu/the-alias-method-efficient-sampling-with-many-discrete-outcomes/
    for details
    """
    number_of_outcomes = len(probabilities)
    alias = np.zeros(number_of_outcomes)
    sampled_probabilities = np.zeros(number_of_outcomes, dtype=np.int)

    smaller = []
    larger = []
    for i, prob in enumerate(probabilities):
        alias[i] = number_of_outcomes * prob
        if alias[i] < 1.0:
            smaller.append(i)
        else:
            larger.append(i)

    while len(smaller) > 0 and len(larger) > 0:
        small = smaller.pop()
        large = larger.pop()

        sampled_probabilities[small] = large
        alias[large] = alias[large] + alias[small] - 1.0
        if alias[large] < 1.0:
            smaller.append(large)
        else:
            larger.append(large)

    return sampled_probabilities, alias


def _alias_draw(probabilities, alias):
    """
    Draw sample from a non-uniform discrete distribution using alias sampling.
    """
    number_of_outcomes = len(probabilities)
    random_index = int(np.floor(np.random.rand() * number_of_outcomes))

    if np.random.rand() < alias[random_index]:
        return random_index
    else:
        return probabilities[random_index]
