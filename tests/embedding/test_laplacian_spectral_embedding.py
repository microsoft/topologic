# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
import numpy as np
import pickle
from topologic.embedding import laplacian_embedding


class TestLaplacianSpectralEmbedding(unittest.TestCase):
    def test_laplacian_embedding(self):
        graph = nx.Graph([('a', 'b', {'weight': 1.0}), ('b', 'c', {'weight': 2.0})])
        result = laplacian_embedding(
            graph,
            elbow_cut=1,
            svd_seed=1234
        )
        self.assertIsNotNone(result)
        (matrix, labels) = result
        self.assertIsInstance(matrix, np.ndarray)
        self.assertIsInstance(labels, list)
        self.assertEqual(2, matrix.ndim)
        expected_matrix = np.array([[0.408248],
                                    [0.707107],
                                    [0.577350]])
        expected_label = ['a', 'b', 'c']
        np.testing.assert_allclose(expected_matrix, matrix, rtol=1e-5)
        self.assertListEqual(expected_label, labels)

    def test_laplacian_embedding_elbowcut_none(self):
        graph = nx.Graph([('a', 'b', {'weight': 1.0}), ('b', 'c', {'weight': 2.0})])
        result = laplacian_embedding(
            graph,
            elbow_cut=None,
            svd_seed=1234
        )
        self.assertIsNotNone(result)
        (matrix, labels) = result
        self.assertIsInstance(matrix, np.ndarray)
        self.assertIsInstance(labels, list)
        self.assertEqual(2, matrix.ndim)
        expected_matrix = np.array([[0.408248, 0.421637],
                                    [0.707107, -0.365148],
                                    [0.57735, 0.149071]])
        expected_label = ['a', 'b', 'c']
        np.testing.assert_allclose(expected_matrix, matrix, rtol=1e-5)
        self.assertListEqual(expected_label, labels)

    def test_laplacian_embedding_gpickle(self):
        graph = nx.Graph([('a', 'b', {'weight': 1.0}), ('b', 'c', {'weight': 2.0})])
        result = laplacian_embedding(graph, svd_seed=1234)
        pickled = pickle.dumps(result)
        unpickled = pickle.loads(pickled)

        np.testing.assert_array_equal(result.embedding, unpickled.embedding)
        np.testing.assert_array_equal(result.vertex_labels, unpickled.vertex_labels)
