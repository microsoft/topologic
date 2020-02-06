# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from collections import Counter
from itertools import combinations

from topologic.io.potential_edge_column_pair import PotentialEdgeColumnPair
from topologic.io.graph_properties import GraphProperties
from topologic.io.csv_loader import CsvDataset

from typing import Dict


def find_edges(
    csv_dataset: CsvDataset,
    common_values_count: int = 20,
    rare_values_count: int = 20
):
    values: Dict[str, Counter] = {}

    headers = csv_dataset.headers()
    for header in headers:
        values[header] = Counter()

    for row in csv_dataset.reader():
        stop = min(len(headers), len(row))
        for i in range(0, stop):
            header = headers[i]
            value = row[i]
            values[header][value] += 1

    result = []

    for x in combinations(headers, 2):
        source = x[0]
        destination = x[1]

        # Make sure that we store the columns in alphabetical order when we return our result.  This will make
        # testing more deterministic
        if destination < source:
            temp = destination
            destination = source
            source = temp

        intersect = values[source] & values[destination]

        result.append(PotentialEdgeColumnPair(source, destination, len(intersect.keys())))

    result.sort(key=lambda y: (int(y.score())), reverse=True)

    common_values = {}
    rare_values = {}

    for header in headers:
        common_values[header] = values[header].most_common(common_values_count)
        rare_values[header] = values[header].most_common()[(-1 * rare_values_count):]

    return GraphProperties(
        headers,
        result,
        common_column_values=common_values,
        rare_column_values=rare_values)
