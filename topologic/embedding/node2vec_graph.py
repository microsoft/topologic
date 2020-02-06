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
import random

import math
import numpy as np
import networkx as nx
from typing import List


class _Node2VecGraph:
    def __init__(
            self,
            graph: nx.Graph,
            p: float,
            q: float
    ):
        """
        :param graph: A networkx graph
        :param p: Return hyperparameter
        :param q: Inout hyperparameter
        """
        self.graph: nx.Graph = graph
        self.is_directed = self.graph.is_directed()
        self.p = p
        self.q = q

    def node2vec_walk(self, walk_length, start_node, degree_percentiles):
        """
        Simulate a random walk starting from start node.
        """
        G = self.graph
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
            degree = nx.degree(G, start_node)
            walk_length = self._get_walk_length_interpolated(degree, degree_percentiles, walk_length)

        while len(walk) < walk_length:
            cur = walk[-1]
            cur_nbrs = sorted(G.neighbors(cur))

            if len(cur_nbrs) > 0:
                if len(walk) == 1:
                    walk.append(cur_nbrs[_alias_draw(alias_nodes[cur][0], alias_nodes[cur][1])])
                else:
                    prev = walk[-2]
                    next = cur_nbrs[_alias_draw(alias_edges[(prev, cur)][0],
                                                alias_edges[(prev, cur)][1])]
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

    def simulate_walks(self, num_walks, walk_length, interpolate_walk_lengths_by_node_degree=False):
        """
        Repeatedly simulate random walks from each node.
        """
        G = self.graph
        walks = []
        nodes = list(G.nodes())

        degree_percentiles = None
        if interpolate_walk_lengths_by_node_degree:
            degree_percentiles = np.percentile(
                [degree for _, degree in G.degree()],
                [x for x in range(20, 90, 10)]
            )

        for walk_iter in range(num_walks):
            logging.info('Walk iteration: ' + str(walk_iter + 1) + '/' + str(num_walks))
            random.shuffle(nodes)
            for node in nodes:
                walks.append(self.node2vec_walk(
                    walk_length=walk_length,
                    start_node=node,
                    degree_percentiles=degree_percentiles
                ))

        return walks

    def get_alias_edge(self, src, dst):
        """
        Get the alias edge setup lists for a given edge.
        """
        G = self.graph
        p = self.p
        q = self.q

        unnormalized_probs = []
        for dst_nbr in sorted(G.neighbors(dst)):
            if dst_nbr == src:
                unnormalized_probs.append(G[dst][dst_nbr].get('weight', 1) / p)
            elif G.has_edge(dst_nbr, src):
                unnormalized_probs.append(G[dst][dst_nbr].get('weight', 1))
            else:
                unnormalized_probs.append(G[dst][dst_nbr].get('weight', 1) / q)
        norm_const = sum(unnormalized_probs)
        normalized_probs = [float(u_prob) / norm_const for u_prob in unnormalized_probs]

        return _alias_setup(normalized_probs)

    def preprocess_transition_probabilities(
            self,
            weight_default=1
    ):
        """
        Preprocessing of transition probabilities for guiding the random walks.
        """
        G = self.graph
        is_directed = self.is_directed

        alias_nodes = {}
        total_nodes = len(G.nodes())
        bucket = 0
        current_node = 0
        quotient = int(total_nodes / 10)

        logging.info(f'Beginning preprocessing of transition probabilities for {total_nodes} vertices')
        for node in G.nodes():
            current_node += 1
            if current_node > bucket * quotient:
                bucket += 1
                logging.info(f'Completed {current_node} / {total_nodes} vertices')

            unnormalized_probs = [G[node][nbr].get('weight', weight_default) for nbr in sorted(G.neighbors(node))]
            norm_const = sum(unnormalized_probs)
            normalized_probs = [float(u_prob) / norm_const for u_prob in unnormalized_probs]
            alias_nodes[node] = _alias_setup(normalized_probs)
        logging.info(f'Completed preprocessing of transition probabilities for vertices')

        alias_edges = {}

        total_edges = len(G.edges())
        bucket = 0
        current_edge = 0
        quotient = int(total_edges / 10)

        logging.info(f'Beginning preprocessing of transition probabilities for {total_edges} edges')
        if is_directed:
            for edge in G.edges():
                current_edge += 1
                if current_edge > bucket * quotient:
                    bucket += 1
                    logging.info(f'Completed {current_edge} / {total_edges} edges')

                alias_edges[edge] = self.get_alias_edge(edge[0], edge[1])
        else:
            for edge in G.edges():
                current_edge += 1
                if current_edge > bucket * quotient:
                    bucket += 1
                    logging.info(f'Completed {current_edge} / {total_edges} edges')

                alias_edges[edge] = self.get_alias_edge(edge[0], edge[1])
                alias_edges[(edge[1], edge[0])] = self.get_alias_edge(edge[1], edge[0])

        logging.info(f'Completed preprocessing of transition probabilities for edges')

        self.alias_nodes = alias_nodes
        self.alias_edges = alias_edges

        return


def _alias_setup(probs):
    """
    Compute utility lists for non-uniform sampling from discrete distributions.
    Refer to
     https://hips.seas.harvard.edu/blog/2013/03/03/the-alias-method-efficient-sampling-with-many-discrete-outcomes/
    for details
    """
    K = len(probs)
    q = np.zeros(K)
    J = np.zeros(K, dtype=np.int)

    smaller = []
    larger = []
    for kk, prob in enumerate(probs):
        q[kk] = K * prob
        if q[kk] < 1.0:
            smaller.append(kk)
        else:
            larger.append(kk)

    while len(smaller) > 0 and len(larger) > 0:
        small = smaller.pop()
        large = larger.pop()

        J[small] = large
        q[large] = q[large] + q[small] - 1.0
        if q[large] < 1.0:
            smaller.append(large)
        else:
            larger.append(large)

    return J, q


def _alias_draw(J, q):
    """
    Draw sample from a non-uniform discrete distribution using alias sampling.
    """
    K = len(J)

    kk = int(np.floor(np.random.rand() * K))
    if np.random.rand() < q[kk]:
        return kk
    else:
        return J[kk]
