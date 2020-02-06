# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
from topologic import largest_connected_component, connected_components_generator, number_connected_components


class TestConnectedComponents(unittest.TestCase):
    def test_undirected_single_connected_component(self):
        graph = nx.Graph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")
        graph.add_edge("c", "d")
        self.assertEqual(graph.edges, largest_connected_component(graph).edges)

    def test_directed_single_connected_component(self):
        graph = nx.DiGraph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")
        graph.add_edge("c", "a")
        self.assertEqual(graph.edges, largest_connected_component(graph).edges)

    def test_undirected_largest_component(self):
        graph = nx.Graph()
        graph.add_edge("a", "b", weight=2)
        graph.add_edge("b", "c", weight=3)
        graph.add_edge("e", "f", weight=5)

        expected = nx.Graph()
        expected.add_edge("a", "b", weight=2)
        expected.add_edge("b", "c", weight=3)
        self.assertEqual(expected.edges, largest_connected_component(graph).edges)

    def test_directed_largest_component(self):
        graph = nx.DiGraph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")
        graph.add_edge("a", "c")
        graph.add_edge("c", "a")
        graph.add_edge("e", "f")

        expected = nx.DiGraph()
        expected.add_edge("a", "b")
        expected.add_edge("b", "c")
        expected.add_edge("a", "c")
        expected.add_edge("c", "a")
        self.assertEqual(expected.edges, largest_connected_component(graph, weakly=False).edges)

    def test_has_largest_fails_on_nongraph(self):
        with self.assertRaises(TypeError):
            largest_connected_component("sandwich")

    def test_undirected_connected_component_generator(self):
        graph = nx.Graph()
        graph.add_edge("a", "b")
        graph.add_edge("e", "f")

        expected_component1 = nx.Graph()
        expected_component1.add_edge("a", "b")
        expected_component2 = nx.Graph()
        expected_component2.add_edge("e", "f")

        component_graphs = list(connected_components_generator(graph))
        component_edges: list[nx.classes.graph.EdgeView] = list(map(lambda x: x.edges, component_graphs))

        self.assertEqual(2, len(component_graphs))
        first_component, second_component = (0, 1) if ("a", "b") in component_edges[0] else (1, 0)
        self.assertEqual(expected_component1.edges, component_graphs[first_component].edges)
        self.assertEqual(expected_component2.edges, component_graphs[second_component].edges)

    def test_directed_connected_component_generator(self):
        graph = nx.DiGraph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "a")
        graph.add_edge("e", "f")
        graph.add_edge("f", "e")

        expected_component1 = nx.DiGraph()
        expected_component1.add_edge("a", "b")
        expected_component1.add_edge("b", "a")
        expected_component2 = nx.DiGraph()
        expected_component2.add_edge("e", "f")
        expected_component2.add_edge("f", "e")

        component_graphs = list(connected_components_generator(graph))
        component_edges: list[nx.classes.graph.EdgeView] = list(map(lambda x: x.edges, component_graphs))

        self.assertEqual(2, len(component_graphs))
        first_component, second_component = (0, 1) if ("a", "b") in component_edges[0] else (1, 0)
        self.assertEqual(expected_component1.edges, component_graphs[first_component].edges)
        self.assertEqual(expected_component2.edges, component_graphs[second_component].edges)

    def test_undirected_number_connected_components(self):
        graph = nx.Graph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")
        graph.add_edge("e", "f")

        self.assertEqual(2, number_connected_components(graph))

    def test_directed_number_connected_components(self):
        graph = nx.DiGraph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "a")
        graph.add_edge("e", "f")
        graph.add_edge("f", "e")

        self.assertEqual(2, number_connected_components(graph))

    def test_connected_undirected_graph_lcc_equals_graph(self):
        G = nx.Graph([('a', 'b'), ('b', 'c')])
        lcc = largest_connected_component(G)
        self.assertEqual(G.adj, lcc.adj, 'LCC should be the entire graph')

    def test_undirected_graph_with_2_unequal_components_larger_is_returned(self):
        G = nx.Graph([('a', 'b'), ('b', 'c'), ('d', 'e')])
        lcc = largest_connected_component(G)
        lcc_expected = nx.Graph([('a', 'b'), ('b', 'c')])
        self.assertEqual(lcc_expected.adj, lcc.adj, 'LCC should be largest component')

    def test_connected_directed_graph_lcc_equals_graph(self):
        G = nx.DiGraph([('a', 'b'), ('b', 'c'), ('c', 'a')])
        lcc = largest_connected_component(G)
        self.assertEqual(G.adj, lcc.adj, 'LCC should be the entire graph')

    def test_directed_graph_with_2_unequal_components_larger_is_returned(self):
        G = nx.DiGraph([('a', 'b'), ('b', 'c'), ('c', 'a'), ('d', 'a')])
        lcc = largest_connected_component(G, weakly=False)
        lcc_expected = nx.DiGraph([('a', 'b'), ('b', 'c'), ('c', 'a')])
        self.assertEqual(lcc_expected.adj, lcc.adj, 'LCC should be largest component')

    def test_directed_graph_with_2_unequal_components_weakly_connected_returned(self):
        G = nx.DiGraph([('a', 'b'), ('b', 'c'), ('c', 'a'), ('d', 'a')])
        lcc = largest_connected_component(G)
        lcc_expected = nx.DiGraph([('a', 'b'), ('b', 'c'), ('c', 'a'), ('d', 'a')])
        self.assertEqual(lcc_expected.adj, lcc.adj, 'LCC should have all edges')


if __name__ == '__main__':
    unittest.main()
