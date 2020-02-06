# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
from topologic.io.csv_loader import CsvDataset


def consolidate_bipartite(
    csv_dataset: CsvDataset,
    vertex_column_index: int,
    pivot_column_index: int
) -> nx.Graph:
    graph = nx.Graph()
    vertices = set()

    for row in csv_dataset.reader():

        vertices.add(row[vertex_column_index])

        graph.add_node(row[vertex_column_index], bipartite=0)
        graph.add_node(row[pivot_column_index], bipartite=1)
        graph.add_edge(row[vertex_column_index], row[pivot_column_index])

    return nx.algorithms.bipartite.projected_graph(
        graph,
        vertices,
        multigraph=True
    )
