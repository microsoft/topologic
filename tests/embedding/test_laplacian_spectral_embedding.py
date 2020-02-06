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
        expected_matrix = np.array([[0.44095855],
                                    [0.70710678],
                                    [0.5527708]])
        expected_label = ['a', 'b', 'c']
        np.testing.assert_allclose(expected_matrix, matrix)
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
        expected_matrix = np.array([[0.44095855, 0.51959271],
                                    [0.70710678, -0.06490658],
                                    [0.5527708, -0.33146281]])
        expected_label = ['a', 'b', 'c']
        np.testing.assert_allclose(expected_matrix, matrix)
        self.assertListEqual(expected_label, labels)

    def test_laplacian_embedding_gpickle(self):
        graph = nx.Graph([('a', 'b', {'weight': 1.0}), ('b', 'c', {'weight': 2.0})])
        result = laplacian_embedding(graph, svd_seed=1234)
        pickled = pickle.dumps(result)
        unpickled = pickle.loads(pickled)

        np.testing.assert_array_equal(result.embedding, unpickled.embedding)
        np.testing.assert_array_equal(result.vertex_labels, unpickled.vertex_labels)
