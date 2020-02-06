# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
from topologic import self_loop_augmentation


class TestDiagonalAugmentation(unittest.TestCase):
    def test_diag_aug_for_a_non_graph_raises_exception(self):
        with self.assertRaises(TypeError) as raised:
            self_loop_augmentation('not a graph')

        self.assertTrue('must be a networkx.Graph' in str(raised.exception))

    def test_diag_aug_for_2_nodes_self_loops(self):
        graph = nx.Graph([('a', 'b'), ('b', 'c'), ('a', 'a'), ('b', 'b'), ('c', 'c')])
        expected_set = {('a', 'a', 0.5), ('a', 'b', None), ('b', 'b', 1.0), ('b', 'c', None), ('c', 'c', 0.5)}

        augmented = self_loop_augmentation(graph)
        ranked_edge_set = set(augmented.edges(data='weight'))

        self.assertEqual(augmented, graph)
        self.assertEqual(expected_set, ranked_edge_set)

    def test_diag_aug_for_2_nodes_no_self_loops(self):
        graph = nx.Graph([('a', 'b'), ('b', 'c')])
        expected_set = {('a', 'a', 0.5), ('a', 'b', None), ('b', 'b', 1.0), ('b', 'c', None), ('c', 'c', 0.5)}

        augmented = self_loop_augmentation(graph)
        ranked_edge_set = set(augmented.edges(data='weight'))

        self.assertEqual(augmented, graph)
        self.assertEqual(expected_set, ranked_edge_set)
