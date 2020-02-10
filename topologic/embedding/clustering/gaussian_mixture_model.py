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
