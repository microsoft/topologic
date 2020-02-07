# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import topologic.io as tc_io
import numpy as np
import tempfile
import unittest
from pathlib import Path
import os


class TestTensorProjectionWriter(unittest.TestCase):
    def test_tensor_projection_serialize_and_deserialize_with_temp_file(self):
        embedding_initial = np.random.rand(21, 50)

        with tempfile.TemporaryDirectory() as temp_directory:
            embedding_file_path = os.path.join(temp_directory, 'vectors.tsv')
            label_file_path = os.path.join(temp_directory, 'labels.tsv')

            tc_io.tensor_projection_writer(
                embedding_file_path,
                label_file_path,
                embedding_initial,
                [['test', 'test2', 'test3'], 'new line']
            )

            embedding_from_disk, labels_from_disk = tc_io.tensor_projection_reader(
                embedding_file_path,
                label_file_path
            )

            # Verify that the deserialized embedding is equivalent to the starting embedding
            np.testing.assert_array_equal(np.array(embedding_from_disk), embedding_initial)

            # Verify that the deserialized labels are equivalent to the starting labels
            self.assertEqual(len(labels_from_disk), 2)

            first_row = labels_from_disk[0]
            self.assertEqual(first_row[0], 'test')
            self.assertEqual(first_row[1], 'test2')
            self.assertEqual(first_row[2], 'test3')

            second_row = labels_from_disk[1]
            self.assertEqual(second_row[0], 'new line')
