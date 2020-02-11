# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx

from typing import Callable, List, Optional
from ._common import ATTRIBUTES, metadata_to_dict


__all__ = ["vertex_with_collection_metadata", "vertex_with_single_metadata"]


def vertex_with_collection_metadata(
    headers: List[str],
    vertex_id_index: int,
    ignored_values: Optional[List[str]] = None
) -> Callable[[nx.Graph], Callable[[List[str]], None]]:
    """
    This function is an unlikely function to use; if you have vertex metadata you wish to load into the networkx.Graph
    where the vertex_id is repeated, it would be a better choice for you to compact those into a single record
    with a specific, string representable format of multiple metadata entries.  However, this function can be used
    when you aren't sure what you have.  Like the edge_with_collection_metadata projection, this function will
    create a List of dictionaries for each instance of metadata it sees for a given vertex_id.

    Note: If the vertex_id for a given row does not exist in the graph, NO METADATA WILL BE RETAINED.

    See package docstrings for more details on these currying functions.

    :param List[str] headers: Headers from a CSV row to use as metadata attribute keys
    :param int vertex_id_index: The index in the CSV data row to use as the vertex id in this graph
    :param Optional[List[str]] ignored_values: Optional.  A list of values to ignore if present in the row, such as
        "NULL" or ""
    :return: A partially applied function that partially applies yet more arguments prior to the final operation
        function
    :rtype: Callable[[networkx.Graph], Callable[[List[str]], None]]
    """
    if not ignored_values:
        ignored_values = []

    def _configure_graph(
        graph: nx.Graph
    ) -> Callable[[List[str]], None]:
        def _vertex_with_collection_metadata(row: List[str]):
            vertex_id = row[vertex_id_index]
            # don't add anything if the vertex isn't even in the graph.
            if vertex_id in graph:
                row_metadata = metadata_to_dict(
                    row,
                    [vertex_id_index],
                    ignored_values,
                    headers
                )
                if not graph.nodes[vertex_id].get(ATTRIBUTES):
                    graph.nodes[vertex_id][ATTRIBUTES] = []
                previous_metadata = graph.nodes[vertex_id][ATTRIBUTES]
                previous_metadata.append(row_metadata)
        return _vertex_with_collection_metadata
    return _configure_graph


def vertex_with_single_metadata(
        headers: List[str],
        vertex_id_index: int,
        ignored_values: List[str] = None
) -> Callable[[nx.Graph], Callable[[List[str]], None]]:
    """
    Function will project vertex metadata into the graph.  If prior data exists for the vertex_id, the later instance
    of data for the vertex_id will clobber it.

    Note: If the vertex_id for a given row does not exist in the graph, NO METADATA WILL BE RETAINED.

    See package docstrings for more details on these currying functions and on the attributes datastructure.

    :param List[str] headers: Headers from a CSV row to use as metadata attribute keys
    :param int vertex_id_index: The index in the CSV data row to use as the vertex id in this graph
    :param Optional[List[str]] ignored_values: Optional.  A list of values to ignore if present in the row, such as
        "NULL" or ""
    :return: A partially applied function that partially applies yet more arguments prior to the final operation
        function
    :rtype: Callable[[networkx.Graph], Callable[[List[str]], None]]
    """
    if not ignored_values:
        ignored_values = []

    def _configure_graph(
        graph: nx.Graph
    ) -> Callable[[List[str]], None]:
        def _vertex_with_single_metadata(row: List[str]):
            vertex_id = row[vertex_id_index]
            if vertex_id in graph:
                current_vertex_metadata = metadata_to_dict(
                    row,
                    [vertex_id_index],
                    ignored_values,
                    headers
                )
                # clobber the existing attributes
                graph.nodes[vertex_id][ATTRIBUTES] = [current_vertex_metadata]
        return _vertex_with_single_metadata
    return _configure_graph
