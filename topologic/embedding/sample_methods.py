# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
import numpy as np
from enum import Enum


class SampleMethod(Enum):
    VERTEX_DEGREE = 0
    EDGE_WEIGHT = 1


def sample_graph_by_edge_weight(
        graph,
        weight_column='weight',
        weight_cutoff=None,
        percentage=0.1,
        nodelist=None
):
    edge_weights = nx.get_edge_attributes(graph, weight_column)
    if weight_cutoff is None:
        if percentage is not None:
            weight_cutoff = np.percentile(list(edge_weights.values()), 100 - percentage * 100)
        else:
            raise ValueError('cutoff_val or percentage cannot both be None')

    edges_to_keep = []

    for edge, weight in edge_weights.items():
        if weight > weight_cutoff:
            edges_to_keep += list(edge)

    edges_to_keep = set(edges_to_keep)

    node_idx_order = nodelist

    if node_idx_order is None:
        node_idx_order = sorted(graph.node())

    return [i for i, n in enumerate(node_idx_order) if n in edges_to_keep]


def sample_graph_by_vertex_degree(
        graph,
        degree_cutoff=None,
        percentage=0.1,
        nodelist=None
):
    degrees = dict(graph.degree())
    if degree_cutoff is None:
        if percentage is not None:
            degree_cutoff = np.percentile(list(degrees.values()), 100 - percentage * 100)
        else:
            raise ValueError('cutoff_val or percentage cannot both be None')

    nodes_to_keep = {node for node, degree in degrees.items() if degree > degree_cutoff}

    nodes_to_keep = set(nodes_to_keep)
    node_idx_order = nodelist

    if node_idx_order is None:
        node_idx_order = sorted(graph.node())

    return [i for i, n in enumerate(node_idx_order) if n in nodes_to_keep]
