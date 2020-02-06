# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
from topologic.iterators import Sampler


class TestSampler(unittest.TestCase):

    def test_small_list(self):
        input_data = range(0, 1000)
        result = Sampler.sample(input_data, 10)

        self.assertIsNotNone(result)
        self.assertEqual(10, len(list(result)))

    def test_medium_list(self):
        input_data = range(0, 100000)
        result = Sampler.sample(input_data, 1000)

        self.assertIsNotNone(result)
        self.assertEqual(1000, len(list(result)))

    def test_large_list(self):
        input_data = range(0, 10000000)
        result = Sampler.sample(input_data, 100000)

        self.assertIsNotNone(result)
        self.assertEqual(100000, len(list(result)))


if __name__ == '__main__':
    unittest.main()
