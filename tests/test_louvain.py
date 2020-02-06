# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
from topologic import best_partition, induced_graph_for_best_partition, induced_community_graph
from community import best_partition as community_best_partition


class TestBestPartition(unittest.TestCase):
    maxDiff = None

    def test_best_partition(self):
        G = nx.erdos_renyi_graph(100, 0.01)
        ex_best_partition = best_partition(G, random_state=0)
        comm_best_partition = community_best_partition(G, random_state=0)

        self.assertEqual(ex_best_partition, comm_best_partition)

    def test_induced_graph_for_best_partition_default_args(self):
        G = nx.erdos_renyi_graph(100, 0.01)
        induced = induced_graph_for_best_partition(G)
        self.assertGreater(len(induced), 0)

    def test_induced_community_graph(self):
        G = nx.erdos_renyi_graph(100, 0.01)
        induced = induced_community_graph(G)
        self.assertEqual(len(induced.graph.nodes()), len(set(induced.communities.values())))
