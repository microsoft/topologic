# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from .version import get_version

# VITAL NOTE: ORDER MATTERS
from .exceptions import DialectException, InvalidGraphError, UnweightedGraphError
from .assertions import assert_is_graph, \
    assert_is_weighted, \
    assert_is_weighted_graph, \
    assert_single_connected_components

# load individual modules into the top level topologic namespace
from .metadata_types import MetadataTypeRegistry
from .louvain import best_partition, \
    induce_graph_by_communities, \
    induced_community_graph, \
    induced_graph_for_best_partition, \
    InducedCommunityGraph
from .connected_components import number_connected_components, \
    largest_connected_component, \
    connected_components_generator
from .partitioned_graph import PartitionedGraph
from .graph_augmentation import rank_edges, self_loop_augmentation
from .eigenvalue_elbows import get_elbows_from_eigenvalues
from .modularity import q_score
from .distance import cosine_distance, euclidean_distance, mahalanobis_distance

from .io.bipartite_graph_consolidator import consolidate_bipartite
from .io.edge_detector import find_edges
from .ari_scores import calculate_ari_scores, calculate_ari
from .io.potential_edge_column_pair import PotentialEdgeColumnPair
from .io.graph_properties import GraphProperties
from .scree_plot import find_elbows

from . import io
from . import projection
from . import iterators
from . import statistics
from . import embedding

__all__ = [
    'DialectException',
    'GraphProperties',
    'InducedCommunityGraph',
    'InvalidGraphError',
    'MetadataTypeRegistry',
    'PartitionedGraph',
    'PotentialEdgeColumnPair',
    'assert_is_graph',
    'assert_is_weighted',
    'assert_is_weighted_graph',
    'assert_single_connected_components',
    'best_partition',
    'calculate_ari_scores',
    'calculate_ari',
    'connected_components_generator',
    'consolidate_bipartite',
    'cosine_distance',
    'euclidean_distance',
    'find_edges',
    'find_elbows',
    'get_elbows_from_eigenvalues',
    'induce_graph_by_communities',
    'induced_community_graph',
    'induced_graph_for_best_partition',
    'largest_connected_component',
    'mahalanobis_distance',
    'number_connected_components',
    'q_score',
    'self_loop_augmentation',
    'UnweightedGraphError'
]

name = 'topologic'
# __build_version__ is defined by the VSTS build and put into version.py.  Copying the variable here so that
# we define __version__ in the standard __init__.py instead of version.py
__version__ = get_version()
