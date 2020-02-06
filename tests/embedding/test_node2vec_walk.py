# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
import topologic as tc
import itertools


class TestNode2VecRandomWalkIterator(unittest.TestCase):
    def setUp(self):
        # nodes for two connected components
        self.component1_nodes = ["c1n1", "c1n2", "c1n3", "c1n4"]
        self.component2_nodes = ["c2n1", "c2n2", "c2n3"]

        # create a graph and add the first component
        g = nx.Graph()
        g.add_edge(self.component1_nodes[0], self.component1_nodes[1], weight=1.0)
        g.add_edge(self.component1_nodes[1], self.component1_nodes[2], weight=2.0)
        g.add_edge(self.component1_nodes[2], self.component1_nodes[3], weight=1.5)
        g.add_edge(self.component1_nodes[3], self.component1_nodes[0], weight=2.9)

        # add the second component
        g.add_edge(self.component2_nodes[0], self.component2_nodes[1], weight=1.3)
        g.add_edge(self.component2_nodes[1], self.component2_nodes[2], weight=3.2)
        g.add_edge(self.component2_nodes[2], self.component2_nodes[0], weight=2.5)

        self.two_component_graph = g

    def test_walk_starts_at_specified_node(self):
        walk_iter = tc.embedding.node2vec_random_walk_iterator(
                self.two_component_graph, node=self.component1_nodes[0], p=1.0, q=1.0, weight_attr=None)
        self.assertEqual(self.component1_nodes[0], next(walk_iter))

    def test_walk_does_not_leave_connected_component(self):
        walk_iter = tc.embedding.node2vec_random_walk_iterator(
                self.two_component_graph, node=self.component1_nodes[0], p=1.0, q=1.0, weight_attr=None)
        for node in itertools.islice(walk_iter, 10):
            self.assertIn(node, self.two_component_graph)
            self.assertNotIn(node, self.component2_nodes)

    def test_walk_with_weight_attribute(self):
        walk_iter = tc.embedding.node2vec_random_walk_iterator(
                self.two_component_graph, node=self.component2_nodes[1], p=1.0, q=1.0, weight_attr='weight')
        for node in itertools.islice(walk_iter, 10):
            self.assertIn(node, self.two_component_graph)
            self.assertNotIn(node, self.component1_nodes)

    def test_walk_visits_all_nodes_in_component(self):
        walk_iter = tc.embedding.node2vec_random_walk_iterator(
                self.two_component_graph, node=self.component2_nodes[1], p=1.0, q=1.0, weight_attr=None)
        visited_nodes = set(itertools.islice(walk_iter, 50))
        self.assertEqual(visited_nodes, set(self.component2_nodes))

    def test_keyerror_raised_when_node_is_not_in_graph(self):
        with self.assertRaises(KeyError):
            walk_iter = tc.embedding.node2vec_random_walk_iterator(
                self.two_component_graph,
                node='missing',
                p=1.0,
                q=1.0
            )
            next(walk_iter)
