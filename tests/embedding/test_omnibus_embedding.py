# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import topologic as tc
import scipy as sp
import numpy as np
import networkx as nx


class TestOmnibusEmbedding(unittest.TestCase):
    def test_given_two_2x2_matrices_expected_omnibus_matrix_is_returned(self):
        a = np.array([[1, 2], [3, 4]])
        b = np.array([[5, 6], [7, 8]])

        result = tc.embedding.generate_omnibus_matrix([a, b])

        np.testing.assert_array_equal(
            result,
            np.array(
                [[1, 2, 3, 4],
                 [3, 4, 5, 6],
                 [3, 4, 5, 6],
                 [5, 6, 7, 8]]
            )
        )

    def test_given_two_2x2_sparse_matrices_expected_omnibus_matrix_is_returned(self):
        a = sp.sparse.csr_matrix(np.array([[1, 2], [3, 4]]))
        b = sp.sparse.csr_matrix(np.array([[5, 6], [7, 8]]))

        result = tc.embedding.generate_omnibus_matrix([a, b])

        np.testing.assert_array_equal(
            result.A,
            np.array(
                [[1, 2, 3, 4],
                 [3, 4, 5, 6],
                 [3, 4, 5, 6],
                 [5, 6, 7, 8]]
            )
        )

    def test_given_three_2x2_matrices_expected_omnibus_matrix_is_returned(self):
        a = np.array([[1, 2], [3, 4]])
        b = np.array([[5, 6], [7, 8]])
        c = np.array([[9, 10], [11, 12]])

        result = tc.embedding.generate_omnibus_matrix([a, b, c])

        np.testing.assert_array_equal(
            result,
            np.array(
                [[1, 2, 3, 4, 5, 6],
                 [3, 4, 5, 6, 7, 8],
                 [3, 4, 5, 6, 7, 8],
                 [5, 6, 7, 8, 9, 10],
                 [5, 6, 7, 8, 9, 10],
                 [7, 8, 9, 10, 11, 12]]
            )
        )

    def test_given_three_2x2_sparse_matrices_expected_omnibus_matrix_is_returned(self):
        a = sp.sparse.csr_matrix(np.array([[1, 2], [3, 4]]))
        b = sp.sparse.csr_matrix(np.array([[5, 6], [7, 8]]))
        c = sp.sparse.csr_matrix(np.array([[9, 10], [11, 12]]))

        result = tc.embedding.generate_omnibus_matrix([a, b, c])

        np.testing.assert_array_equal(
            result.A,
            np.array(
                [[1, 2, 3, 4, 5, 6],
                 [3, 4, 5, 6, 7, 8],
                 [3, 4, 5, 6, 7, 8],
                 [5, 6, 7, 8, 9, 10],
                 [5, 6, 7, 8, 9, 10],
                 [7, 8, 9, 10, 11, 12]]
            )
        )

    def test_given_two_3x3_matrices_expected_omnibus_matrix_is_returned(self):
        a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        result = tc.embedding.generate_omnibus_matrix([a, b])

        np.testing.assert_array_equal(
            result,
            np.array(
                [[1, 2, 3, 1, 2, 3],
                 [4, 5, 6, 4, 5, 6],
                 [7, 8, 9, 7, 8, 9],
                 [1, 2, 3, 1, 2, 3],
                 [4, 5, 6, 4, 5, 6],
                 [7, 8, 9, 7, 8, 9]]
            )
        )

    def test_given_two_3x3_sparse_matrices_expected_omnibus_matrix_is_returned(self):
        a = sp.sparse.csr_matrix(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
        b = sp.sparse.csr_matrix(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

        result = tc.embedding.generate_omnibus_matrix([a, b])

        np.testing.assert_array_equal(
            result.A,
            np.array(
                [[1, 2, 3, 1, 2, 3],
                 [4, 5, 6, 4, 5, 6],
                 [7, 8, 9, 7, 8, 9],
                 [1, 2, 3, 1, 2, 3],
                 [4, 5, 6, 4, 5, 6],
                 [7, 8, 9, 7, 8, 9]]
            )
        )

    def test_union_lcc_returns_expected_shape(self):
        first = nx.Graph()
        first.add_edge(0, 1, weight=1)
        first.add_edge(1, 2, weight=1)
        # node 3 and 4 will exist in the union LCC as there is an edge that connects them to the
        # LCC of the union of all edges in first, second
        first.add_edge(3, 4, weight=1)
        # node 5 will not appear in the embedding as it is not in the LCC of the union edges
        first.add_edge(5, 5, weight=1)

        second = nx.Graph()
        second.add_edge(0, 1, weight=1)
        second.add_edge(1, 2, weight=1)
        second.add_edge(3, 1, weight=1)

        result = tc.embedding.omnibus_embedding(
            [first, second]
        )

        self.assertIsNotNone(result)

        for containers in result:
            self.assertEqual(len(containers[0].embedding.shape), len(containers[1].embedding.shape))
            self.assertEqual(len(containers[0].vertex_labels), len(containers[1].vertex_labels))

            self.assertTrue(3 in containers[0].vertex_labels)
            self.assertTrue(4 in containers[0].vertex_labels)
            self.assertTrue(5 not in containers[0].vertex_labels)

    def test_barbell_graph_generates_embedding(self):
        graph = nx.barbell_graph(10, 2)

        for edge in graph.edges():
            graph.add_edge(edge[0], edge[1], weight=1)

        result = tc.embedding.omnibus_embedding(
            [graph, graph],
            embedding_method=tc.embedding.EmbeddingMethod.ADJACENCY_SPECTRAL_EMBEDDING,
            elbow_cut=None
        )

        self.assertIsNotNone(result)

        for containers in result:
            self.assertEqual(len(containers[0].embedding.shape), len(containers[1].embedding.shape))
            self.assertEqual(len(containers[0].vertex_labels), len(containers[1].vertex_labels))

    def test_barbell_graph_generates_laplacian_embedding(self):
        graph = nx.barbell_graph(10, 2)

        for edge in graph.edges():
            graph.add_edge(edge[0], edge[1], weight=1)

        result = tc.embedding.omnibus_embedding(
            [graph, graph],
            embedding_method=tc.embedding.EmbeddingMethod.LAPLACIAN_SPECTRAL_EMBEDDING,
            elbow_cut=None
        )

        self.assertIsNotNone(result)

        for containers in result:
            self.assertEqual(len(containers[0].embedding.shape), len(containers[1].embedding.shape))
            self.assertEqual(len(containers[0].vertex_labels), len(containers[1].vertex_labels))

    def test_invalid_embedding_method_throws_exception(self):
        graph = nx.barbell_graph(10, 2)

        for edge in graph.edges():
            graph.add_edge(edge[0], edge[1], weight=1)

        with self.assertRaises(TypeError):
            tc.embedding.omnibus_embedding(
                [graph, graph],
                elbow_cut=None,
                embedding_method=-1
            )

    def test_None_graphs_raises_error(self):
        with self.assertRaises(ValueError):
            tc.embedding.omnibus_embedding(
                None
            )

    def test_0_graphs_raises_error(self):
        with self.assertRaises(ValueError):
            tc.embedding.omnibus_embedding(
                []
            )

    def test_1_graphs_raises_error(self):
        with self.assertRaises(ValueError):
            tc.embedding.omnibus_embedding(
                [nx.Graph()]
            )


if __name__ == '__main__':
    unittest.main()
