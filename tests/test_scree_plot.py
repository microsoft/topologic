# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
from topologic.scree_plot import find_elbows
import numpy as np


class TestScreePlotElbowFinder(unittest.TestCase):

    def test_small_list(self):
        input_data = [2, 3, 4, 5, 6, 7, 8, 9]
        result: np.array = find_elbows(input_data, elbow_count=1, threshold=0)

        self.assertIsNotNone(result)
        self.assertEqual(1, result.size)
        self.assertEqual(4, result[0])

    def test_list_of_1(self):
        input_data = [2]
        result: np.array = find_elbows(input_data, elbow_count=1, threshold=0)

        self.assertIsNotNone(result)
        self.assertEqual(1, result.size)

    def test_list_of_2(self):
        input_data = [2, 10]
        result: np.array = find_elbows(input_data, elbow_count=1, threshold=0)

        self.assertIsNotNone(result)
        self.assertEqual(1, result.size)
        self.assertEqual(1, result[0])


if __name__ == '__main__':
    unittest.main()
