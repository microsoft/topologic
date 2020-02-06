# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import topologic as tc
import networkx as nx
import numpy as np
from topologic.embedding.node2vec_graph import _Node2VecGraph
from tests.utils import data_file


class TestNode2VecEmbedding(unittest.TestCase):
    def test_node2vec_embedding_correct_shape_is_returned(self):
        graph = nx.read_edgelist(data_file('node2vec_edge_list.txt'), nodetype=int, create_using=nx.DiGraph())

        model = tc.embedding.node2vec_embedding(graph)
        model_matrix: np.ndarray = model[0]
        vocab_list = model[1]
        self.assertIsNotNone(model)
        self.assertIsNotNone(model[0])
        self.assertIsNotNone(model[1])

        # model matrix should be 34 x 128
        self.assertEqual(model_matrix.shape[0], 34)
        self.assertEqual(model_matrix.shape[1], 128)

        # vocab list should have exactly 34 elements
        self.assertEqual(len(vocab_list), 34)

    def test_node2vec_embedding_florentine_graph_correct_shape_is_returned(self):
        graph = nx.florentine_families_graph()
        for s, t in graph.edges():
            graph.add_edge(s, t, weight=1)

        model = tc.embedding.node2vec_embedding(graph)
        model_matrix: np.ndarray = model[0]
        vocab_list = model[1]
        self.assertIsNotNone(model)
        self.assertIsNotNone(model[0])
        self.assertIsNotNone(model[1])

        # model matrix should be 34 x 128
        self.assertEqual(model_matrix.shape[0], 15)
        self.assertEqual(model_matrix.shape[1], 128)

        # vocab list should have exactly 34 elements
        self.assertEqual(len(vocab_list), 15)

    def test_node2vec_embedding_barbell_graph_correct_shape_is_returned(self):
        graph = nx.barbell_graph(25, 2)
        for s, t in graph.edges():
            graph.add_edge(s, t, weight=1)

        model = tc.embedding.node2vec_embedding(graph)
        model_matrix: np.ndarray = model[0]
        vocab_list = model[1]
        self.assertIsNotNone(model)
        self.assertIsNotNone(model[0])
        self.assertIsNotNone(model[1])

        # model matrix should be 34 x 128
        self.assertEqual(model_matrix.shape[0], 52)
        self.assertEqual(model_matrix.shape[1], 128)

        # vocab list should have exactly 34 elements
        self.assertEqual(len(vocab_list), 52)

    def test_get_walk_length_lower_defaults_to_1(self):
        expected_walk_length = 1

        g = _Node2VecGraph(nx.Graph(), 1, 1)
        w = g._get_walk_length_interpolated(
            degree=0,
            percentiles=[1, 2, 3, 4, 10, 100],
            max_walk_length=10
        )

        self.assertEqual(w, expected_walk_length)

    def test_get_walk_length_higher_default_to_walk_length(self):
        expected_walk_length = 100

        g = _Node2VecGraph(nx.Graph(), 1, 1)
        w = g._get_walk_length_interpolated(
            degree=10,
            percentiles=[2, 3, 4, 5, 6, 7, 8, 9],
            max_walk_length=expected_walk_length
        )

        self.assertEqual(w, expected_walk_length)

    def test_get_walk_length_in_middle_selects_interpolated_bucket(self):
        expected_walk_length = 5

        g = _Node2VecGraph(nx.Graph(), 1, 1)
        w = g._get_walk_length_interpolated(
            degree=5,
            percentiles=[2, 3, 4, 5, 6, 7, 8, 9],
            max_walk_length=10
        )

        self.assertEqual(w, expected_walk_length)


if __name__ == '__main__':
    unittest.main()
