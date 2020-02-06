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


def kmeans_with_bic(
        embedding: np.ndarray,
        max_clusters: int = 2,
        min_clusters: int = 1,
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
    Performs kmeans clustering on the embedding. Will approximate the number of components using
    a binary search; the embedding will be fitted log(n) times and the n_components that minimize BIC will be
    chosen.

    :param numpy.ndarray embedding: An n x d array of vectors representing n labels in a d dimensional space
    :param int max_clusters: The maximum number of clusters, default 2
    :param int min_clusters: The minimum number of clusters, default 1
    :param init: Method for initialization, defaults to 'k-means++':

        'k-means++' : selects initial cluster centers for k-mean
        clustering in a smart way to speed up convergence.

        'random': choose k observations (rows) at random from data for
        the initial centroids.

        If an ndarray is passed, it should be of shape (n_clusters, n_features)
        and gives the initial centers.
    :type init: Union[str, np.ndarray]
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
    :rtype: np.ndarray
    """
    clusters = _kmeans_find_optimal_number_of_components_log(embedding,
                                                             max_clusters,
                                                             min_clusters,
                                                             init,
                                                             n_init,
                                                             max_iter,
                                                             tolerance,
                                                             precompute_distances,
                                                             verbose,
                                                             random_state,
                                                             copy_x,
                                                             n_jobs,
                                                             algorithm)
    classifier = KMeans(
        n_clusters=clusters,
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


def kmeans_with_bic_linear(
        embedding: np.ndarray,
        max_clusters: int = 2,
        min_clusters: int = 1,
        step: int = 1,
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
    Performs kmeans clustering on the embedding. Will approximate the number of clusters using
    a linear search. This will take significantly longer than the binary search implementation. A step has been
    provided that is used as a skip during the linear search of bic.

    For example, if max_clusters = 6, min_clusters = 1,
    and step = 1, then the embedding will be fitted exactly 6 times and the number of clusters that minimize BIC
    will be chosen. If max_clusters = 6, min_clusters = 1 and step = 2, then fitting will occur exactly 3 times, at
    num_clusters = 1, num_clusters = 3, and num_clusters = 5.


    :param numpy.ndarray embedding: An n x d array of vectors representing n labels in a d dimensional space
    :param int max_clusters: The maximum number of clusters, default 2
    :param int min_clusters: The minimum number of clusters, default 1
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
    :rtype: np.ndarray
    """
    clusters = _kmeans_find_optimal_number_of_components_linear(
        embedding,
        max_clusters,
        min_clusters,
        step,
        init,
        n_init,
        max_iter,
        tolerance,
        precompute_distances,
        verbose,
        random_state,
        copy_x,
        n_jobs,
        algorithm
    )

    classifier = KMeans(
        n_clusters=clusters,
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


def _kmeans_find_optimal_number_of_components_linear(
        feature_matrix,
        max_clusters,
        min_clusters,
        step,
        init,
        n_init,
        max_iter,
        tol,
        precompute_distances,
        verbose,
        random_state,
        copy_x,
        n_jobs,
        algorithm
):
    max_score_index, max_score_so_far = 0, 0
    i = min_clusters

    while i < max_clusters:
        classifier = KMeans(
            n_clusters=i,
            init=init,
            n_init=n_init,
            max_iter=max_iter,
            tol=tol,
            precompute_distances=precompute_distances,
            verbose=verbose,
            random_state=random_state,
            copy_x=copy_x,
            n_jobs=n_jobs,
            algorithm=algorithm
        )
        classifier.fit(feature_matrix)
        current_score = -classifier.score(feature_matrix)

        if current_score > max_score_so_far:
            max_score_so_far = current_score
            max_score_index = i

        i += step

    return max_score_index


def _kmeans_find_optimal_number_of_components_log(
        feature_matrix,
        max_clusters,
        min_clusters,
        init,
        n_init,
        max_iter,
        tol,
        precompute_distances,
        verbose,
        random_state,
        copy_x,
        n_jobs,
        algorithm
):
    max_score_index = 0
    max_score_so_far = 0
    start, end = min_clusters, max_clusters

    while start <= end:
        mid = (start + end) // 2

        classifier = KMeans(
            n_clusters=start,
            init=init,
            n_init=n_init,
            max_iter=max_iter,
            tol=tol,
            precompute_distances=precompute_distances,
            verbose=verbose,
            random_state=random_state,
            copy_x=copy_x,
            n_jobs=n_jobs,
            algorithm=algorithm
        )
        classifier.fit(feature_matrix)
        start_score = -classifier.score(feature_matrix)

        classifier = KMeans(
            n_clusters=mid,
            init=init,
            n_init=n_init,
            max_iter=max_iter,
            tol=tol,
            precompute_distances=precompute_distances,
            verbose=verbose,
            random_state=random_state,
            copy_x=copy_x,
            n_jobs=n_jobs,
            algorithm=algorithm
        )
        classifier.fit(feature_matrix)
        mid_score = -classifier.score(feature_matrix)

        classifier = KMeans(
            n_clusters=end,
            init=init,
            n_init=n_init,
            max_iter=max_iter,
            tol=tol,
            precompute_distances=precompute_distances,
            verbose=verbose,
            random_state=random_state,
            copy_x=copy_x,
            n_jobs=n_jobs,
            algorithm=algorithm
        )
        classifier.fit(feature_matrix)
        end_score = -classifier.score(feature_matrix)

        if mid_score > max_score_so_far:
            max_score_so_far = mid_score
            max_score_index = mid

        if mid_score > start_score:
            start = mid
        elif mid_score > end_score:
            end = mid
        else:
            start += 1

    return max_score_index
