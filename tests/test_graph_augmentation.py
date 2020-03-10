# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
import numpy as np
from topologic import diagonal_augmentation


class TestDiagonalAugmentation(unittest.TestCase):
    def test_diag_aug_for_a_non_graph_raises_exception(self):
        with self.assertRaises(TypeError) as raised:
            diagonal_augmentation('not a graph')

        self.assertTrue('must be a networkx.Graph' in str(raised.exception))

    def test_diag_aug_for_2_nodes_self_loops(self):
        graph = nx.Graph([('a', 'b'), ('b', 'c'), ('a', 'a'), ('b', 'b'), ('c', 'c')])
        expected_set = {('a', 'a', 0.5), ('a', 'b', None), ('b', 'b', 1.0), ('b', 'c', None), ('c', 'c', 0.5)}

        augmented = diagonal_augmentation(graph)
        ranked_edge_set = set(augmented.edges(data='weight'))

        self.assertEqual(augmented, graph)
        self.assertEqual(expected_set, ranked_edge_set)

    def test_diag_aug_for_2_nodes_no_self_loops(self):
        graph = nx.Graph([('a', 'b'), ('b', 'c')])
        expected_set = {('a', 'a', 0.5), ('a', 'b', None), ('b', 'b', 1.0), ('b', 'c', None), ('c', 'c', 0.5)}

        augmented = diagonal_augmentation(graph)
        ranked_edge_set = set(augmented.edges(data='weight'))

        self.assertEqual(augmented, graph)
        self.assertEqual(expected_set, ranked_edge_set)

    def test_undirected_uses_weighted_degree(self):
        start_adajacency = np.array(
            [
                [0, 1, 1, 0, 0],
                [1, 0, 0, 2, 1],
                [1, 0, 0, 1, 1],
                [0, 2, 1, 0, 0],
                [0, 1, 1, 0, 0],
            ]
        )
        expected = [
            [.5, 1, 1, 0, 0],
            [1, 1, 0, 2, 1],
            [1, 0, .75, 1, 1],
            [0, 2, 1, .75, 0],
            [0, 1, 1, 0, .5]
        ]

        g = diagonal_augmentation(nx.Graph(start_adajacency))
        augmented_adjacency = nx.adj_matrix(g).todense()

        np.testing.assert_array_equal(
            augmented_adjacency,
            expected
        )

    def test_directed_averages_in_out_edge_weights(self):
        start_adajacency = np.array(
            [
                [0, 1, -1, 0, 0],
                [0, 0, 0, 2, 1],
                [1, 0, 0, 1, 1],
                [0, 2, 0, 0, 0],
                [0, 0, 1, 0, 0],
            ]
        )
        expected = [
            [.125, 1, -1, 0, 0],
            [0, .75, 0, 2, 1],
            [1, 0, .375, 1, 1],
            [0, 2, 0, .625, 0],
            [0, 0, 1, 0, .375],
        ]

        g = diagonal_augmentation(nx.DiGraph(start_adajacency))
        augmented_adjacency = nx.adj_matrix(g).todense()

        np.testing.assert_array_equal(
            augmented_adjacency,
            expected
        )
