# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import numpy as np
from sklearn.mixture import GaussianMixture


def gaussian_mixture_model(
        embedding: np.ndarray,
        num_clusters: int = 1,
        seed: int = None,
) -> np.ndarray:
    """
    Performs gaussian mixture model clustering on the feature_matrix.

    :param numpy.ndarray embedding: An n x d feature matrix; it is assumed that the d features are ordered
    :param int num_clusters: How many clusters to look at between min_clusters and max_clusters, default 1
    :param Optional[int] seed: The seed for numpy random, default None
    :return:  The cluster labels for each vector in the given embedding. The vector at index n in the embedding will
        have the label at index n in this returned array
    :rtype: np.ndarray
    """
    np.random.seed(seed)

    classifier = GaussianMixture(
        n_components=num_clusters,
        covariance_type='spherical'
    )
    classifier.fit(embedding)

    predictions = classifier.predict(embedding)
    predictions = np.array([int(i) for i in predictions])

    return predictions


def gaussian_mixture_model_with_bic(
        embedding: np.ndarray,
        max_clusters: int = 2,
        min_clusters: int = 1,
        seed: int = None
) -> np.ndarray:
    """
    Performs gaussian mixture model clustering on the feature_matrix. Will approximate the number of components using
    a binary search; the feature_matrix will be fitted log(n) times and the n_components that minimize BIC will be
    chosen.

    :param numpy.ndarray embedding: An n x d feature matrix; it is assumed that the d features are ordered
    :param int max_clusters: The maximum number of clusters, default 2
    :param int min_clusters: The minimum number of clusters, default 1
    :param Optional[int] seed: The seed for numpy random, default None
    :return:  The cluster labels for each vector in the given embedding. The vector at index n in the embedding will
        have the label at index n in this returned array
    :rtype: np.ndarray
    """
    _validate_arguments(max_clusters, min_clusters)

    np.random.seed(seed)

    height, width = embedding.shape

    max_clusters = int(max_clusters)
    min_clusters = int(min_clusters)

    if max_clusters < width:
        embedding = embedding[:, :max_clusters].copy()

    classifier = GaussianMixture(n_components=min_clusters, covariance_type='spherical')
    classifier.fit(embedding)

    number_of_likely_clusters = _gmm_find_optimal_number_of_components_log(embedding,
                                                                           max_clusters,
                                                                           min_clusters
                                                                           )

    classifier_with_ideal_bic = GaussianMixture(n_components=number_of_likely_clusters)
    classifier_with_ideal_bic.fit(embedding)

    predictions = classifier_with_ideal_bic.predict(embedding)
    predictions = np.array([int(i) for i in predictions])

    return predictions


def gaussian_mixture_model_with_bic_linear(
        embedding: np.ndarray,
        max_clusters: int = 2,
        min_clusters: int = 1,
        step: int = 1,
        seed: int = None
) -> np.ndarray:
    """
    Performs gaussian mixture model clustering on the embedding. Will approximate the number of components using
    a linear search. This will take significantly longer than the binary search implementation. A step has been provided
    that is used as a skip during the linear search of bic. For example, if max_clusters = 6, min_clusters = 1, and
    step = 1, then the feature_matrix will be fitted exactly 6 times and the number of clusters that minimize BIC will
    be chosen. If max_clusters = 6, min_clusters = 1 and step = 2, then fitting will occur exactly 3 times, at
    num_clusters = 1, num_clusters = 3, and num_clusters = 5.

    :param numpy.ndarray embedding: An n x d feature matrix; it is assumed that the d features are ordered
    :param int max_clusters: The maximum number of clusters, default 2
    :param int min_clusters: The minimum number of clusters, default 1
    :param Optional[int] seed: The seed for numpy random, default None
    :return:  The cluster labels for each vector in the given embedding. The vector at index n in the embedding will
        have the label at index n in this returned array
    :rtype: np.ndarray
    """
    _validate_arguments(max_clusters, min_clusters)

    np.random.seed(seed)

    height, width = embedding.shape

    max_clusters = int(max_clusters)
    min_clusters = int(min_clusters)

    if max_clusters < width:
        embedding = embedding[:, :max_clusters].copy()

    classifier = GaussianMixture(
        n_components=min_clusters,
        covariance_type='spherical')
    classifier.fit(embedding)

    number_of_likely_clusters = _gmm_find_optimal_number_of_components_linear(
        classifier,
        embedding,
        max_clusters,
        min_clusters,
        step
    )

    classifier_with_ideal_bic = GaussianMixture(n_components=number_of_likely_clusters)
    classifier_with_ideal_bic.fit(embedding)

    predictions = classifier_with_ideal_bic.predict(embedding)
    predictions = np.array([int(i) for i in predictions])

    return predictions


def _validate_arguments(max_clusters, min_clusters):
    if type(max_clusters) is not int:
        raise TypeError("max_clusters must be an int.")
    if type(min_clusters) is not int:
        raise TypeError("min_clusters must be an int.")
    if min_clusters > max_clusters:
        raise TypeError(f"min_clusters must be less than or equal to max_clusters. Min {min_clusters} Max "
                        f"{max_clusters}")


def _gmm_find_optimal_number_of_components_linear(
        classifier,
        feature_matrix,
        max_clusters,
        min_clusters,
        step
):
    max_bayesian_information_criteria = -classifier.bic(feature_matrix)
    cluster_likelihood_max = min_clusters

    for i in range(min_clusters, max_clusters, step):
        classifier = GaussianMixture(n_components=i)
        classifier.fit(feature_matrix)

        current_bic = -classifier.bic(feature_matrix)

        if current_bic > max_bayesian_information_criteria:
            max_bayesian_information_criteria = current_bic
            cluster_likelihood_max = i

    return cluster_likelihood_max


def _gmm_find_optimal_number_of_components_log(
        feature_matrix,
        max_clusters,
        min_clusters
):
    max_score_index = 0
    max_score_so_far = 0
    start, end = min_clusters, max_clusters

    while start <= end:
        mid = (start + end) // 2

        classifier = GaussianMixture(n_components=start)
        classifier.fit(feature_matrix)
        start_score = -classifier.bic(feature_matrix)

        classifier = GaussianMixture(n_components=mid)
        classifier.fit(feature_matrix)
        mid_score = -classifier.bic(feature_matrix)

        classifier = GaussianMixture(n_components=end)
        classifier.fit(feature_matrix)
        end_score = -classifier.bic(feature_matrix)

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
