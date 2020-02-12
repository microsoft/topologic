# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from .version.version import name, version as __version__

# VITAL NOTE: ORDER MATTERS
from .exceptions import DialectException, InvalidGraphError, UnweightedGraphError
from .assertions import assert_is_graph, \
    assert_is_weighted, \
    assert_is_weighted_graph, \
    assert_single_connected_components

# load individual modules into the top level topologic namespace
from .connected_components import number_connected_components, \
    largest_connected_component, \
    connected_components_generator
from .partitioned_graph import PartitionedGraph
from .graph_augmentation import rank_edges, self_loop_augmentation
from .eigenvalue_elbows import get_elbows_from_eigenvalues
from .distance import cosine_distance, euclidean_distance, mahalanobis_distance

from .io.bipartite_graph_consolidator import consolidate_bipartite
from .io.edge_detector import find_edges
from .ari_scores import calculate_ari_scores, calculate_ari
from .io.potential_edge_column_pair import PotentialEdgeColumnPair
from .io.graph_properties import GraphProperties
from .scree_plot import find_elbows

from . import io
from . import projection
from . import statistics
from . import embedding
from . import partition

__all__ = [
    'DialectException',
    'GraphProperties',
    'InvalidGraphError',
    'PartitionedGraph',
    'PotentialEdgeColumnPair',
    'assert_is_graph',
    'assert_is_weighted',
    'assert_is_weighted_graph',
    'assert_single_connected_components',
    'calculate_ari_scores',
    'calculate_ari',
    'connected_components_generator',
    'consolidate_bipartite',
    'cosine_distance',
    'euclidean_distance',
    'find_edges',
    'find_elbows',
    'get_elbows_from_eigenvalues',
    'largest_connected_component',
    'mahalanobis_distance',
    'number_connected_components',
    'self_loop_augmentation',
    'UnweightedGraphError'
]
