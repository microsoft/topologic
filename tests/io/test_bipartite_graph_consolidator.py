# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
from tests.utils import data_file
from topologic.io import CsvDataset, bipartite_graph_consolidator


class TestBipartiteGraphConsolidator(unittest.TestCase):

    def test_second_column_is_removed(self):
        """Ensures that the second column of the bipartite graph has been removed.  This means that
        the graph is no longer bipartite."""
        with open(data_file('actor_bipartite_graph.csv')) as csv_file:
            csv_dataset = CsvDataset(
                csv_file,
                has_headers=True,
                dialect="excel"
            )
            graph = bipartite_graph_consolidator.consolidate_bipartite(csv_dataset, 0, 1)

            self.assertIsNotNone(graph)
            z = [x for x in graph.nodes() if graph.nodes[x]["bipartite"] == 1]

            # The Target node should have disappeared
            self.assertEqual(0, len(z))

    def test_bipartite_graph_is_consolidated(self):
        """Ensures that the consolidated graph is correct."""
        with open(data_file('actor_bipartite_graph.csv')) as csv_file:
            csv_dataset = CsvDataset(
                csv_file,
                has_headers=True,
                dialect="excel"
            )
            graph = bipartite_graph_consolidator.consolidate_bipartite(csv_dataset, 0, 1)

            self.assertIsNotNone(graph)

            self.assertTrue(graph.has_edge('Tom Hanks', 'Kevin Bacon'))
            self.assertTrue(graph.has_edge('Kevin Bacon', 'Steve Martin'))
            self.assertTrue(graph.has_edge('Tom Hanks', 'Sally Field'))

            self.assertFalse(graph.has_edge('Kevin Bacon', 'Sally Field'))

            # Ensure that the Apollo 13 movie node has been consolidated
            with self.assertRaises(KeyError):
                graph.nodes['Apollo 13']


if __name__ == '__main__':
    unittest.main()
