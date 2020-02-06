# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest

import csv
from topologic.io import CsvDataset, from_dataset, from_file, GraphContainer, load
from topologic import projection
from ..utils import data_file


class TestCsvLoaderFromDataset(unittest.TestCase):
    def test_load(self):
        graph = load(
            edge_file=data_file('my_edges.tsv'),
            separator="excel-tab",
            has_header=True,
            source_index=3,
            target_index=4,
            weight_index=2
        )

        self.assertEqual(len(graph.edges()), 7)
        self.assertEqual(len(graph['widgets, inc.']), 4)
        # verify that edge weights were aggregated (there are two edges with weights 10 and 2 in the file)
        self.assertEqual(graph['parent automotive company']['Your Local Auto Dealer']['weight'], 12)
        self.assertEqual(max([weight for _, _, weight in graph.edges(data='weight')]), 1000)
        self.assertEqual(min([weight for _, _, weight in graph.edges(data='weight')]), 5)

    def test_edge(self):
        with open(data_file("tiny-multigraph.csv")) as edge_file:
            edge_dataset = CsvDataset(
                edge_file,
                True,
                csv.excel()
            )
            proj = projection.edge_with_collection_metadata(
                edge_dataset.headers(),
                1,
                2,
                4
            )
            graph, registry = from_dataset(edge_dataset, proj)
            self.assertEqual(7, len(graph.nodes))
            self.assertEqual(2, graph["jon"]["john"]["weight"])
            attributes = graph["jon"]["john"]["attributes"]
            self.assertDictEqual(
                {"date": "7/1/2018", "subject": "Graphs are great", "replyCount": "1"},
                attributes[0]
            )
            self.assertDictEqual(
                {"date": "7/1/2018", "subject": "Going to need to ask you to stay late tonight", "replyCount": "1"},
                attributes[1]
            )
            self.assertDictEqual(
                {"date": "7/2/2018", "subject": "RE: Graphs are great", "replyCount": "0"},
                attributes[2]
            )
            self.assertDictEqual(
                {"date": "7/2/2018", "subject": "RE: Going to need to ask you to stay late tonight",
                 "replyCount": "0"},
                attributes[3]
            )
            self.assertDictEqual(
                {"date": "7/2/2018", "subject": "No I'm not Lumberg", "replyCount": "0"},
                attributes[4]
            )
            self.assertEqual(int, registry.attribute_to_type_mapping()["replyCount"])

    def test_vertex(self):
        with open(data_file("tiny-graph-vertex.csv")) as vertex_file:
            vertex_dataset = CsvDataset(
                vertex_file,
                True,
                csv.excel()
            )
            proj = projection.vertex_with_single_metadata(
                vertex_dataset.headers(),
                0
            )
            graph, registry = from_dataset(vertex_dataset, proj)
            self.assertEqual(0, len(graph.nodes))
            self.assertEqual(0, len(registry.attribute_to_type_mapping()))

    def test_edge_then_vertex(self):
        with open(data_file("tiny-multigraph.csv")) as edge_file:
            edge_dataset = CsvDataset(
                edge_file,
                True,
                csv.excel()
            )
            proj = projection.edge_with_collection_metadata(
                edge_dataset.headers(),
                1,
                2,
                4
            )
            graph, registry = from_dataset(edge_dataset, proj)

            with open(data_file("tiny-graph-vertex.csv")) as vertex_file:
                vertex_dataset = CsvDataset(
                    vertex_file,
                    True,
                    csv.excel()
                )
                vertex_proj = projection.vertex_with_single_metadata(
                    vertex_dataset.headers(),
                    0,
                    ignored_values=["NULL"]
                )
                same_graph, new_registry = from_dataset(vertex_dataset, vertex_proj, graph)

                self.assertTrue(same_graph == graph)
                self.assertTrue(registry != new_registry)

            self.assertEqual(7, len(graph.nodes))
            self.assertEqual(2, graph["jon"]["john"]["weight"])
            attributes = graph["jon"]["john"]["attributes"]
            self.assertDictEqual(
                {"date": "7/1/2018", "subject": "Graphs are great", "replyCount": "1"},
                attributes[0]
            )
            self.assertDictEqual(
                {"date": "7/1/2018", "subject": "Going to need to ask you to stay late tonight", "replyCount": "1"},
                attributes[1]
            )
            self.assertDictEqual(
                {"date": "7/2/2018", "subject": "RE: Graphs are great", "replyCount": "0"},
                attributes[2]
            )
            self.assertDictEqual(
                {"date": "7/2/2018", "subject": "RE: Going to need to ask you to stay late tonight",
                 "replyCount": "0"},
                attributes[3]
            )
            self.assertDictEqual(
                {"date": "7/2/2018", "subject": "No I'm not Lumberg", "replyCount": "0"},
                attributes[4]
            )
            self.assertEqual(int, registry.attribute_to_type_mapping()["replyCount"])

            self.assertDictEqual({"lastName": "larson"}, graph.nodes["jon"]["attributes"][0])
            self.assertDictEqual(
                {"lastName": "redhot", "sandwichPreference": "buffalo chicken"},
                graph.nodes["frank"]["attributes"][0]
            )


class TestCsvLoaderFromFile(unittest.TestCase):
    def test_invalid_projection_values(self):
        with open(data_file("tiny-graph.csv")) as edge_file:
            with self.assertRaises(ValueError):
                from_file(
                    edge_file,
                    1,
                    2,
                    4,
                    True,
                    "excel",
                    None,
                    "salad"
                )
        with open(data_file("tiny-graph.csv")) as edge_file:
            with open(data_file("tiny-graph-vertex.csv")) as vertex_file:
                with self.assertRaises(ValueError):
                    from_file(
                        edge_file,
                        1,
                        2,
                        4,
                        True,
                        "excel",
                        vertex_csv_file=vertex_file,
                        vertex_column_index=0,
                        vertex_metadata_behavior="steak",
                        vertex_dialect="excel"
                    )

    def test_invalid_arguments_for_vertex(self):
        with open(data_file("tiny-graph.csv")) as edge_file:
            with open(data_file("tiny-graph-vertex.csv")) as vertex_file:
                with self.assertRaises(ValueError):
                    from_file(
                        edge_file,
                        1,
                        2,
                        4,
                        True,
                        "excel",
                        vertex_csv_file=vertex_file
                    )

    def test_edge_only_collection_projection(self):
        with open(data_file("tiny-multigraph.csv")) as edge_file:
            container: GraphContainer = from_file(
                edge_file,
                1,
                2,
                4,
                True,
                "excel",
                edge_metadata_behavior="collection"
            )
            graph = container.graph
            registry = container.edge_metadata_type_registry
            self.assertEqual(7, len(graph.nodes))
            self.assertEqual(2, graph["jon"]["john"]["weight"])
            attributes = graph["jon"]["john"]["attributes"]
            self.assertDictEqual(
                {"date": "7/1/2018", "subject": "Graphs are great", "replyCount": "1"},
                attributes[0]
            )
            self.assertDictEqual(
                {"date": "7/1/2018", "subject": "Going to need to ask you to stay late tonight", "replyCount": "1"},
                attributes[1]
            )
            self.assertDictEqual(
                {"date": "7/2/2018", "subject": "RE: Graphs are great", "replyCount": "0"},
                attributes[2]
            )
            self.assertDictEqual(
                {"date": "7/2/2018", "subject": "RE: Going to need to ask you to stay late tonight",
                 "replyCount": "0"},
                attributes[3]
            )
            self.assertDictEqual(
                {"date": "7/2/2018", "subject": "No I'm not Lumberg", "replyCount": "0"},
                attributes[4]
            )
            self.assertEqual(int, registry.attribute_to_type_mapping()["replyCount"])

    def test_edge_only_single_projection(self):
        with open(data_file("tiny-graph.csv")) as edge_file:
            container: GraphContainer = from_file(
                edge_file,
                1,
                2,
                4,
                True,
                "excel",
                edge_csv_use_headers=["date", "emailFrom", "emailTo", "subject", "replyCount"],
                edge_metadata_behavior="single"
            )
            graph = container.graph
            registry = container.edge_metadata_type_registry
            self.assertEqual(7, len(graph.nodes))
            self.assertEqual(1, graph["jon"]["john"]["weight"])
            attributes = graph["jon"]["john"]["attributes"]
            self.assertDictEqual(
                {"date": "7/2/2018", "subject": "RE: Graphs are great", "replyCount": "0"},
                attributes[0]
            )
            self.assertEqual(int, registry.attribute_to_type_mapping()["replyCount"])

    def test_edge_only_no_metadata_projection(self):
        with open(data_file("tiny-graph.csv")) as edge_file:
            container: GraphContainer = from_file(
                edge_file,
                1,
                2,
                4,
                True,
                "excel",
                edge_csv_use_headers=["date", "emailFrom", "emailTo", "subject", "replyCount"],
                edge_metadata_behavior="none"
            )
            graph = container.graph
            registry = container.edge_metadata_type_registry
            self.assertEqual(7, len(graph.nodes))
            self.assertEqual(1, graph["jon"]["john"]["weight"])
            self.assertNotIn("attributes", graph["jon"]["john"])
            self.assertNotIn("replyCount", registry.attribute_to_type_mapping())

    def test_vertex_single_projection(self):
        with open(data_file("tiny-multigraph.csv")) as edge_file:
            with open(data_file("tiny-graph-vertex.csv")) as vertex_file:
                container: GraphContainer = from_file(
                    edge_file,
                    1,
                    2,
                    4,
                    True,
                    "excel",
                    edge_metadata_behavior="collection",
                    vertex_csv_file=vertex_file,
                    vertex_column_index=0,
                    vertex_csv_has_headers=True,
                    vertex_dialect=csv.excel()
                )

                graph = container.graph
                edge_registry = container.edge_metadata_type_registry
                vertex_registry = container.vertex_metadata_type_registry

                self.assertTrue(edge_registry != vertex_registry)  # specifically verifying memory addresses differ

                self.assertEqual(7, len(graph.nodes))
                self.assertEqual(2, graph["jon"]["john"]["weight"])
                attributes = graph["jon"]["john"]["attributes"]
                self.assertDictEqual(
                    {"date": "7/1/2018", "subject": "Graphs are great", "replyCount": "1"},
                    attributes[0]
                )
                self.assertDictEqual(
                    {"date": "7/1/2018", "subject": "Going to need to ask you to stay late tonight",
                     "replyCount": "1"},
                    attributes[1]
                )
                self.assertDictEqual(
                    {"date": "7/2/2018", "subject": "RE: Graphs are great", "replyCount": "0"},
                    attributes[2]
                )
                self.assertDictEqual(
                    {
                        "date": "7/2/2018",
                        "subject": "RE: Going to need to ask you to stay late tonight",
                        "replyCount": "0"},
                    attributes[3]
                )
                self.assertDictEqual(
                    {"date": "7/2/2018", "subject": "No I'm not Lumberg", "replyCount": "0"},
                    attributes[4]
                )
                self.assertEqual(int, edge_registry.attribute_to_type_mapping()["replyCount"])

                self.assertDictEqual(
                    {"lastName": "larson", "sandwichPreference": "NULL"},
                    graph.nodes["jon"]["attributes"][0]
                )
                self.assertDictEqual(
                    {"lastName": "redhot", "sandwichPreference": "buffalo chicken"},
                    graph.nodes["frank"]["attributes"][0]
                )
