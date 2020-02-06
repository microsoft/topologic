# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
import numpy as np
from topologic import statistics
from topologic.statistics import DefinedHistogram
from testfixtures import LogCapture


def _graph():
    graph = nx.Graph()
    graph.add_edge(1, 2, weight=3)
    graph.add_edge(4, 5, weight=3)
    graph.add_edge('a', 'b', weight=5)
    graph.add_edge("nick", "dwayne", weight=7)
    return graph


class TestEdgeWeights(unittest.TestCase):

    def test_histogram_from_graph(self):
        with LogCapture() as log_capture:
            graph = nx.Graph()
            graph.add_edge(1, 2, weight=3)
            graph.add_edge(4, 5, weight=3)
            graph.add_edge('a', 'b', weight=5)
            graph.add_edge("nick", "dwayne")
            expected = DefinedHistogram(histogram=np.array([2, 1]), bin_edges=np.array([3, 4, 5]))
            result = statistics.histogram_edge_weight(graph, 2)
            np.testing.assert_array_equal(expected.histogram, result.histogram)
            np.testing.assert_array_equal(expected.bin_edges, result.bin_edges)

            # check logger is logging things correctly since it is an important part of this function
            # by proxy this also checks that edges_by_weight is called
            log_capture.check(
                (
                    'topologic.statistics.edge_weights',
                    'WARNING',
                    "Graph contains 1 edges with no weight. Histogram excludes these values."
                )
            )

    def test_make_cuts_larger_than_inclusive(self):
        graph = _graph()

        updated_graph = statistics.cut_edges_by_weight(
            graph,
            5,
            statistics.MakeCuts.LARGER_THAN_INCLUSIVE,
            prune_isolates=True
        )
        self.assertEqual(2, len(updated_graph.edges))
        self.assertEqual(4, len(updated_graph.nodes))
        self.assertEqual(3, updated_graph[1][2]['weight'])
        self.assertEqual(3, updated_graph[5][4]['weight'])

    def test_make_cuts_larger_than_exclusive(self):
        graph = _graph()

        updated_graph = statistics.cut_edges_by_weight(
            graph,
            5,
            statistics.MakeCuts.LARGER_THAN_EXCLUSIVE,
            prune_isolates=True
        )
        self.assertEqual(3, len(updated_graph.edges))
        self.assertEqual(6, len(updated_graph.nodes))
        self.assertEqual(3, updated_graph[1][2]['weight'])
        self.assertEqual(3, updated_graph[5][4]['weight'])
        self.assertEqual(5, updated_graph['b']['a']['weight'])

    def test_make_cuts_smaller_than_inclusive(self):
        graph = _graph()

        updated_graph = statistics.cut_edges_by_weight(
            graph,
            5,
            statistics.MakeCuts.SMALLER_THAN_INCLUSIVE,
            prune_isolates=True
        )
        self.assertEqual(1, len(updated_graph.edges))
        self.assertEqual(2, len(updated_graph.nodes))
        self.assertEqual(7, updated_graph["nick"]["dwayne"]['weight'])

    def test_make_cuts_smaller_than_exclusive(self):
        graph = _graph()

        updated_graph = statistics.cut_edges_by_weight(
            graph,
            5,
            statistics.MakeCuts.SMALLER_THAN_EXCLUSIVE,
            prune_isolates=True
        )
        self.assertEqual(2, len(updated_graph.edges))
        self.assertEqual(4, len(updated_graph.nodes))
        self.assertEqual(5, updated_graph["a"]["b"]['weight'])
        self.assertEqual(7, updated_graph["nick"]["dwayne"]['weight'])

    def test_make_cuts_smaller_than_exclusive_no_prune_isolates(self):
        graph = _graph()

        updated_graph = statistics.cut_edges_by_weight(
            graph,
            5,
            statistics.MakeCuts.SMALLER_THAN_EXCLUSIVE
        )
        self.assertEqual(2, len(updated_graph.edges))
        self.assertEqual(8, len(updated_graph.nodes))
        self.assertEqual(5, updated_graph["a"]["b"]['weight'])
        self.assertEqual(7, updated_graph["nick"]["dwayne"]['weight'])
        self.assertIn(1, updated_graph)
        self.assertIn(2, updated_graph)
        self.assertIn(4, updated_graph)
        self.assertIn(5, updated_graph)

    def test_cut_all(self):
        graph = _graph()

        updated_graph = statistics.cut_edges_by_weight(
            graph,
            7,
            statistics.MakeCuts.SMALLER_THAN_INCLUSIVE,
            prune_isolates=True
        )
        self.assertEqual(0, len(updated_graph.edges))
        self.assertEqual(0, len(updated_graph.nodes))

    def test_cut_none(self):
        graph = _graph()

        updated_graph = statistics.cut_edges_by_weight(
            graph,
            7,
            statistics.MakeCuts.LARGER_THAN_EXCLUSIVE,
            prune_isolates=True
        )
        self.assertEqual(4, len(updated_graph.edges))
        self.assertEqual(8, len(updated_graph.nodes))

    def test_broken_make_cuts(self):
        graph = _graph()
        with self.assertRaises(ValueError):
            statistics.cut_edges_by_weight(
                graph,
                5,
                None
            )
