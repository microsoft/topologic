# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import csv as csv_import
import itertools
import unittest

from topologic.io import CsvDataset
from ..utils import data_file


class TestGetFirstLines(unittest.TestCase):

    csv_data_with_headers = data_file("tiny-graph.csv")
    csv_data_without_headers = data_file("tiny-graph-no-header.csv")
    tsv_data_with_headers = data_file("tiny-graph.tsv")

    expected_file_headers = ["date", "emailFrom", "emailTo", "subject", "replyCount"]

    def test_csv_with_headers_sniff_dialect_sniff_headers(self):
        with open(self.csv_data_with_headers) as source_iterator:
            csv = CsvDataset(source_iterator)
            self.assertSequenceEqual(self.expected_file_headers, csv.headers())
            rows = list(itertools.islice(csv.reader(), 50))
            self.assertEqual(9, len(rows))
            self.assertEqual("What?", rows[8][3])  # just a spot check

    def test_csv_with_headers_sniff_dialect_use_headers(self):
        expected_headers = ["Date", "Sender", "Recipient", "Subject Line", "Number of Replies"]
        with open(self.csv_data_with_headers) as source_iterator:
            csv = CsvDataset(
                source_iterator,
                use_headers=expected_headers.copy()
            )
            self.assertSequenceEqual(
                expected_headers,
                csv.headers()
            )
            rows = list(itertools.islice(csv.reader(), 50))
            # we specifically did not tell the CsvDataset to skip the first row.
            # if we provide a header, and we don't want the existing header to be used, we need to
            # tell it to not use that top row!
            self.assertEqual(10, len(rows))
            self.assertEqual("What?", rows[9][3])  # just a spot check

    def test_csv_without_headers_sniff_dialect_sniff_headers(self):
        with open(self.csv_data_without_headers) as source_iterator:
            csv = CsvDataset(source_iterator)
            self.assertSequenceEqual(
                ["Attribute 0", "Attribute 1", "Attribute 2", "Attribute 3", "Attribute 4"],
                csv.headers()
            )
            rows = list(itertools.islice(csv.reader(), 50))
            self.assertEqual(9, len(rows))
            self.assertEqual("What?", rows[8][3])  # just a spot check

    def test_csv_without_headers_sniff_dialect_use_headers(self):
        expected_headers = ["Date", "Sender", "Recipient", "Subject Line", "Number of Replies"]
        with open(self.csv_data_with_headers) as source_iterator:
            csv = CsvDataset(
                source_iterator,
                has_headers=True,
                use_headers=expected_headers.copy()
            )
            self.assertSequenceEqual(
                expected_headers,
                csv.headers()
            )
            rows = list(itertools.islice(csv.reader(), 50))
            self.assertEqual(9, len(rows))
            self.assertEqual("What?", rows[8][3])  # just a spot check

    def test_tsv_with_headers_use_dialect(self):
        with open(self.tsv_data_with_headers) as source_iterator:
            csv = CsvDataset(
                source_iterator,
                has_headers=True,
                dialect="excel-tab"
            )
            self.assertSequenceEqual(self.expected_file_headers, csv.headers())
            rows = list(itertools.islice(csv.reader(), 50))
            self.assertEqual(9, len(rows))
            self.assertEqual("What?", rows[8][3])  # just a spot check

    def test_tsv_with_headers_use_dialect_object(self):
        with open(self.tsv_data_with_headers) as source_iterator:
            csv = CsvDataset(
                source_iterator,
                has_headers=True,
                dialect=csv_import.excel_tab()
            )
            self.assertSequenceEqual(self.expected_file_headers, csv.headers())
            rows = list(itertools.islice(csv.reader(), 50))
            self.assertEqual(9, len(rows))
            self.assertEqual("What?", rows[8][3])  # just a spot check

    def test_tsv_with_headers_sniff_dialect(self):
        with open(self.tsv_data_with_headers) as source_iterator:
            csv = CsvDataset(source_iterator)
            self.assertSequenceEqual(self.expected_file_headers, csv.headers())
            rows = list(itertools.islice(csv.reader(), 50))
            self.assertEqual(9, len(rows))
            self.assertEqual("What?", rows[8][3])  # just a spot check

    def test_networkx_cleaning(self):
        with open(data_file("octothorpes.csv")) as source_iterator:
            csv = CsvDataset(source_iterator, has_headers=True, dialect="excel")

            self.assertSequenceEqual(["column1", "column2", "column3", "column4"], csv.headers())
            rows = list(itertools.islice(csv.reader(), 50))
            self.assertEqual(1, len(rows))
            self.assertSequenceEqual(["field1", "field2", "field3", "field4"], rows[0])

    def test_long_fields(self):
        with open(data_file("super-long-fields.tsv")) as source_iterator:
            csv = CsvDataset(source_iterator, has_headers=True, dialect="excel-tab")
            self.assertEqual(655350, len(next(csv.reader())[3]))
