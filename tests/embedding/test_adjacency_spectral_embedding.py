# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
import numpy as np
import pickle
from topologic.embedding import adjacency_embedding


class TestAdjacencySpectralEmbedding(unittest.TestCase):
    def test_adjacency_embedding(self):
        graph = nx.Graph([('a', 'b', {'weight': 1.0}), ('b', 'c', {'weight': 2.0})])
        result = adjacency_embedding(
            graph,
            elbow_cut=1,
            svd_seed=1234
        )
        self.assertIsNotNone(result)
        (matrix, labels) = result
        self.assertIsInstance(matrix, np.ndarray)
        self.assertIsInstance(labels, list)
        self.assertEqual(2, matrix.ndim)
        expected_matrix = np.array([[0.385095],
                                    [1.140718],
                                    [0.926595]])
        expected_label = ['a', 'b', 'c']
        np.testing.assert_allclose(expected_matrix, matrix, rtol=1e-6)
        self.assertListEqual(expected_label, labels)

    def test_adjacency_embedding_elbowcut_none(self):
        graph = nx.Graph([('a', 'b', {'weight': 1.0}), ('b', 'c', {'weight': 2.0})])
        result = adjacency_embedding(
            graph,
            elbow_cut=None,
            svd_seed=1234
        )
        self.assertIsNotNone(result)
        (matrix, labels) = result
        self.assertIsInstance(matrix, np.ndarray)
        self.assertIsInstance(labels, list)
        self.assertEqual(2, matrix.ndim)
        expected_matrix = np.array([[0.385095, -0.351718],
                                    [1.140718, 0.552094],
                                    [0.926595, -0.5335]])
        expected_label = ['a', 'b', 'c']
        np.testing.assert_allclose(expected_matrix, matrix, rtol=1e-5)
        self.assertListEqual(expected_label, labels)

    def test_adjacency_embedding_gpickle(self):
        networkx_graph = nx.Graph([('a', 'b', {'weight': 1.0}), ('b', 'c', {'weight': 2.0})])
        result = adjacency_embedding(networkx_graph, svd_seed=1234)
        pickled = pickle.dumps(result)
        unpickled = pickle.loads(pickled)

        np.testing.assert_array_equal(result.embedding, unpickled.embedding)
        np.testing.assert_array_equal(result.vertex_labels, unpickled.vertex_labels)
