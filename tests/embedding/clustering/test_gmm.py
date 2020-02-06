# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import topologic.embedding.clustering as tc_embedding_clustering
import numpy as np
import unittest
from tests.utils import data_file


class TestGmm(unittest.TestCase):
    def test_gmm_matches_expected_cluster(self):
        matrix = np.loadtxt(data_file('gmm-input.csv'), delimiter=',', usecols=range(19))
        expected_cluster = np.loadtxt(data_file('gmm-output.txt')).astype(int)

        gmm_cluster = tc_embedding_clustering.gaussian_mixture_model(
            matrix,
            num_clusters=10,
            seed=1234
        )

        self.assertEqual(len(gmm_cluster), len(expected_cluster), 'Incorrect length of gmm_cluster')
        self.assertListEqual(list(gmm_cluster), list(expected_cluster), 'Expected clusters to be equal')

    def test_gmm_with_bic_matches_expected_cluster(self):
        matrix = np.loadtxt(data_file('gmm-input.csv'), delimiter=',', usecols=range(19))
        expected_cluster_labels = np.loadtxt(data_file('gmm-with-bic-output.txt')).astype(int)

        gmm_cluster_labels = tc_embedding_clustering.gaussian_mixture_model_with_bic(
            matrix,
            max_clusters=50,
            min_clusters=2,
            seed=1234
        )

        self.assertEqual(len(gmm_cluster_labels), len(expected_cluster_labels),
                         'Incorrect length of gmm_cluster_labels')
        self.assertListEqual(list(gmm_cluster_labels), list(expected_cluster_labels), 'Expected clusters to be equal')

    def test_gmm_with_bic_linear_matches_expected_cluster(self):
        matrix = np.loadtxt(data_file('gmm-input.csv'), delimiter=',', usecols=range(19))
        expected_cluster_labels = np.loadtxt(data_file('gmm-with-bic-output.txt')).astype(int)

        gmm_cluster_labels = tc_embedding_clustering.gaussian_mixture_model_with_bic_linear(
            matrix,
            max_clusters=50,
            min_clusters=2,
            step=1,
            seed=1234
        )

        self.assertEqual(len(gmm_cluster_labels), len(expected_cluster_labels),
                         'Incorrect length of gmm_cluster_labels')
        self.assertListEqual(list(gmm_cluster_labels), list(expected_cluster_labels), 'Expected clusters to be equal')


if __name__ == '__main__':
    unittest.main()
