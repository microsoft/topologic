# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from sklearn.metrics.cluster import adjusted_rand_score
from typing import Any, Dict
import numpy as np

__all__ = ["ari"]


def ari(
    primary_partition: Dict[Any, int],
    test_partition: Dict[Any, int],
) -> float:
    """
    Given two partition schemas, a primary partition mapping (the most accurate representation of truth) and the test
    partition mapping (to be scored against that accurate representation of truth), calculate the Adjusted Rand Index.

    See https://en.wikipedia.org/wiki/Rand_index

    :param Dict[Any, int] primary_partition: The most accurate representation of truth for cluster or community
        membership of nodes. The keys are vertex labels and the values are the cluster/community/partition labels.
    :param Dict[Any, int] test_partition: The partition mapping to compare against the primary partition. The keys are
        vertex labels and the values are the cluster/community/partition labels.
    :return: The adjusted rand index for the two mappings
    :rtype float:
    :raises ValueError: If the primary partition and test partition do not have an identical vertex label set.
    """
    if primary_partition.keys() != test_partition.keys():
        raise ValueError("The reference partition provided does not contain the exact same keys as the predicted "
                         "clusters; an ari score cannot be generated automatically.")

    size = len(primary_partition.keys())
    primary = np.empty(size, dtype=int)
    test = np.empty(size, dtype=int)
    for i, vertex in enumerate(primary_partition.keys()):
        primary[i] = primary_partition[vertex]
        test[i] = test_partition[vertex]

    return adjusted_rand_score(labels_true=primary, labels_pred=test)
