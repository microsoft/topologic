# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
import numpy as np
from topologic import PartitionedGraph
from topologic.partition import modularity, modularity_components, q_score
import unittest

from tests.utils import data_file


class TestModularity(unittest.TestCase):
    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            q_score("foo")

    def test_q_score(self):
        graph = nx.Graph()
        graph.add_edge("a", "b", weight=4.0)
        graph.add_edge("b", "c", weight=3.0)
        graph.add_edge("e", "f", weight=5.0)

        partition = {'a': 0, 'b': 0, 'c': 0, 'e': 1, 'f': 1}
        part_graph = PartitionedGraph(graph, partition)
        modularity = q_score(part_graph)
        self.assertIsInstance(modularity, float)
        np.testing.assert_almost_equal(0.48611111111111105, modularity)

    def test_modularity_components(self):
        graph = nx.Graph()
        with open(data_file("large-graph.csv"), "r") as edge_list_io:
            for line in edge_list_io:
                source, target, weight = line.strip().split(",")
                previous_weight = graph.get_edge_data(source, target, {"weight": 0})["weight"]
                weight = float(weight) + previous_weight
                graph.add_edge(source, target, weight=weight)

        partitions = {}
        with open(data_file("large-graph-partitions.csv"), "r") as communities_io:
            for line in communities_io:
                vertex, community = line.strip().split(",")
                partitions[vertex] = int(community)

        components = modularity_components(graph, partitions)

        python_louvain_modularity = q_score(PartitionedGraph(graph, partitions))
        new_modularity = modularity(graph, partitions)
        (python_louvain_summed_modularity, pl_components) = modularity_from_python_louvain(graph, partitions)

        self.assertEqual(python_louvain_modularity, python_louvain_summed_modularity)
        summed_pl_components = sum(pl_components.values())
        print(f"python-louvain modularity: {python_louvain_modularity} vs: new modularity: {new_modularity} vs: Summation of python-louvain components {summed_pl_components}")
        self.assertEqual(components.keys(), pl_components.keys())
        assertion_errors = []
        attempts = 0
        for community in components.keys():
            attempts += 1
            try:
                self.assertEqual(components[community], pl_components[community], community)
            except AssertionError as e:
                assertion_errors.append(e)
        if len(assertion_errors) != 0:
            import sys
            for error in assertion_errors:
                args = error.args
                print(
                    f"community id {args[2]} modularity component {args[0]} != {args[1]}",
                    file=sys.stderr
                )
            self.fail(f"{len(assertion_errors)} tests failed of {attempts}")


def modularity_from_python_louvain(graph, partition, weight="weight"):
    inc = dict([])
    deg = dict([])
    links = graph.size(weight=weight)

    if links == 0:
        raise ValueError("A graph without link has an undefined modularity")

    for node in graph:
        com = partition[node]
        deg[com] = deg.get(com, 0.) + graph.degree(node, weight=weight)
        for neighbor, datas in graph[node].items():
            edge_weight = datas.get(weight, 1)
            if partition[neighbor] == com:
                if neighbor == node:
                    inc[com] = inc.get(com, 0.) + float(edge_weight)
                else:
                    inc[com] = inc.get(com, 0.) + float(edge_weight) / 2.

    res = 0.
    elements = {}
    for com in sorted(set(partition.values())):
        element = (inc.get(com, 0.) / links) - \
                  (deg.get(com, 0.) / (2. * links)) ** 2
        res += element
        elements[com] = element
    return res, elements