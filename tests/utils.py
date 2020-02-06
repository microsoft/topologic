# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os
import re
import networkx as nx


def data_file(filename):
    return os.path.join(os.path.dirname(__file__), 'test_data', filename)


def get_graph_from_file(file_name):
    counter = 0
    labels = {}  # represents the ids of each vertex in the graph
    graph = nx.Graph()

    with open(data_file(file_name), 'r') as f:
        lines = f.readlines()
        for line in lines:
            tokens = re.split(r'\t+', line)

            if tokens[0] not in labels:
                labels[tokens[0]] = tokens[0]
                counter += 1
            if tokens[1] not in labels:
                labels[tokens[1]] = tokens[1]
                counter += 1

            weight_val = str(tokens[2]).split()[1]
            weight = weight_val[0:(len(weight_val) - 1)]

            graph.add_edge(labels[tokens[0]], labels[tokens[1]], weight=float(weight))

    return graph
