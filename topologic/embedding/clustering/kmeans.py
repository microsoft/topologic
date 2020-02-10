# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import numpy as np
from sklearn.cluster import KMeans
from typing import Union


def kmeans(
        embedding: np.ndarray,
        n_clusters: int = 1,
        init: Union[str, np.ndarray] = 'k-means++',
        n_init: int = 10,
        max_iter: int = 300,
        tolerance: float = 0.0001,
        precompute_distances='auto',
        verbose: int = 0,
        random_state: int = None,
        copy_x: bool = True,
        n_jobs: int = None,
        algorithm: str = 'auto'
) -> np.ndarray:
    """
    Performs kmeans clustering on the embedding.

    :param numpy.ndarray embedding: An n x d array of vectors representing n labels in a d dimensional space
    :param int n_clusters: The number of clusters to form as well as the number of
        centroids to generate. Default 1
    :param init: Method for initialization, defaults to 'k-means++':

        'k-means++' : selects initial cluster centers for k-mean
        clustering in a smart way to speed up convergence.

        'random': choose k observations (rows) at random from data for
        the initial centroids.

        If an ndarray is passed, it should be of shape (n_clusters, n_features)
        and gives the initial centers.
    :type init: Union[str, numpy.ndarray]
    :param int n_init: Number of time the k-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of inertia. Default 10
    :param int max_iter: Maximum number of iterations of the k-means algorithm for a
        single run. Default 300
    :param float tolerance: Relative tolerance with regards to inertia to declare convergence. Default 1e-4
    :param precompute_distances: Precompute distances (faster but takes more memory).

        'auto' : do not precompute distances if n_samples * n_clusters > 12
        million. This corresponds to about 100MB overhead per job using
        double precision.

        True : always precompute distances

        False : never precompute distances
    :type precompute_distances: Union[bool, str]
    :param int verbose: Verbosity mode. Default 0
    :param random_state: Determines random number generation for centroid
        initialization. Use an int to make the randomness deterministic.
    :type random_state: Optional[Union[int, numpy.random.RandomState]]
    :param Optional[bool] copy_x: When pre-computing distances it is more numerically accurate to center
        the data first.  If copy_x is True (default), then the original data is
        not modified, ensuring X is C-contiguous.  If False, the original data
        is modified, and put back before the function returns, but small
        numerical differences may be introduced by subtracting and then adding
        the data mean, in this case it will also not ensure that data is
        C-contiguous which may cause a significant slowdown.
    :param Optional[int] n_jobs: The number of jobs to use for the computation. This works by computing
        each of the n_init runs in parallel.

        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors.
    :param str algorithm: K-means algorithm to use. The classical EM-style algorithm is "full".
        The "elkan" variation is more efficient by using the triangle
        inequality, but currently doesn't support sparse data. "auto" chooses
        "elkan" for dense data and "full" for sparse data.
    :return:  The cluster labels for each vector in the given embedding. The vector at index n in the embedding will
        have the label at index n in this returned array
    :rtype: numpy.ndarray
    """
    classifier = KMeans(
        n_clusters=n_clusters,
        init=init,
        n_init=n_init,
        max_iter=max_iter,
        tol=tolerance,
        precompute_distances=precompute_distances,
        verbose=verbose,
        random_state=random_state,
        copy_x=copy_x,
        n_jobs=n_jobs,
        algorithm=algorithm
    )

    classifier.fit(embedding)

    return classifier.predict(embedding)
