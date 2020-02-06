# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import numpy as np
from typing import List, NamedTuple, Any


class EmbeddingContainer(NamedTuple):
    embedding: np.ndarray
    vertex_labels: List[Any]

    def to_dictionary(self):
        return dict(zip(self.vertex_labels, self.embedding))


class OutOfSampleEmbeddingContainer(NamedTuple):
    embedding: np.ndarray
    vertex_labels: List[Any]
    vertex_labels_failing_inference: List[Any]
    starting_index_of_oos_embedding: int
    u: np.ndarray
    sigma: np.ndarray

    def to_dictionary(self):
        return dict(zip(self.vertex_labels, self.embedding))
