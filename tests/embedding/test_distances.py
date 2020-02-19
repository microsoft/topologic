# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import numpy as np
from topologic.embedding import distance


class TestDistances(unittest.TestCase):

    first_vector = np.array([1.0, 1.0, 1.0, 1.0])
    second_vector = np.array([-10.0, -10.0, -10.0, -10.0])

    def test_cosine_distance_returns_0(self):
        self.assertEqual(distance.cosine(
            np.array([0, 0, 1]),
            np.array([0, 0, 1])
        ), 0)

    def test_euclidean_distance_returns_0(self):
        self.assertEqual(distance.euclidean(
            np.array([0, 0, 1]),
            np.array([0, 0, 1])
        ), 0)

    def test_mahalanobis_distance_returns_1(self):
        inverse_covariance = [[1, 0.5, 0.5], [0.5, 1, 0.5], [0.5, 0.5, 1]]
        mahalanobis = distance.mahalanobis(inverse_covariance)
        self.assertEqual(
            mahalanobis(
                np.array([1, 0, 0]),
                np.array([0, 1, 0])
            ),
            1.0
        )

    def test_vector_distance_cosine(self):
        expected = 2.0
        actual_str = distance.vector_distance(self.first_vector, self.second_vector, "cosine")
        actual_func = distance.vector_distance(self.first_vector, self.second_vector, distance.cosine)
        self.assertEqual(expected, actual_str)
        self.assertEqual(expected, actual_func)

    def test_vector_distance_euclidean(self):
        expected = 22.0
        actual_str = distance.vector_distance(self.first_vector, self.second_vector, "euclidean")
        actual_func = distance.vector_distance(self.first_vector, self.second_vector, distance.euclidean)
        self.assertEqual(expected, actual_str)
        self.assertEqual(expected, actual_func)

    def test_vector_distance_str_notexist(self):
        self.assertRaises(
            ValueError,
            distance.vector_distance,
            self.first_vector,
            self.second_vector,
            method="sandwiches"
        )

    def test_embedding_distance_for_cosine(self):
        expected = [0.0, 22.0]
        embedding = np.array([[1.0, 1.0, 1.0, 1.0], [-10, -10, -10, -10]])
        actual = distance.embedding_distances_from(self.first_vector, embedding, distance.euclidean)
        np.testing.assert_array_equal(expected, actual)

    def test_embedding_distance_for_arbitrary_distance_function(self):
        def always_10(first_vector: np.ndarray, second_vector: np.ndarray) -> float:
            return 10.0

        expected = [10.0, 10.0]
        embedding = np.array([[1.0, 1.0, 1.0, 1.0], [-10, -10, -10, -10]])
        actual_1 = distance.embedding_distances_from(self.first_vector, embedding, always_10)
        actual_2 = distance.embedding_distances_from(self.second_vector, embedding, always_10)
        np.testing.assert_array_equal(expected, actual_1)
        np.testing.assert_array_equal(expected, actual_2)
