# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import numpy as np
from array import array
from sklearn.cluster import dbscan as sk_dbscan


def dbscan(
        embedding: np.ndarray,
        eps: float = 0.5,
        min_samples: int = 5,
        metric: str = 'minkowski',
        metric_params: dict = None,
        algorithm: str = 'auto',
        leaf_size: int = 30,
        p: float = 2,
        sample_weight: array = None,
        n_jobs: int = None
) -> np.ndarray:
    """
    Perform DBSCAN clustering from vector array or distance matrix.

    :param numpy.ndarray embedding: An n x d array of vectors representing n labels in a d dimensional space
    :param Optional[float] eps: The maximum distance between two samples for them to be considered as in the same
        neighborhood.
    :param Optional[int] min_samples: The number of samples (or total weight) in a neighborhood for a point to be
        considered as a core point. This includes the point itself.
    :param metric: The metric to use when calculating distance between instances in a feature
        array. If metric is a string or callable, it must be one of the options allowed by
        :func:`sklearn.metrics.pairwise_distances` for its metric parameter. If metric is "precomputed", X is assumed
        to be a distance matrix and must be square. X may be a sparse matrix, in which case only "nonzero" elements may
        be considered neighbors for DBSCAN.

        If metric is a callable function, it is called on each pair of instances (rows) and the resulting value
        recorded. The callable should take two arrays from X as input and return a value indicating the distance
        between them.
    :type metric: Union[str, Callable[[float, float], float]]
    :param Optional[dict] metric_params:  Additional keyword arguments for the metric function.
    :param Optional[str] algorithm: The algorithm to be used by the NearestNeighbors module
        to compute pointwise distances and find nearest neighbors.
        Potential values: {'auto', 'ball_tree', 'kd_tree', 'brute'}, optional
    :param Optional[int] leaf_size: Leaf size passed to BallTree or cKDTree. This can affect the speed
        of the construction and query, as well as the memory required
        to store the tree. The optimal value depends
        on the nature of the problem. Default 30
    :param Optional[float] p: The power of the Minkowski metric to be used to calculate distance
        between points. Default 2.0
    :param Optional[Array[int]] sample_weight: Weight of each sample, such that a sample with a weight of at least
        ``min_samples`` is by itself a core sample; a sample with negative
        weight may inhibit its eps-neighbor from being core.
        Note that weights are absolute, and default to 1.
    :param Optional[int] n_jobs: The number of parallel jobs to run for neighbors search.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors.
    :return:  The cluster labels for each vector in the given embedding. The vector at index n in the embedding will
        have the label at index n in this returned array. Noisy samples are given the value -1
    :rtype: np.ndarray
    """
    return sk_dbscan(
        X=embedding,
        eps=eps,
        min_samples=min_samples,
        metric=metric,
        metric_params=metric_params,
        algorithm=algorithm,
        leaf_size=leaf_size,
        p=p,
        sample_weight=sample_weight,
        n_jobs=n_jobs
    )[1]  # element at index 1 contains the labels
