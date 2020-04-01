# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from .version.version import name, version as __version__

# VITAL NOTE: ORDER MATTERS
from .exceptions import DialectException, InvalidGraphError, UnweightedGraphError

# load individual modules into the top level topologic namespace
from .connected_components import number_connected_components, \
    largest_connected_component, \
    connected_components_generator
from .partitioned_graph import PartitionedGraph
from .graph_augmentation import rank_edges, diagonal_augmentation

from . import similarity
from . import io
from . import projection
from . import statistics
from . import embedding
from . import partition

__all__ = [
    'connected_components_generator',
    'DialectException',
    'InvalidGraphError',
    'largest_connected_component',
    'number_connected_components',
    'PartitionedGraph',
    'diagonal_augmentation',
    'UnweightedGraphError'
]
