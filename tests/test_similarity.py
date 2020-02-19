# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import topologic as tc


class TestSimilarity(unittest.TestCase):
    def test_ari(self):
        a = {0: 1, 1: 1, 2: 2, 3: 3}
        b = {0: 1, 1: 2, 2: 2, 3: 3}

        score: float = tc.similarity.ari(a, b)

        # Check the distances
        self.assertAlmostEqual(-0.20, score, places=2)

    def test_ari_wrong_sizes(self):
        a = {"foo": 1, "bar": 2, "baz": 4}
        b = {"foo": 1, "baz": 4}

        self.assertRaises(ValueError, tc.similarity.ari, a, b)
