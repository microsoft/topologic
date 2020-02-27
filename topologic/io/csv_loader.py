# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import networkx as nx
import csv
from typing import Callable, List, Optional, TextIO, Union
from ..projection.edge_projections import edge_ignore_metadata, edge_with_collection_metadata, edge_with_single_metadata
from ..projection.vertex_projections import vertex_with_collection_metadata, vertex_with_single_metadata
from .datasets import CsvDataset


def from_dataset(
    csv_dataset: CsvDataset,
    projection_function_generator: Callable[[nx.Graph], Callable[[List[str]], None]],
    graph: Optional[nx.Graph] = None
) -> nx.Graph:
    """
    Load a graph from a source csv

    The most important part of this function is selecting the appropriate projection function generators.
    These functions generate yet another function generator, which in turn generates the function we will use to
    project the source CsvDataset into our graph.

    The provided projection function generators fall into 3 groups:

    - edges we don't want any  metadata for (note that there is no vertex version of this - if you don't want
      vertex metadata, don't provide a vertex_csv_dataset or function!)
    - edges or vertices we want metadata for, but the file is ordered sequentially and we only want the last
      metadata to be available in the graph
    - edges or vertices we want metadata for, and we wish to keep track of every record of metadata for the
      edge or vertex in a list of metadata dictionaries

    You can certainly provide your own projection function generators for specialized needs; just ensure they follow
    the type signature of Callable[[nx.Graph], Callable[[List[str]], None]]

    :param CsvDataset csv_dataset: the dataset to read from row by row
    :param projection_function_generator: The
        projection function generator function.  When called with a nx.Graph, it will return the
        actual projection function to be used when processing each row of data.
    :type projection_function_generator: Callable[[nx.Graph], Callable[[List[str]], None]]
    :param nx.Graph graph: The graph to populate.  If not provided a new one is created of type nx.Graph.  Note
        that from_dataset can be called repeatedly with different edge or vertex csv_dataset files to populate the graph
        more and more. If you seek to take this approach, ensure you use the same Graph object
        from the previous calls so that it is continuously populated with the updated data from new files
    :return: the graph object
    :rtype: nx.Graph
    """
    if graph is None:
        graph = nx.Graph()

    projection_function = projection_function_generator(graph)
    for row in csv_dataset.reader():
        projection_function(row)

    return graph


def from_file(
    edge_csv_file: TextIO,
    source_column_index: int,
    target_column_index: int,
    weight_column_index: Optional[int] = None,
    edge_csv_has_headers: Optional[bool] = None,
    edge_dialect: Optional[Union[csv.Dialect, str]] = None,
    edge_csv_use_headers: Optional[List[str]] = None,
    edge_metadata_behavior: str = "none",
    edge_ignored_values: Optional[List[str]] = None,
    vertex_csv_file: Optional[TextIO] = None,
    vertex_column_index: Optional[int] = None,
    vertex_csv_has_headers:  Optional[bool] = None,
    vertex_dialect: Optional[Union[csv.Dialect, str]] = None,
    vertex_csv_use_headers: Optional[List[str]] = None,
    vertex_metadata_behavior: str = "single",
    vertex_ignored_values: Optional[List[str]] = None,
    sample_size: int = 50,
    is_digraph: bool = False,
) -> nx.Graph:
    """
    This function weaves a lot of graph materialization code into a single call.

    The only required arguments are necessary for the bare minimum of creating a graph from an edge list.  However,
    it is definitely recommended to specify whether the any data files use headers and a dialect; in this way
    we can avoid relying on the csv module's sniffing ability to detect it for us.  We only use a modest number of
    records to discern the likelihood of headers existing or what to use for column separation (tabs or commas?  quotes
    or double quotes? Better to specify your own dialect than hope for the best, but the capability exists if you want
    to throw caution to the wind.

    The entire vertex metadata portion is optional; if no vertex_csv_file is specified (or it is set to None),
    no attempt will be made to enrich the graph node metadata.  The resulting vertex_metadata_types dictionary in the
    NamedTuple will be an empty dictionary and can be discarded.

    Likewise if no metadata is requested for projection by the edge projection function, the edge_metadata_types
    dictionary in the NamedTuple will be an emtpy dictionary and can be discarded.

    Lastly, it is important to note that the options for edge_metadata_behavior can only be the 3 string values
    specified in the documentation - see the docs for that parameter for details.  This is also true for the
    vertex_metadata_behavior - see the docs for that parameter as well.

    :param typing.TextIO edge_csv_file: A csv file that represents the edges of a graph.  This file must contain at
        minimum two columns: a source column and a target column. It is suggested there also exist a weight column with
        some form of numeric value (e.g. 30 or 30.0)
    :param int source_column_index: The column index the source vertex will be in.  Columns start at 0.
    :param int target_column_index: The column index the target vertex will be in.  Columns start at 0.
    :param Optional[int] weight_column_index: The column index the weight vertex will be in.  Columns start at 0.  If no
        weight_column_index is provided, we use a count of the number of VertexA to VertexB edges that exist and use
        that as the weight.
    :param Optional[bool] edge_csv_has_headers: Does the source CSV file contain headers?  If so, we will skip the
        first line.  If edge_csv_use_headers is a List[str], we will use those as headers for mapping any metadata.
        If it is None, we will use the header row as the headers, i.e. *edge_csv_use_headers* will take precedence
        over any headers in the source file, if applicable.
    :param edge_dialect: The dialect to use when parsing the source CSV file.  See
        https://docs.python.org/3/library/csv.html#csv.Dialect for more details.  If the value is None, we attempt
        to use the `csv` module's Sniffer class to detect which dialect to use based on a sample of the first 50 lines
        of the source csv file.  String values can be used if you provide the strings "excel", "excel-tab", or "unix"
    :type edge_dialect: Optional[Union[csv.Dialect, str]]
    :param Optional[List[str]] edge_csv_use_headers: Optional. Headers to use for the edge file either because the
        source file does not contain them or because you wish to override them with your own in a programmatic fashion.
    :param str edge_metadata_behavior: Dictates what extra data, aside from source, target, and weight, that we use from
        the provided edge list.

        - "none" brings along no metadata.
        - "single" iterates through the file from top to bottom; any edges between VertexA and VertexB that had
          metadata retained during edge projection will be overwritten with the newest row corresponding with
          VertexA and VertexB.  See also: Clobbering
        - "collection" iterates through the file from top to bottom; all new metadata detected between VertexA and
          VertexB is appended to the end of a list.  All metadata is kept for all edges unless pruned via normal
          graph pruning mechanisms.
    :param List[str] edge_ignored_values: Optional. A list of strings to reject retention of during projection, e.g.
        "NULL" or "N/A" or "NONE".  Any attribute value found to be one of these words will be ignored.
    :param Optional[typing.TextIO] vertex_csv_file: A csv file that represents the vertices of a graph.  This file
        should contain a column whose values correspond with the vertex ID in either the source or column field in the
        edges. If no edge exists for a Vertex, no metadata is retained.

        Note: If vertex_csv_file is None or not provided, <u>none</u> of the vertex_* arguments will be used.
    :param Optional[int] vertex_column_index: The column index the vertex id will be in.  Columns start at 0.  See note
        on vertex_csv_file.
    :param Optional[bool] vertex_csv_has_headers: Does the source CSV file contain headers?  If so, we will skip the
        first line.  If vertex_csv_use_headers is a List[str], we will use those as headers for mapping any metadata.
        If it is None, we will use the header row as the headers, i.e. *vertex_csv_use_headers* will take precedence
        over any header in the source file, if applicable.
    :param Optional[Union[csv.Dialect, str]] vertex_dialect: The dialect to use when parsing the source CSV file.  See
        https://docs.python.org/3/library/csv.html#csv.Dialect for more details.  If the value is None, we attempt
        to use the `csv` module's Sniffer class to detect which dialect to use based on a sample of the first 50 lines
        of the source csv file.  String values can be used if you provide the strings "excel", "excel-tab", or "unix"
    :param Optional[List[str]] vertex_csv_use_headers: Optional. Headers to use for the vertex file either because the
        source file does not contain them or because you wish to override them with your own in a programmatic fashion.
        See note on vertex_csv_file.
    :param str vertex_metadata_behavior: Dictates what we do with vertex metadata.  Unlike edge metadata, there is no
        need to provide a vertex_metadata_behavior if you have no vertex metadata you wish to capture.  No metadata will
        be stored for any vertex if it is not detected in the graph already; if there are no edges to or from VertexA,
        there will be no metadata retained for VertexA.

        - "simple" iterates through the file from top to bottom; any vertex that had already captured metadata through
          the vertex metadata projection process will be overwritten with the newest metadata corresponding with that
          vertex.
        - "collection" iterates through the file from top to bottom; all new metadata detected for a given vertex will
    :param List[str] vertex_ignored_values: Optional. A list of strings to reject retention of during projection, e.g.
        "NULL" be appended to a metadata list.
        or "N/A" or "NONE".  Any attribute value found to be one of these words will be ignored.
    :param int sample_size: The sample size to extract from the source CSV for use in Sniffing dialect or has_headers.
        Please note that this sample_size does NOT advance your underlying iterator, nor is there any guarantee that
        the csv Sniffer class will use every row extracted via sample_size.  Setting this above 50 may not have the
        impact you hope for due to the csv.Sniffer.has_header function - it will use at most 20 rows.
    :param bool is_digraph: If the data represents an undirected graph or a directed graph. Default is `False`.
    :return: The graph populated graph
    :rtype: nx.Graph
    """
    edge_dataset = CsvDataset(
        edge_csv_file,
        edge_csv_has_headers,
        edge_dialect,
        edge_csv_use_headers,
        sample_size
    )

    edge_projection_function: Optional[Callable[[nx.Graph], Callable[[List[str]], None]]] = None
    if edge_metadata_behavior == "none":
        edge_projection_function = edge_ignore_metadata(
            source_column_index,
            target_column_index,
            weight_column_index
        )
    elif edge_metadata_behavior == "collection":
        edge_projection_function = edge_with_collection_metadata(
            edge_dataset.headers(),
            source_column_index,
            target_column_index,
            weight_column_index,
            edge_ignored_values
        )
    elif edge_metadata_behavior == "single":
        edge_projection_function = edge_with_single_metadata(
            edge_dataset.headers(),
            source_column_index,
            target_column_index,
            weight_column_index,
            edge_ignored_values
        )
    if edge_projection_function is None:
        raise ValueError('edge_metadata_behavior must be "none", "collection", or "single"')

    graph = nx.DiGraph() if is_digraph else nx.Graph()
    graph = from_dataset(edge_dataset, edge_projection_function, graph)

    if vertex_csv_file:
        if vertex_column_index is None:
            raise ValueError("If vertex_csv_file is provided, vertex_column_index is also required.")
        vertex_dataset = CsvDataset(
            vertex_csv_file,
            vertex_csv_has_headers,
            vertex_dialect,
            vertex_csv_use_headers,
            sample_size
        )
        vertex_projection_function: Optional[
            Callable[[nx.Graph], Callable[[List[str]], None]]
        ] = None

        if vertex_metadata_behavior == "collection":
            vertex_projection_function = vertex_with_collection_metadata(
                vertex_dataset.headers(),
                vertex_column_index,
                vertex_ignored_values
            )
        elif vertex_metadata_behavior == "single":
            vertex_projection_function = vertex_with_single_metadata(
                vertex_dataset.headers(),
                vertex_column_index,
                vertex_ignored_values
            )

        if vertex_projection_function is None:
            raise ValueError('vertex_metadata_behavior must be "collection" or "single"')

        graph = from_dataset(
            vertex_dataset,
            vertex_projection_function,
            graph
        )

    return graph


def load(
    edge_file: str,
    separator: str = "excel",
    has_header: bool = True,
    source_index: int = 0,
    target_index: int = 1,
    weight_index: Optional[int] = None,
) -> nx.Graph:
    """
    Spartan, on-rails function to load an edge file.

    :param str edge_file: String path to an edge file on the filesystem
    :param str separator: Valid values are 'excel' or 'excel-tab'.
    :param bool has_header: True if the edge file has a header line, False if not
    :param int source_index: The column index for the source vertex (default 0)
    :param int target_index: The column index for the target vertex (default 1)
    :param Optional[int] weight_index: The column index for the edge weight (default None).  If
        None, or if there is no column at `weight_index`, weights per edge are defaulted to 1.
    :return:
    """
    if separator not in ["excel", "excel-tab"]:
        raise ValueError(
            "Separator must be either excel (comma separated file) or excel-tab (tab separated file). " +
            "See documentation on ETL in topologic for a more flexible loading mechanism."
        )

    with open(edge_file, "r") as edge_file_io:
        graph: nx.Graph = from_file(
            edge_file_io,
            source_column_index=source_index,
            target_column_index=target_index,
            weight_column_index=weight_index,
            edge_csv_has_headers=has_header,
            edge_dialect=separator
        )
    return graph
