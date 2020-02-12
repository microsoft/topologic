# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
from tests.utils import data_file
import topologic as tc
from topologic.io import CsvDataset


class TestEdgeDetector(unittest.TestCase):

    def test_find_likely_edges_tiny_graph(self):
        with open(data_file('tiny-graph.csv')) as csvfile:
            """Find likely edges using a tiny graph.  The graph is small enough to be validated by hand."""
            result = tc.find_edges(make_graph_reader(csvfile), common_values_count=2, rare_values_count=2)

            self.assertEqual(['date', 'emailFrom', 'emailTo', 'subject', 'replyCount'], result.column_names(),
                             'Column names are not correct')

            top_rated_combo = result.potential_edge_column_pairs()[0]

            self.assertEqual('emailFrom', top_rated_combo.source(), 'Source is not correct')
            self.assertEqual('emailTo', top_rated_combo.destination(), 'Destination is not correct')

            # person1, person2, person5 are shared between emailFrom and emailTo
            self.assertEqual(3, top_rated_combo.score(), 'Score is not correct')

            self.assertEqual([('bill', 3), ('john', 2)], result.common_column_values()['emailFrom'])
            self.assertEqual([('frank', 4), ('john', 3)], result.common_column_values()['emailTo'])

            self.assertEqual([('moses', 1), ('robert downey jr.', 1)], result.rare_column_values()['emailFrom'])
            self.assertEqual([('jon', 1), ('bill', 1)], result.rare_column_values()['emailTo'])

    def test_edges_tab_separated_values(self):
        with open(data_file('tiny-graph.tsv')) as tsvfile:
            """
            Find likely edges using a tiny graph with tab-separated values.
            The graph is small enough to be validated by hand.
            """
            result = tc.find_edges(
                make_graph_reader(tsvfile, dialect='excel-tab'),
                common_values_count=2,
                rare_values_count=2)

            self.assertEqual(['date', 'emailFrom', 'emailTo', 'subject', 'replyCount'], result.column_names(),
                             'Column names are not correct')

            top_rated_combo = result.potential_edge_column_pairs()[0]

            self.assertEqual('emailFrom', top_rated_combo.source(), 'Source is not correct')
            self.assertEqual('emailTo', top_rated_combo.destination(), 'Destination is not correct')

            self.assertEqual(3, top_rated_combo.score(), 'Score is not correct')

    def test_find_likely_edges_tiny_graph_no_header(self):
        with open(data_file('tiny-graph-no-header.csv')) as csvfile:
            """Find likely edges using a tiny graph that does not contain a header row.
              The graph is small enough to be validated by hand."""
            result = tc.find_edges(
                make_graph_reader(csvfile, has_header_row=False),
                common_values_count=2,
                rare_values_count=2)
            expected_columns = list(map(lambda x: f"Attribute {x}", range(0, 5)))
            self.assertEqual(expected_columns, result.column_names(),
                             'Column names are not correct')

            top_rated_combo = result.potential_edge_column_pairs()[0]

            self.assertEqual(expected_columns[1], top_rated_combo.source(), 'Source is not correct')
            self.assertEqual(expected_columns[2], top_rated_combo.destination(), 'Destination is not correct')

            # person1, person2, person5 are shared between emailFrom and emailTo
            self.assertEqual(3, top_rated_combo.score(), 'Score is not correct')

            self.assertEqual([('bill', 3), ('john', 2)], result.common_column_values()[expected_columns[1]])
            self.assertEqual([('frank', 4), ('john', 3)], result.common_column_values()[expected_columns[2]])

            self.assertEqual([('moses', 1), ('robert downey jr.', 1)], result.rare_column_values()[expected_columns[1]])
            self.assertEqual([('jon', 1), ('bill', 1)], result.rare_column_values()[expected_columns[2]])

    def test_find_likely_edges(self):
        with open(data_file('actor_bipartite_graph.csv')) as csvfile:
            """Find likely edges using a medium sized graph.  This CSV has a header row."""
            result = tc.find_edges(make_graph_reader(csvfile))

            self.assertEqual(['Person', 'Movie', 'Role'], result.column_names(), 'Column names are not correct')

            top_rated_combo = result.potential_edge_column_pairs()[0]

            self.assertEqual('Movie', top_rated_combo.source(), 'Movie is not correct')
            self.assertEqual('Person', top_rated_combo.destination(), 'Person is not correct')

    def test_find_likely_edges_reordered_columns(self):
        """Find likely edges using a medium sized graph.  In this CSV the columns have been reversed.  This ensures
        that the code is not order-dependent and has sorts the column names for easier comparison"""
        with open(data_file('actor_bipartite_graph_reordered.csv')) as csvfile:
            result = tc.find_edges(make_graph_reader(csvfile))

            self.assertEqual(['Role', 'Movie', 'Person'], result.column_names(), 'Column names are not correct')

            top_rated_combo = result.potential_edge_column_pairs()[0]

            self.assertEqual('Movie', top_rated_combo.source(), 'Movie is not correct')
            self.assertEqual('Role', top_rated_combo.destination(), 'Role is not correct')


def make_graph_reader(
        csv_file,
        has_header_row=True,
        dialect='excel'
):
    raw_data = csv_file

    return CsvDataset(
        raw_data,
        has_headers=has_header_row,
        dialect=dialect
    )


if __name__ == '__main__':
    unittest.main()
