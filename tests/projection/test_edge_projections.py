# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
from topologic import MetadataTypeRegistry, projection
import networkx as nx


headers = ["source", "target", "weight", "airspeed"]


class TestEdgeCollectionMetadataProjection(unittest.TestCase):
    def test_single_metadata(self):
        rows = [
            ["id1", "id2", "5", "too fast"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_with_collection_metadata(headers, 0, 1, 2, [])(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(5, graph["id1"]["id2"]["weight"])
        attributes = graph["id1"]["id2"]["attributes"]
        self.assertEqual(1, len(attributes))
        self.assertDictEqual({"airspeed": "too fast", "weight": "5"}, attributes[0])

    def test_multiple_metadata_same_shape(self):
        rows = [
            ["id1", "id2", "5", "too fast"],
            ["id1", "id2", "3", "reasonable and prudent"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_with_collection_metadata(headers, 0, 1, 2, [])(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(8, graph["id1"]["id2"]["weight"])
        attributes = graph["id1"]["id2"]["attributes"]
        self.assertEqual(2, len(attributes))
        self.assertDictEqual({"airspeed": "too fast", "weight": "5"}, attributes[0])
        self.assertDictEqual({"airspeed": "reasonable and prudent", "weight": "3"}, attributes[1])

    def test_multiple_metadata_different_shape(self):
        rows = [
            ["id1", "id2", "5", "too fast"],
            ["id1", "id2", "3", "NONE"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_with_collection_metadata(headers, 0, 1, 2, ["NONE"])(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(8, graph["id1"]["id2"]["weight"])
        attributes = graph["id1"]["id2"]["attributes"]
        self.assertEqual(2, len(attributes))
        self.assertDictEqual({"airspeed": "too fast", "weight": "5"}, attributes[0])
        self.assertDictEqual({"weight": "3"}, attributes[1])

    def test_multiple_edges(self):
        rows = [
            ["id1", "id2", "5", "too fast"],
            ["id1", "id2", "3", "reasonable and prudent"],
            ["id2", "id3", "1", "slow"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_with_collection_metadata(headers, 0, 1, 2, [])(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(8, graph["id1"]["id2"]["weight"])
        attributes = graph["id1"]["id2"]["attributes"]
        self.assertEqual(2, len(attributes))
        self.assertDictEqual({"airspeed": "too fast", "weight": "5"}, attributes[0])
        self.assertDictEqual({"airspeed": "reasonable and prudent", "weight": "3"}, attributes[1])

        self.assertEqual(1, graph["id2"]["id3"]["weight"])
        attributes = graph["id2"]["id3"]["attributes"]
        self.assertEqual(1, len(attributes))
        self.assertDictEqual({"airspeed": "slow", "weight": "1"}, attributes[0])

    def test_invalid_rows(self):
        rows = [
            [],
            ["id1"],
            ["id1", "id2"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_with_collection_metadata(headers, 0, 1, 2, [])(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(0, len(graph))


class TestEdgeSingleMetadataProjection(unittest.TestCase):
    def test_single_metadata(self):
        rows = [
            ["id1", "id2", "5", "too fast"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_with_single_metadata(headers, 0, 1, 2, [])(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(5, graph["id1"]["id2"]["weight"])
        attributes = graph["id1"]["id2"]["attributes"]
        self.assertEqual(1, len(attributes))
        self.assertDictEqual({"airspeed": "too fast", "weight": "5"}, attributes[0])

    def test_multiple_metadata_same_shape(self):
        rows = [
            ["id1", "id2", "5", "too fast"],
            ["id1", "id2", "3", "reasonable and prudent"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_with_single_metadata(headers, 0, 1, 2, [])(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(8, graph["id1"]["id2"]["weight"])
        attributes = graph["id1"]["id2"]["attributes"]
        self.assertEqual(1, len(attributes))
        self.assertDictEqual({"airspeed": "reasonable and prudent", "weight": "3"}, attributes[0])

    def test_multiple_metadata_different_shape(self):
        rows = [
            ["id1", "id2", "5", "too fast"],
            ["id1", "id2", "3", "NONE"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_with_single_metadata(headers, 0, 1, 2, ["NONE"])(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(8, graph["id1"]["id2"]["weight"])
        attributes = graph["id1"]["id2"]["attributes"]
        self.assertEqual(1, len(attributes))
        self.assertDictEqual({"weight": "3"}, attributes[0])

    def test_multiple_edges(self):
        rows = [
            ["id1", "id2", "5", "too fast"],
            ["id1", "id2", "3", "reasonable and prudent"],
            ["id2", "id3", "1", "slow"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_with_single_metadata(headers, 0, 1, 2, [])(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(8, graph["id1"]["id2"]["weight"])
        attributes = graph["id1"]["id2"]["attributes"]
        self.assertEqual(1, len(attributes))
        self.assertDictEqual({"airspeed": "reasonable and prudent", "weight": "3"}, attributes[0])

        self.assertEqual(1, graph["id2"]["id3"]["weight"])
        attributes = graph["id2"]["id3"]["attributes"]
        self.assertEqual(1, len(attributes))
        self.assertDictEqual({"airspeed": "slow", "weight": "1"}, attributes[0])

    def test_invalid_rows(self):
        rows = [
            [],
            ["id1"],
            ["id1", "id2"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_with_single_metadata(headers, 0, 1, 2, [])(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(0, len(graph))


class TestEdgeNoMetadataProjection(unittest.TestCase):
    def test_single_edge(self):
        rows = [
            ["id1", "id2", "5", "too fast"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_ignore_metadata(0, 1, 2)(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(5, graph["id1"]["id2"]["weight"])
        self.assertNotIn("attributes", graph["id1"]["id2"])

    def test_same_edge_different_weight(self):
        rows = [
            ["id1", "id2", "5", "too fast"],
            ["id1", "id2", "3", "reasonable and prudent"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_ignore_metadata(0, 1, 2)(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(8, graph["id1"]["id2"]["weight"])
        self.assertNotIn("attributes", graph["id1"]["id2"])

    def test_multiple_edges(self):
        rows = [
            ["id1", "id2", "5", "too fast"],
            ["id1", "id2", "3", "reasonable and prudent"],
            ["id2", "id3", "1", "slow"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_ignore_metadata(0, 1, 2)(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(8, graph["id1"]["id2"]["weight"])
        self.assertNotIn("attributes", graph["id1"]["id2"])

        self.assertEqual(1, graph["id2"]["id3"]["weight"])
        self.assertNotIn("attributes", graph["id2"]["id3"])

    def test_invalid_rows(self):
        rows = [
            [],
            ["id1"],
            ["id1", "id2"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.edge_ignore_metadata(0, 1, 2)(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(0, len(graph))
