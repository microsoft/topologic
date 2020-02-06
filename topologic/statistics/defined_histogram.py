# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import NamedTuple
import numpy as np


class DefinedHistogram(NamedTuple):
    """
    Contains the histogram and the edges of the bins in the histogram.

    The bin_edges will have a length 1 greater than the histogram, as it defines the minimal and maximal edges as well
    as each edge in between.
    """
    histogram: np.ndarray
    bin_edges: np.ndarray
