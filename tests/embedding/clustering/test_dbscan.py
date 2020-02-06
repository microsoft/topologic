# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import topologic.embedding.clustering as tc_embedding_clustering
import numpy as np
import unittest


class TestDbscan(unittest.TestCase):
    def test_dbscan_array_gives_expected_labels(self):
        feature_array = np.array([[1, 1, 1], [1, 1, 1], [50, 30, 20]])
        clustering_labels = tc_embedding_clustering.dbscan(feature_array, eps=1, min_samples=1)

        self.assertEqual(clustering_labels[0], 0)
        self.assertEqual(clustering_labels[1], 0)
        self.assertEqual(clustering_labels[2], 1)


if __name__ == '__main__':
    unittest.main()
