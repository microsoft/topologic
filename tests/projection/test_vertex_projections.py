# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
from topologic import MetadataTypeRegistry, projection
import networkx as nx


class TestVertexCollectionMetadataProjection(unittest.TestCase):

    def test_vertex_not_exist(self):
        header = ["id", "FirstName", "Ecosystem"]
        rows = [
            ["id1", "Dwayne", "jvm"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.vertex_with_collection_metadata(header, 0)(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(0, len(graph))

    def test_single_metadata(self):
        header = ["id", "FirstName", "Ecosystem"]
        rows = [
            ["id1", "Dwayne", "jvm"]
        ]
        graph = nx.Graph()
        graph.add_edge("id1", "something")  # otherwise the node won't get added
        registry = MetadataTypeRegistry()
        projection_func = projection.vertex_with_collection_metadata(header, 0)(graph, registry)
        for row in rows:
            projection_func(row)

        node_dict = graph.nodes(data=True)["id1"]
        self.assertEqual(1, len(node_dict["attributes"]))
        self.assertDictEqual({"FirstName": "Dwayne", "Ecosystem": "jvm"}, node_dict["attributes"][0])

    def test_multiple_metadata_same_shape(self):
        header = ["id", "FirstName", "Ecosystem"]
        rows = [
            ["id1", "Dwayne", "jvm"],
            ["id1", "Dwayne", "python"]
        ]
        graph = nx.Graph()
        graph.add_edge("id1", "something")  # otherwise the node won't get added
        registry = MetadataTypeRegistry()
        projection_func = projection.vertex_with_collection_metadata(header, 0)(graph, registry)
        for row in rows:
            projection_func(row)

        node_dict = graph.nodes(data=True)["id1"]
        self.assertEqual(2, len(node_dict["attributes"]))
        self.assertDictEqual({"FirstName": "Dwayne", "Ecosystem": "jvm"}, node_dict["attributes"][0])
        self.assertDictEqual({"FirstName": "Dwayne", "Ecosystem": "python"}, node_dict["attributes"][1])

    def test_multiple_metadata_different_shape(self):
        header = ["id", "FirstName", "Ecosystem", "years", "likes"]
        rows = [
            ["id1", "Dwayne", "jvm", "15", "scala,kotlin"],
            ["id1", "Dwayne", "python", "3", "NULL"]
        ]
        graph = nx.Graph()
        graph.add_edge("id1", "something")  # otherwise the node won't get added
        registry = MetadataTypeRegistry()
        # filter out NULL to change the dictionary "shape"
        projection_func = projection.vertex_with_collection_metadata(header, 0, ["NULL"])(graph, registry)
        for row in rows:
            projection_func(row)

        node_dict = graph.nodes(data=True)["id1"]
        self.assertEqual(2, len(node_dict["attributes"]))
        self.assertDictEqual(
            {"FirstName": "Dwayne", "Ecosystem": "jvm", "years": "15", "likes": "scala,kotlin"},
            node_dict["attributes"][0]
        )
        self.assertDictEqual(
            {"FirstName": "Dwayne", "Ecosystem": "python", "years": "3"},
            node_dict["attributes"][1]
        )

    def test_multiple_multivertex(self):
        header = ["id", "FirstName", "Ecosystem"]
        rows = [
            ["id1", "Dwayne", "jvm"],
            ["id1", "Dwayne", "python"],
            ["id2", "Nick", ".NET"]
        ]
        graph = nx.Graph()
        graph.add_edge("id1", "id2")
        registry = MetadataTypeRegistry()
        projection_func = projection.vertex_with_collection_metadata(header, 0)(graph, registry)
        for row in rows:
            projection_func(row)

        dwayne_node_dict = graph.nodes(data=True)["id1"]
        self.assertEqual(2, len(dwayne_node_dict["attributes"]))
        self.assertDictEqual({"FirstName": "Dwayne", "Ecosystem": "jvm"}, dwayne_node_dict["attributes"][0])
        self.assertDictEqual({"FirstName": "Dwayne", "Ecosystem": "python"}, dwayne_node_dict["attributes"][1])

        nick_node_dict = graph.nodes(data=True)["id2"]
        self.assertEqual(1, len(nick_node_dict["attributes"]))
        self.assertDictEqual({"FirstName": "Nick", "Ecosystem": ".NET"}, nick_node_dict["attributes"][0])


class TestVertexSingleMetadataProjection(unittest.TestCase):
    def test_vertex_not_exist(self):
        header = ["id", "FirstName", "Ecosystem"]
        rows = [
            ["id1", "Dwayne", "jvm"]
        ]
        graph = nx.Graph()
        registry = MetadataTypeRegistry()
        projection_func = projection.vertex_with_single_metadata(header, 0)(graph, registry)
        for row in rows:
            projection_func(row)

        self.assertEqual(0, len(graph))

    def test_single_metadata(self):
        header = ["id", "FirstName", "Ecosystem"]
        rows = [
            ["id1", "Dwayne", "jvm"]
        ]
        graph = nx.Graph()
        graph.add_edge("id1", "something")  # otherwise the node won't get added
        registry = MetadataTypeRegistry()
        projection_func = projection.vertex_with_single_metadata(header, 0)(graph, registry)
        for row in rows:
            projection_func(row)

        node_dict = graph.nodes(data=True)["id1"]
        self.assertEqual(1, len(node_dict["attributes"]))
        self.assertDictEqual({"FirstName": "Dwayne", "Ecosystem": "jvm"}, node_dict["attributes"][0])

    def test_multiple_metadata_same_shape(self):
        header = ["id", "FirstName", "Ecosystem"]
        rows = [
            ["id1", "Dwayne", "jvm"],
            ["id1", "Dwayne", "python"]
        ]
        graph = nx.Graph()
        graph.add_edge("id1", "something")  # otherwise the node won't get added
        registry = MetadataTypeRegistry()
        projection_func = projection.vertex_with_single_metadata(header, 0)(graph, registry)
        for row in rows:
            projection_func(row)

        node_dict = graph.nodes(data=True)["id1"]
        self.assertEqual(1, len(node_dict["attributes"]))
        self.assertDictEqual({"FirstName": "Dwayne", "Ecosystem": "python"}, node_dict["attributes"][0])

    def test_multiple_metadata_different_shape(self):
        header = ["id", "FirstName", "Ecosystem", "years", "likes"]
        rows = [
            ["id1", "Dwayne", "jvm", "15", "scala,kotlin"],
            ["id1", "Dwayne", "python", "3", "NULL"]
        ]
        graph = nx.Graph()
        graph.add_edge("id1", "something")  # otherwise the node won't get added
        registry = MetadataTypeRegistry()
        # filter out NULL to change the dictionary "shape"
        projection_func = projection.vertex_with_single_metadata(header, 0, ["NULL"])(graph, registry)
        for row in rows:
            projection_func(row)

        node_dict = graph.nodes(data=True)["id1"]
        self.assertEqual(1, len(node_dict["attributes"]))
        self.assertDictEqual(
            {"FirstName": "Dwayne", "Ecosystem": "python", "years": "3"},
            node_dict["attributes"][0]
        )

    def test_multiple_multivertex(self):
        header = ["id", "FirstName", "Ecosystem"]
        rows = [
            ["id1", "Dwayne", "jvm"],
            ["id1", "Dwayne", "python"],
            ["id2", "Nick", ".NET"]
        ]
        graph = nx.Graph()
        graph.add_edge("id1", "id2")
        registry = MetadataTypeRegistry()
        projection_func = projection.vertex_with_single_metadata(header, 0)(graph, registry)
        for row in rows:
            projection_func(row)

        dwayne_node_dict = graph.nodes(data=True)["id1"]
        self.assertEqual(1, len(dwayne_node_dict["attributes"]))
        self.assertDictEqual({"FirstName": "Dwayne", "Ecosystem": "python"}, dwayne_node_dict["attributes"][0])

        nick_node_dict = graph.nodes(data=True)["id2"]
        self.assertEqual(1, len(nick_node_dict["attributes"]))
        self.assertDictEqual({"FirstName": "Nick", "Ecosystem": ".NET"}, nick_node_dict["attributes"][0])
