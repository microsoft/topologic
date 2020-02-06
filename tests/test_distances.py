# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import numpy as np
from topologic import cosine_distance, euclidean_distance, mahalanobis_distance


class TestDistances(unittest.TestCase):

    def test_cosine_distance_returns_0(self):
        self.assertEqual(cosine_distance(
            np.array([0, 0, 1]),
            np.array([0, 0, 1])
        ), 0)

    def test_euclidean_distance_returns_0(self):
        self.assertEqual(euclidean_distance(
            np.array([0, 0, 1]),
            np.array([0, 0, 1])
        ), 0)

    def test_mahalanobis_distance_returns_0(self):
        inverse_covariance = [[1, 0.5, 0.5], [0.5, 1, 0.5], [0.5, 0.5, 1]]

        self.assertEqual(
            mahalanobis_distance(
                np.array([1, 0, 0]),
                np.array([0, 1, 0]),
                np.array(inverse_covariance)),
            1.0
        )
