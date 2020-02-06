# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
import numpy as np
from scipy.stats import rankdata

import topologic.graph_augmentation
from topologic import UnweightedGraphError


class TestRank(unittest.TestCase):

    # EdgeDataView is a pain in the ass to try to create expected versions of for assertions.
    # conversion function to be used in a map() operation.
    def __edge_data_view_to_tuple_list__(self, edge_from_data_view):
        (source, destination, data) = edge_from_data_view
        return source, destination, data

    def test_simple_rank(self):
        starting_graph = nx.Graph()
        starting_graph.add_edge("1", "2", weight=3)
        starting_graph.add_edge("2", "3", weight=4)
        starting_graph.add_edge("4", "5", weight=2)
        updated_graph = topologic.graph_augmentation.rank_edges(starting_graph)
        edges = updated_graph.edges(data=True)
        list_edges = list(map(self.__edge_data_view_to_tuple_list__, edges))
        expected = [
            ('1', '2', {'weight': 1.0}),
            ('2', '3', {'weight': 1.5}),
            ('4', '5', {'weight': 0.5})
        ]
        self.assertEqual(list_edges, expected)

    # zeinab and others from JHU had a version that they were using prior
    # it was rewritten and we want to verify the output is the same across implementations
    # it would also be a good way to test the times of creations of each.
    def test_against_old_impl(self):
        def old_implementation(networkx_graph, weightcol='weight'):
            nedges = len(networkx_graph.edges)
            edges = np.zeros(nedges)  # declare float array
            # loop over the edges and store in an array

            if nx.is_weighted(networkx_graph, weight=weightcol) is False:
                raise IOError('Weight column not found.')

            else:
                j = 0
                for source, target, data in networkx_graph.edges(data=True):
                    edges[j] = data[weightcol]
                    j += 1

                ranked_values = rankdata(edges)
                # loop through the edges and assign the new weight:
                j = 0
                for source, target, data in networkx_graph.edges(data=True):
                    # This is meant to scale edge weights between 0 and 2
                    data[weightcol] = ranked_values[j]*2/(nedges + 1)
                    j += 1
            return networkx_graph
        starting_graph = nx.Graph()
        starting_graph.add_edge("1", "2", weight=3)
        starting_graph.add_edge("2", "3", weight=4)
        starting_graph.add_edge("4", "5", weight=2)
        updated_graph = topologic.graph_augmentation.rank_edges(starting_graph)
        edges = updated_graph.edges(data=True)
        list_edges = list(map(self.__edge_data_view_to_tuple_list__, edges))

        old_updated_graph = old_implementation(starting_graph)
        old_edges = old_updated_graph.edges(data=True)
        old_list_edges = list(map(self.__edge_data_view_to_tuple_list__, old_edges))

        self.assertEqual(list_edges, old_list_edges)

    def test_not_a_graph(self):
        with self.assertRaises(TypeError):
            topologic.graph_augmentation.rank_edges("foo")

    def test_no_weights(self):
        starting_graph = nx.Graph()
        starting_graph.add_edge("1", "2")
        starting_graph.add_edge("2", "3")
        starting_graph.add_edge("4", "5")
        with self.assertRaises(UnweightedGraphError):
            topologic.graph_augmentation.rank_edges(starting_graph)

    def test_some_weights(self):
        starting_graph = nx.Graph()
        starting_graph.add_edge("1", "2")
        starting_graph.add_edge("2", "3", weight=4)
        starting_graph.add_edge("4", "5")
        with self.assertRaises(UnweightedGraphError):
            topologic.graph_augmentation.rank_edges(starting_graph)

    def test_empty_graph(self):
        starting_graph = nx.Graph()
        with self.assertRaises(UnweightedGraphError):
            topologic.graph_augmentation.rank_edges(starting_graph)


if __name__ == '__main__':
    unittest.main()
