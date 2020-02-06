# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import statistics
import unittest

import networkx as nx

import topologic as tc


class TestDensities(unittest.TestCase):
    def test_unweighted_graph_raises_type_error(self):
        graph = nx.karate_club_graph()

        with self.assertRaises(ValueError):
            tc.embedding.metric.calculate_internal_external_densities(
                graph=graph,
                partitions=dict()
            )

    def test_internal_external_densities_are_calculated(self):
        graph = nx.karate_club_graph()

        for source, target in graph.edges():
            graph.add_edge(source, target, weight=1)

        partitions = tc.louvain.best_partition(graph=graph, random_state=1)

        internal_density, external_density = tc.embedding.metric.calculate_internal_external_densities(
            graph=graph,
            partitions=partitions
        )

        self.assertEqual(statistics.mean(internal_density[0]), 1.)
        self.assertEqual(statistics.mean(external_density[0]), 1.)

    def test_external_density(self):
        graph = nx.Graph()
        graph.add_edge(0, 1, weight=1)
        graph.add_edge(0, 2, weight=2)

        membership = dict()
        membership[0] = 0
        membership[1] = 1
        membership[2] = 1

        internal_density, external_density = tc.embedding.metric.calculate_internal_external_densities(
            graph=graph,
            partitions=membership
        )

        self.assertEqual(len(internal_density), 0)
        self.assertEqual(statistics.mean(external_density[0]), .75)
        self.assertEqual(statistics.mean(external_density[1]), 1.)

    def test_internal_density(self):
        graph = nx.Graph()
        graph.add_edge(0, 1, weight=1)
        graph.add_edge(0, 2, weight=2)

        membership = dict()
        membership[0] = 0
        membership[1] = 0
        membership[2] = 0

        internal_density, external_density = tc.embedding.metric.calculate_internal_external_densities(
            graph=graph,
            partitions=membership
        )

        self.assertEqual(statistics.mean(internal_density[0]), (1/2 + 1 + 1 + 1) / 4)
        self.assertEqual(len(external_density), 0)


if __name__ == '__main__':
    unittest.main()
