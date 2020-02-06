# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
import numpy as np
from topologic import InvalidGraphError, q_score, PartitionedGraph
import unittest


class TestModularity(unittest.TestCase):
    def test_wrong_type(self):
        with self.assertRaises(InvalidGraphError):
            q_score("foo")

    def test_q_score(self):
        graph = nx.Graph()
        graph.add_edge("a", "b", weight=4.0)
        graph.add_edge("b", "c", weight=3.0)
        graph.add_edge("e", "f", weight=5.0)
        # manually specified partition just in case louvain picks some other partition scheme, which seems incredibly
        # unlikely, but I hate when builds break due to incredible unlikeliness
        partition = {'a': 0, 'b': 0, 'c': 0, 'e': 1, 'f': 1}
        part_graph = PartitionedGraph(graph, partition)
        modularity = q_score(part_graph)
        self.assertIsInstance(modularity, float)
        np.testing.assert_almost_equal(0.48611111111111105, modularity)
