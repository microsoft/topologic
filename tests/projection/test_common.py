# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
from topologic.projection._common import metadata_to_dict


class TestCommonProjectionsMetadataToDict(unittest.TestCase):

    row = ["someid", "salad", "trader joe's", "4.99", "2018"]
    ignored_values = ["NULL"]
    ignore_columns = [0]
    headers = ["id", "food", "vendor", "price", "year"]

    def test_simple(self):
        expected = {"food": "salad", "vendor": "trader joe's", "price": "4.99", "year": "2018"}

        returned = metadata_to_dict(
            self.row,
            self.ignore_columns,
            self.ignored_values,
            self.headers
        )
        self.assertEqual(expected, returned)

    def test_empty_row_metadata_to_dict(self):
        expected = {}

        returned = metadata_to_dict(
            [],
            self.ignore_columns,
            self.ignored_values,
            self.headers
        )
        self.assertEqual(expected, returned)

    def test_no_ignore_columns_metadata_to_dict(self):
        expected = {"id": "someid", "food": "salad", "vendor": "trader joe's", "price": "4.99", "year": "2018"}

        returned = metadata_to_dict(
            self.row,
            [],
            self.ignored_values,
            self.headers
        )
        self.assertEqual(expected, returned)

    def test_all_columns_ignored_metadata_to_dict(self):
        expected = {}

        returned = metadata_to_dict(
            self.row,
            list(range(0, len(self.row))),
            self.ignored_values,
            self.headers
        )
        self.assertEqual(expected, returned)

    def test_row_shorter_than_headers(self):
        expected = {"food": "salad", "vendor": "trader joe's", "price": "4.99"}
        row = self.row[:-1]

        returned = metadata_to_dict(
            row,
            self.ignore_columns,
            self.ignored_values,
            self.headers
        )
        self.assertEqual(expected, returned)

    def test_headers_shorter_than_row(self):
        expected = {"food": "salad", "vendor": "trader joe's", "price": "4.99", "year": "2018"}
        row = self.row.copy()
        row.append("tax")

        returned = metadata_to_dict(
            row,
            self.ignore_columns,
            self.ignored_values,
            self.headers
        )
        self.assertEqual(expected, returned)

    def test_all_ignored_values(self):
        expected = {}
        ignored_values = self.row.copy()

        returned = metadata_to_dict(
            self.row,
            self.ignore_columns,
            ignored_values,
            self.headers
        )
        self.assertEqual(expected, returned)

    def test_no_ignored_values(self):
        expected = {"food": "salad", "vendor": "trader joe's", "price": "4.99", "year": "2018"}

        returned = metadata_to_dict(
            self.row,
            self.ignore_columns,
            [],
            self.headers
        )
        self.assertEqual(expected, returned)
