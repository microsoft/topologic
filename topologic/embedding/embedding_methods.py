# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from enum import Enum


class EmbeddingMethod(Enum):
    """
    An enum to represent which embedding method to use when generating an Omnibus embedding
    """
    ADJACENCY_SPECTRAL_EMBEDDING = 0
    LAPLACIAN_SPECTRAL_EMBEDDING = 1
