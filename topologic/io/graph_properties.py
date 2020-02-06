# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.


class GraphProperties:
    def __init__(self, column_names, potential_edge_column_pairs, common_column_values, rare_column_values):
        self._column_names = column_names
        self._potential_edge_column_pairs = potential_edge_column_pairs
        self._common_column_values = common_column_values
        self._rare_column_values = rare_column_values

    def column_names(self):
        return self._column_names

    def potential_edge_column_pairs(self):
        return self._potential_edge_column_pairs

    def common_column_values(self):
        """Dictionary of column name to set of common values for that column and their counts"""
        return self._common_column_values

    def rare_column_values(self):
        """Dictionary of column name to set of rare values for that column and their counts"""
        return self._rare_column_values
