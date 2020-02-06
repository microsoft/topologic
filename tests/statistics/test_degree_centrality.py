# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
from ..utils import data_file
from topologic.io.csv_loader import from_file
from topologic.statistics import degree_centrality, MakeCuts
import numpy as np


def _get_graph_container():
    with open(data_file("actor_bipartite_graph.csv")) as source_iterator:
        graph_container = from_file(source_iterator, 0, 1, 0, True, "excel")
        return graph_container


class TestDegreeCentralityHistogram(unittest.TestCase):

    def test_histogram_by_bin_count(self):
        graph_container = _get_graph_container()
        defined_histogram = degree_centrality.histogram_degree_centrality(graph_container.graph, 10)
        self.assertEqual(10, len(defined_histogram.histogram))
        self.assertEqual(11, len(defined_histogram.bin_edges))

    def test_histogram_by_edge_bins(self):
        graph_container = _get_graph_container()
        defined_histogram = degree_centrality.histogram_degree_centrality(graph_container.graph, [0.0, 0.03, 2.0])
        self.assertEqual(2, len(defined_histogram.histogram))
        self.assertEqual(3, len(defined_histogram.bin_edges))
        np.testing.assert_array_equal(
            np.array([0.0, 0.03, 2.0], dtype=np.dtype(float)),
            defined_histogram.bin_edges
        )

    def test_histogram_by_auto(self):
        graph_container = _get_graph_container()
        defined_histogram = degree_centrality.histogram_degree_centrality(graph_container.graph, "auto")
        self.assertEqual(5, len(defined_histogram.histogram))
        self.assertEqual(6, len(defined_histogram.bin_edges))


class TestDegreeCentralityCut(unittest.TestCase):

    def test_cut_none(self):
        graph_container = _get_graph_container()
        graph = graph_container.graph
        expected_graph_nodes = len(graph.nodes)
        expected_graph_edges = len(graph.edges)

        result = degree_centrality.cut_vertices_by_degree_centrality(
            graph,
            0.5,
            MakeCuts.LARGER_THAN_EXCLUSIVE
        )
        self.assertEqual(expected_graph_edges, len(result.edges))
        self.assertEqual(expected_graph_nodes, len(result.nodes))

    def test_cut_all(self):
        graph_container = _get_graph_container()
        graph = graph_container.graph

        result = degree_centrality.cut_vertices_by_degree_centrality(
            graph,
            0.5,
            MakeCuts.SMALLER_THAN_INCLUSIVE
        )
        self.assertEqual(0, len(result.edges))
        self.assertEqual(0, len(result.nodes))

    def test_cut_less_than_inclusive(self):
        graph_container = _get_graph_container()
        graph = graph_container.graph

        result = degree_centrality.cut_vertices_by_degree_centrality(
            graph,
            0.01665,
            MakeCuts.SMALLER_THAN_INCLUSIVE
        )
        self.assertEqual(11, len(result.nodes))

    def test_cut_less_than_exclusive(self):
        graph_container = _get_graph_container()
        graph = graph_container.graph

        result = degree_centrality.cut_vertices_by_degree_centrality(
            graph,
            0.01666666666666668,
            MakeCuts.SMALLER_THAN_EXCLUSIVE
        )
        self.assertEqual(11, len(result.nodes))

    def test_cut_greater_than_inclusive(self):
        graph_container = _get_graph_container()
        graph = graph_container.graph

        result = degree_centrality.cut_vertices_by_degree_centrality(
            graph,
            0.139280,
            MakeCuts.LARGER_THAN_INCLUSIVE
        )
        self.assertEqual(6, len(result.nodes))

    def test_cut_greater_than_exclusive(self):
        graph_container = _get_graph_container()
        graph = graph_container.graph

        result = degree_centrality.cut_vertices_by_degree_centrality(
            graph,
            0.1392857142857144,
            MakeCuts.LARGER_THAN_EXCLUSIVE
        )
        self.assertEqual(6, len(result.nodes))
