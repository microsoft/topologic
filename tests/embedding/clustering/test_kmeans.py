# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import topologic.embedding.clustering as tc_embedding_clustering
import numpy as np
import unittest
from tests.utils import data_file


class TestKmeans(unittest.TestCase):
    def test_kmeans_returns_correctly_shaped_labels(self):
        matrix = np.loadtxt(data_file('gmm-input.csv'), delimiter=',', usecols=range(19))

        cluster_labels = tc_embedding_clustering.kmeans(matrix,
                                                        n_clusters=50
                                                        )

        self.assertEqual(cluster_labels.shape[0], 70, 'Incorrect shape of cluster_labels')

    def test_kmeans_with_bic_returns_correctly_shaped_labels(self):
        matrix = np.loadtxt(data_file('gmm-input.csv'), delimiter=',', usecols=range(19))

        cluster_labels = tc_embedding_clustering.kmeans_with_bic(matrix,
                                                                 max_clusters=50,
                                                                 min_clusters=2)

        self.assertEqual(cluster_labels.shape[0], 70, 'Incorrect shape of cluster_labels')

    def test_kmeans_with_bic_linear_returns_correctly_shaped_labels(self):
        matrix = np.loadtxt(data_file('gmm-input.csv'), delimiter=',', usecols=range(19))

        cluster_labels = tc_embedding_clustering.kmeans_with_bic_linear(matrix,
                                                                        max_clusters=50,
                                                                        min_clusters=2,
                                                                        step=1)

        self.assertEqual(cluster_labels.shape[0], 70, 'Incorrect shape of cluster_labels')


if __name__ == '__main__':
    unittest.main()
