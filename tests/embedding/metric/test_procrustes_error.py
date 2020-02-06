# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import numpy as np
import unittest
import networkx as nx
import topologic as tc


class TestDensities(unittest.TestCase):
    def test_procrutes_error_no_change_is_0(self):
        graph = nx.karate_club_graph()

        for s, t in graph.edges():
            graph.add_edge(s, t, weight=1)

        container = tc.embedding.laplacian_embedding(graph=graph)

        results = tc.embedding.metric.procrustes_error(
            container.embedding,
            container.embedding
        )

        np.testing.assert_almost_equal(results[0], 0)


if __name__ == '__main__':
    unittest.main()
