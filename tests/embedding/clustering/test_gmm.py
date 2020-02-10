# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import topologic.embedding.clustering as tc_embedding_clustering
import numpy as np
import unittest
from tests.utils import data_file


class TestGmm(unittest.TestCase):
    def test_gmm_matches_expected_cluster(self):
        matrix = np.loadtxt(data_file('gmm-input.csv'), delimiter=',', usecols=range(19))
        expected_cluster = [0, 0, 0, 2, 0, 0, 0, 0, 2, 6, 0, 2, 2, 7, 1, 1, 0, 0, 0, 7, 9, 0, 0, 0, 2, 0, 6, 0, 0, 5, 0,
                            0, 0, 4, 6, 6, 1, 2, 5, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 3, 0, 0]

        gmm_cluster = tc_embedding_clustering.gaussian_mixture_model(
            matrix,
            num_clusters=10,
            seed=1234
        )

        self.assertEqual(len(gmm_cluster), len(expected_cluster), 'Incorrect length of gmm_cluster')
        self.assertListEqual(list(gmm_cluster), list(expected_cluster), 'Expected clusters to be equal')


if __name__ == '__main__':
    unittest.main()
