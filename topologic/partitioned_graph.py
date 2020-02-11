# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import NamedTuple, Dict, Any
import networkx as nx


class PartitionedGraph(NamedTuple):
    """A PartitionedGraph combines a networkx graph object with
    a global community partitioning for that graph. """
    graph: nx.Graph
    community_partitions: Dict[Any, int]
