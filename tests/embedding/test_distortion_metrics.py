# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import topologic as tc
import networkx as nx
import numpy as np


class TestDistortionMetrics(unittest.TestCase):
    def test_mean_average_precision_calculated_correctly(self):
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (0, 2), (2, 0), (2, 1), (1, 0), (3, 2), (3, 1)])

        embedding = np.array([[0, 0], [0, 1], [1, 1], [0.5, 1]])
        label_indices = [0, 1, 2, 3]
        emb_container = tc.embedding.EmbeddingContainer(embedding=embedding, vertex_labels=label_indices)

        expected_mean_avg_precision = 0.9583

        calculated_mean_avg_precision = tc.embedding.distortion_metrics.mean_average_precision(graph, emb_container)

        self.assertAlmostEqual(expected_mean_avg_precision, calculated_mean_avg_precision, places=4)

    def test_mean_average_precision_graph_not_specified_error_raised(self):
        embedding_container = tc.embedding.EmbeddingContainer(embedding=[[0]], vertex_labels=[0])

        with self.assertRaises(ValueError):
            tc.embedding.distortion_metrics.mean_average_precision(None, embedding_container)

    def test_mean_average_precision_embedding_not_specified_error_raised(self):
        with self.assertRaises(ValueError):
            tc.embedding.distortion_metrics.mean_average_precision(nx.Graph(), None)
