# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
from topologic.statistics import betweenness_centrality, MakeCuts
import numpy as np
import networkx as nx


def _get_graph():
    graph = nx.florentine_families_graph()

    for s, t in graph.edges():
        graph.add_edge(s, t, weight=1)

    return graph


class TestDegreeCentralityHistogram(unittest.TestCase):

    def test_histogram_by_bin_count(self):
        graph = _get_graph()
        defined_histogram = betweenness_centrality.histogram_betweenness_centrality(graph, 10)
        self.assertEqual(10, len(defined_histogram.histogram))
        self.assertEqual(11, len(defined_histogram.bin_edges))

    def test_histogram_by_edge_bins(self):
        graph = _get_graph()
        defined_histogram = betweenness_centrality.histogram_betweenness_centrality(
            graph,
            [0.0, 0.03, 2.0]
        )
        self.assertEqual(2, len(defined_histogram.histogram))
        self.assertEqual(3, len(defined_histogram.bin_edges))
        np.testing.assert_array_equal(
            np.array([0.0, 0.03, 2.0], dtype=np.dtype(float)),
            defined_histogram.bin_edges
        )

    def test_histogram_by_auto(self):
        graph = _get_graph()
        defined_histogram = betweenness_centrality.histogram_betweenness_centrality(graph, "auto")
        self.assertEqual(6, len(defined_histogram.histogram))
        self.assertEqual(7, len(defined_histogram.bin_edges))


class TestDegreeCentralityCut(unittest.TestCase):

    def test_cut_none(self):
        graph = _get_graph()
        expected_graph_nodes = 14
        expected_graph_edges = 14

        result = betweenness_centrality.cut_vertices_by_betweenness_centrality(
            graph,
            0.4,
            MakeCuts.LARGER_THAN_EXCLUSIVE
        )
        self.assertEqual(expected_graph_edges, len(result.edges))
        self.assertEqual(expected_graph_nodes, len(result.nodes))

    def test_cut_all(self):
        graph = _get_graph()

        result = betweenness_centrality.cut_vertices_by_betweenness_centrality(
            graph,
            0.5,
            MakeCuts.SMALLER_THAN_INCLUSIVE
        )
        self.assertEqual(0, len(result.edges))
        self.assertEqual(1, len(result.nodes))

    def test_cut_less_than_inclusive(self):
        graph = _get_graph()

        result = betweenness_centrality.cut_vertices_by_betweenness_centrality(
            graph,
            0.0166525071464909,
            MakeCuts.SMALLER_THAN_INCLUSIVE
        )
        self.assertEqual(11, len(result.nodes))

    def test_cut_less_than_exclusive(self):
        graph = _get_graph()

        result = betweenness_centrality.cut_vertices_by_betweenness_centrality(
            graph,
            0.017,
            MakeCuts.SMALLER_THAN_EXCLUSIVE
        )
        self.assertEqual(11, len(result.nodes))

    def test_cut_greater_than_inclusive(self):
        graph = _get_graph()

        result = betweenness_centrality.cut_vertices_by_betweenness_centrality(
            graph,
            0.01665250714649088,
            MakeCuts.LARGER_THAN_INCLUSIVE
        )
        self.assertEqual(4, len(result.nodes))

    def test_cut_greater_than_exclusive(self):
        graph = _get_graph()

        result = betweenness_centrality.cut_vertices_by_betweenness_centrality(
            graph,
            0.017,
            MakeCuts.LARGER_THAN_EXCLUSIVE
        )
        self.assertEqual(4, len(result.nodes))
