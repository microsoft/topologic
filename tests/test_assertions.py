# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
from topologic import assertions, InvalidGraphError


class TestConnectedComponents(unittest.TestCase):

    def test_undirected_has_multiple_connected_components(self):
        graph = nx.Graph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")
        graph.add_edge("a", "c")
        graph.add_edge("c", "a")
        assertions.assert_single_connected_components(graph)
        graph.add_edge("e", "f")
        with self.assertRaises(InvalidGraphError):
            assertions.assert_single_connected_components(graph)

    def test_directed_has_multiple_connected_components(self):
        graph = nx.DiGraph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")
        graph.add_edge("a", "c")
        graph.add_edge("c", "a")
        assertions.assert_single_connected_components(graph)
        graph.add_edge("e", "f")
        with self.assertRaises(InvalidGraphError):
            assertions.assert_single_connected_components(graph)

    def test_directed_has_multiple_weakly_connected_components_raises_error(self):
        graph = nx.DiGraph()
        graph.add_edge("a", "a")
        graph.add_edge("b", "b")
        with self.assertRaises(InvalidGraphError):
            assertions.assert_single_connected_components(graph)

    def test_has_multiple_fails_on_nongraph(self):
        with self.assertRaises(TypeError):
            assertions.assert_single_connected_components("salad")
