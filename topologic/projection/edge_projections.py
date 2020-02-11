# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
from typing import Any, Callable, List, Optional
from ._common import ATTRIBUTES, metadata_to_dict


__all__ = ["edge_with_collection_metadata", "edge_with_single_metadata", "edge_ignore_metadata"]


WEIGHT_ATTRIBUTE = "weight"
NUMERIC_TYPES = [int, float]


def _cast_weight(weight: Any):
    # attempts to turn a weight value into a number if it is not already a number.
    # weight always has to be a number - though a field could be invalid and then this will explode (by design)
    if type(weight) in NUMERIC_TYPES:
        return weight
    try:
        return int(weight)
    except ValueError:
        return float(weight)


def _length_check(
    row: List[str],
    source_index: int,
    target_index: int,
    weight_index: Optional[int] = None
) -> bool:
    functional_weight_index = weight_index if weight_index else -1
    return len(row) > max(source_index, target_index, functional_weight_index)


def _add_edge(
    graph: nx.Graph,
    source: str,
    target: str,
    row_weight: str
):
    # add edge does the same thing for all edge projections; it adds the edge, checks to see if it had a previous weight
    # defaulting to 0 if it did not, then aggregating the new weight value with the old weight value, then updating the
    # edge weight value on the graph.
    graph.add_edge(source, target)
    previous_weight = graph[source][target].get(WEIGHT_ATTRIBUTE, 0)
    aggregate_weight = row_weight + previous_weight
    graph[source][target][WEIGHT_ATTRIBUTE] = aggregate_weight


def edge_with_collection_metadata(
    headers: List[str],
    source_index: int,
    target_index: int,
    weight_index: Optional[int] = None,
    ignored_values: Optional[List[str]] = None
) -> Callable[[nx.Graph], Callable[[List[str]], None]]:
    """
    Some graph algorithms have undefined behavior over multigraphs.  To skirt this limitation, we allow the data to
    represent a multigraph, though we collapse it into a non-multigraph.  We do this by aggregating the weights,
    and in this case we take any extra metadata in the edge source and project it, along with headers, into an
    attribute dictionary.  This dictionary is then added to a List of any previous attribute dictionaries for the same
    source and target, so as to not clobber any metadata.

    See package docstrings for more details on these currying functions.

    :param List[str] headers: Headers from a CSV row to use as metadata attribute keys
    :param int source_index: The index in the CSV data row to use as the source node in this edge
    :param int target_index: The index in the CSV data row to use as the target node in this edge
    :param Optional[int] weight_index: Optional.  The index in the CSV data row to use as the weight of the edge.
        If no weight is provided, all records of an edge are presumed to have a weight of 1.  Duplicates of an edge
        will have their weights (or inferred weight) aggregated into a single value.
    :param Optional[List[str]] ignored_values: Optional.  A list of values to ignore if present in the row, such as
        "NULL" or ""
    :return: A partially applied function that partially applies yet more arguments prior to the final operation
        function
    :rtype: Callable[[networkx.Graph], Callable[[List[str]], None]]
    """
    if not ignored_values:
        ignored_values = []
    ignore_list = [source_index, target_index]

    def _configure_graph(
        graph: nx.Graph
    ) -> Callable[[List[str]], None]:
        def _edge_with_collection_metadata(row: List[str]):
            if _length_check(row, source_index, target_index, weight_index):
                source = row[source_index]
                target = row[target_index]
                row_weight = _cast_weight(row[weight_index]) if weight_index else 1
                _add_edge(
                    graph,
                    source,
                    target,
                    row_weight
                )
                row_metadata = metadata_to_dict(row, ignore_list, ignored_values, headers)
                if not graph[source][target].get(ATTRIBUTES):
                    graph[source][target][ATTRIBUTES] = []
                graph[source][target][ATTRIBUTES].append(row_metadata)
        return _edge_with_collection_metadata
    return _configure_graph


def edge_with_single_metadata(
    headers: List[str],
    source_index: int,
    target_index: int,
    weight_index: Optional[int] = None,
    ignored_values: Optional[List[str]] = None
) -> Callable[[nx.Graph], Callable[[List[str]], None]]:
    """
    Will load edges into graph even if they are a multigraph.  However, aside from weight, the multigraph attributes are
    ignored and the last record to be processed for that source and target will have its metadata retained and all prior
    metadata dropped.

    See package docstrings for more details on these currying functions.

    :param List[str] headers: Headers from a CSV row to use as metadata attribute keys
    :param int source_index: The index in the CSV data row to use as the source node in this edge
    :param int target_index: The index in the CSV data row to use as the target node in this edge
    :param Optional[int[ weight_index: Optional.  The index in the CSV data row to use as the weight of the edge.
        If no weight is provided, all records of an edge are presumed to have a weight of 1.  Duplicates of an edge
        will have their weights (or inferred weight) aggregated into a single value.
    :param Optional[List[str]] ignored_values: Optional.  A list of values to ignore if present in the row, such as
        "NULL" or ""
    :return: A partially applied function that partially applies yet more arguments prior to the final operation
        function
    :rtype: Callable[[networkx.Graph], Callable[[List[str]], None]]
    """

    if not ignored_values:
        ignored_values = []
    ignore_list = [source_index, target_index]

    def _configure_graph(
        graph: nx.Graph
    ) -> Callable[[List[str]], None]:

        def _edge_with_single_metadata(row: List[str]):
            if _length_check(row, source_index, target_index, weight_index):
                source = row[source_index]
                target = row[target_index]
                row_weight = _cast_weight(row[weight_index]) if weight_index else 1
                _add_edge(
                    graph,
                    source,
                    target,
                    row_weight
                )
                row_metadata = [metadata_to_dict(row, ignore_list, ignored_values, headers)]
                graph[source][target][ATTRIBUTES] = row_metadata
        return _edge_with_single_metadata
    return _configure_graph


def edge_ignore_metadata(
    source_index: int,
    target_index: int,
    weight_index: Optional[int] = None
) -> Callable[[nx.Graph], Callable[[List[str]], None]]:
    """
    Drops all metadata.  Creates graph solely based on source, target, and optional weight.

    See package docstrings for more details on these currying functions.

    :param int source_index: The index in the CSV data row to use as the source node in this edge
    :param int target_index: The index in the CSV data row to use as the target node in this edge
    :param Optional[int] weight_index: Optional.  The index in the CSV data row to use as the weight of the edge.
        If no weight is provided, all records of an edge are presumed to have a weight of 1.  Duplicates of an edge
        will have their weights (or inferred weight) aggregated into a single value.
    :return: A partially applied function that partially applies yet more arguments prior to the final operation
        function
    :rtype: Callable[[networkx.Graph], Callable[[List[str]], None]]
    """
    def _configure_graph(
        graph: nx.Graph
    ) -> Callable[[List[str]], None]:

        def _edge_ignore_metadata(row: List[str]):
            if _length_check(row, source_index, target_index, weight_index):
                source = row[source_index]
                target = row[target_index]
                row_weight = _cast_weight(row[weight_index]) if weight_index else 1
                _add_edge(
                    graph,
                    source,
                    target,
                    row_weight
                )
        return _edge_ignore_metadata
    return _configure_graph
