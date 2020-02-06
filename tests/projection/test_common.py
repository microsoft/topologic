# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest

from topologic import MetadataTypeRegistry
from topologic.projection._common import metadata_to_dict


class TestCommonProjectionsMetadataToDict(unittest.TestCase):

    row = ["someid", "salad", "trader joe's", "4.99", "2018"]
    ignored_values = ["NULL"]
    ignore_columns = [0]
    headers = ["id", "food", "vendor", "price", "year"]

    def test_simple(self):
        expected = {"food": "salad", "vendor": "trader joe's", "price": "4.99", "year": "2018"}
        types_registry = MetadataTypeRegistry()
        expected_types = {"food": str, "vendor": str, "price": float, "year": int}

        returned = metadata_to_dict(
            self.row,
            self.ignore_columns,
            self.ignored_values,
            self.headers,
            types_registry
        )
        self.assertEqual(expected, returned)
        self.assertEqual(expected_types, types_registry.attribute_to_type_mapping())

    def test_empty_row_metadata_to_dict(self):
        expected = {}
        types_registry = MetadataTypeRegistry()
        expected_types = {}

        returned = metadata_to_dict(
            [],
            self.ignore_columns,
            self.ignored_values,
            self.headers,
            types_registry
        )
        self.assertEqual(expected, returned)
        self.assertEqual(expected_types, types_registry.attribute_to_type_mapping())

    def test_no_ignore_columns_metadata_to_dict(self):
        expected = {"id": "someid", "food": "salad", "vendor": "trader joe's", "price": "4.99", "year": "2018"}
        types_registry = MetadataTypeRegistry()
        expected_types = {"id": str, "food": str, "vendor": str, "price": float, "year": int}

        returned = metadata_to_dict(
            self.row,
            [],
            self.ignored_values,
            self.headers,
            types_registry
        )
        self.assertEqual(expected, returned)
        self.assertEqual(expected_types, types_registry.attribute_to_type_mapping())

    def test_all_columns_ignored_metadata_to_dict(self):
        expected = {}
        types_registry = MetadataTypeRegistry()
        expected_types = {}

        returned = metadata_to_dict(
            self.row,
            list(range(0, len(self.row))),
            self.ignored_values,
            self.headers,
            types_registry
        )
        self.assertEqual(expected, returned)
        self.assertEqual(expected_types, types_registry.attribute_to_type_mapping())

    def test_row_shorter_than_headers(self):
        expected = {"food": "salad", "vendor": "trader joe's", "price": "4.99"}
        row = self.row[:-1]
        types_registry = MetadataTypeRegistry()
        expected_types = {"food": str, "vendor": str, "price": float}

        returned = metadata_to_dict(
            row,
            self.ignore_columns,
            self.ignored_values,
            self.headers,
            types_registry
        )
        self.assertEqual(expected, returned)
        self.assertEqual(expected_types, types_registry.attribute_to_type_mapping())

    def test_headers_shorter_than_row(self):
        expected = {"food": "salad", "vendor": "trader joe's", "price": "4.99", "year": "2018"}
        row = self.row.copy()
        row.append("tax")
        types_registry = MetadataTypeRegistry()
        expected_types = {"food": str, "vendor": str, "price": float, "year": int}

        returned = metadata_to_dict(
            row,
            self.ignore_columns,
            self.ignored_values,
            self.headers,
            types_registry
        )
        self.assertEqual(expected, returned)
        self.assertEqual(expected_types, types_registry.attribute_to_type_mapping())

    def test_all_ignored_values(self):
        expected = {}
        ignored_values = self.row.copy()
        types_registry = MetadataTypeRegistry()
        expected_types = {}

        returned = metadata_to_dict(
            self.row,
            self.ignore_columns,
            ignored_values,
            self.headers,
            types_registry
        )
        self.assertEqual(expected, returned)
        self.assertEqual(expected_types, types_registry.attribute_to_type_mapping())

    def test_no_ignored_values(self):
        expected = {"food": "salad", "vendor": "trader joe's", "price": "4.99", "year": "2018"}
        types_registry = MetadataTypeRegistry()
        expected_types = {"food": str, "vendor": str, "price": float, "year": int}

        returned = metadata_to_dict(
            self.row,
            self.ignore_columns,
            [],
            self.headers,
            types_registry
        )
        self.assertEqual(expected, returned)
        self.assertEqual(expected_types, types_registry.attribute_to_type_mapping())
