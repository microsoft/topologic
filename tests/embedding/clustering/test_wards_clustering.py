# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import numpy as np
import topologic.embedding.clustering as tc_embedding_clustering


class TestWardsClustering(unittest.TestCase):
    def test_wards_clustering_with_array(self):
        X = np.array([[1, 2, 1], [1, 4, 1], [2, 3, 2]])
        clustering_labels = tc_embedding_clustering.wards_clustering(X,
                                                                     affinity='euclidean',
                                                                     compute_full_tree='auto',
                                                                     connectivity=None,
                                                                     memory=None,
                                                                     num_clusters=2)

        self.assertEqual(clustering_labels[0], 0)
        self.assertEqual(clustering_labels[1], 1)
        self.assertEqual(clustering_labels[2], 0)


if __name__ == '__main__':
    unittest.main()
