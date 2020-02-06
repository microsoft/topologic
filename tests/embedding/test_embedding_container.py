# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import networkx as nx
import topologic as tc
import pytest


class TestEmbeddingContainer(unittest.TestCase):
    def test_embedding_container_dictionary_contains_all_labels(self):
        networkx_graph = nx.Graph([('a', 'b', {'weight': 1.0}), ('b', 'c', {'weight': 2.0})])
        result = tc.embedding.adjacency_embedding(networkx_graph, svd_seed=1234)
        self.assertIsNotNone(result)
        (matrix, labels) = result

        d = result.to_dictionary()

        for label in labels:
            if label not in d:
                self.fail(f'Not all labels found in dictionary. Missing {label}')

    def test_oos_embedding_container_dictionary_contains_all_labels(self):
        pytest.skip('OOS is hidden')
        networkx_graph = nx.Graph([('a', 'b', {'weight': 1.0}), ('b', 'c', {'weight': 2.0})])
        result = tc.embedding.adjacency_spectral_embedding_out_of_sample(networkx_graph, svd_seed=1234)
        self.assertIsNotNone(result)
        (matrix, labels) = result

        d = result.to_dictionary()

        for label in labels:
            if label not in d:
                self.fail(f'Not all labels found in dictionary. Missing {label}')
