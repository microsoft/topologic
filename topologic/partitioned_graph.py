# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import NamedTuple, Dict, Any
import networkx as nx


class PartitionedGraph(NamedTuple):
    """A PartitionedGraph combines a networkx graph object with
    a louvain community partition for that graph. The community can either
    be calculated or supplied to the constructor"""
    graph: nx.Graph
    partition: Dict[Any, int]
