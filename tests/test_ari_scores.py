# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
import topologic as tc
import numpy as np


class TestAriScores(unittest.TestCase):
    def test_smoke_test_simple(self):
        a = [1, 1, 2, 3]
        b = [1, 2, 2, 3]

        score: float = tc.calculate_ari(a, b)

        # Check the distances
        self.assertEqual(-0.20, round(score, ndigits=1))

    def test_smoke_test(self):
        graph = nx.Graph()
        graph.add_edge("one", "two")
        graph.add_edge("two", "three")
        graph.add_edge("three", "four")
        graph.add_edge("four", "one")

        graph.add_node("one", reference_cluster=1, pred_cluster1=1, pred_cluster2=1)
        graph.add_node("two", reference_cluster=1, pred_cluster1=2, pred_cluster2=1)
        graph.add_node("three", reference_cluster=2, pred_cluster1=2, pred_cluster2=2)
        graph.add_node("four", reference_cluster=3, pred_cluster1=3, pred_cluster2=3)

        # Check the distance between "pred_cluster1" and "reference_cluster" as well as "pred_cluster2"
        # and "reference_cluster"
        result: np.ndarray = tc.calculate_ari_scores(graph, "reference_cluster", ["pred_cluster1", "pred_cluster2"])

        # Check the distances
        self.assertEqual(2, result.size)
        self.assertEqual(-0.20, round(result[0], ndigits=1))
        self.assertEqual(1.0, result[1])

    def test_invalid_reference_cluster_type(self):
        graph = nx.Graph()
        graph.add_edge("one", "two")

        graph.add_node("one", reference_cluster=1, pred_cluster1=1, pred_cluster2=1)
        graph.add_node("two", reference_cluster="one", pred_cluster1=1, pred_cluster2=1)
        with self.assertRaises(ValueError):
            tc.calculate_ari_scores(graph, "reference_cluster", ["pred_cluster1", "pred_cluster2"])

    def test_invalid_pred_cluster_type(self):
        graph = nx.Graph()
        graph.add_edge("one", "two")

        graph.add_node("one", reference_cluster=1, pred_cluster1=1, pred_cluster2=1)
        graph.add_node("two", reference_cluster=1, pred_cluster1=1, pred_cluster2="one")
        with self.assertRaises(ValueError):
            tc.calculate_ari_scores(graph, "reference_cluster", ["pred_cluster1", "pred_cluster2"])

    def test_reference_cluster_not_defined(self):
        graph = nx.Graph()
        graph.add_edge("one", "two")

        graph.add_node("one", reference_cluster=1, pred_cluster1=1, pred_cluster2=1)
        graph.add_node("two", reference_cluster="one", pred_cluster1=1, pred_cluster2=1)
        with self.assertRaises(KeyError):
            tc.calculate_ari_scores(graph, "reference_cluster_invalid", ["pred_cluster1", "pred_cluster2"])

    def test_pred2_cluster_not_defined(self):
        graph = nx.Graph()
        graph.add_edge("one", "two")

        graph.add_node("one", reference_cluster=1, pred_cluster1=1, pred_cluster2=1)
        graph.add_node("two", reference_cluster=1, pred_cluster1=1, pred_cluster2=1)
        with self.assertRaises(KeyError):
            tc.calculate_ari_scores(graph, "reference_cluster", ["pred_cluster1", "pred_cluster2_invalid"])

    def test_graph_not_a_graph(self):
        with self.assertRaises(TypeError):
            tc.calculate_ari_scores("invalid_object", "reference_cluster", ["pred_cluster1", "pred_cluster2_invalid"])
