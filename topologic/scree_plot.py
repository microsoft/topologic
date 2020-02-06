# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

# Adapted from Youngser Park.
# @references, Zhu, Mu and Ghodsi, Ali (2006), Automatic dimensionality selection from the scree plot via the
# use of profile likelihood, Computational Statistics & Data Analysis, Volume 51 Issue 2, pp 918-930, November, 2006

import numpy as np
from typing import Union
from scipy.stats import norm


def find_elbows(eigenvalues: Union[list, np.array], elbow_count: int = 1, threshold: int = 0) -> np.array:
    """
    An implementation of profile likelihood as outlined in Zhu and Ghodsi
    References, Zhu, Mu and Ghodsi, Ali (2006), Automatic dimensionality selection from the scree plot via the
    use of profile likelihood, Computational Statistics & Data Analysis, Volume 51 Issue 2, pp 918-930, November, 2006

    :examples:
        >>> input_data = [2, 3, 4, 5, 6, 7, 8, 9]
        >>> result: np.array = find_elbows(input_data, elbow_count=1, threshold=0)
        >>> result.size
        1

    :param eigenvalues: An ordered or unordered list of eigenvalues
    :param elbow_count: The number of elbows to return
    :param threshold: Smallest value to consider.  Nonzero thresholds will affect elbow selection.
    :return: A numpy array containing elbows

    :
    """

    copied_data: np.array = None

    # cast to array for functionality later
    if type(eigenvalues) == list:
        copied_data = np.array(eigenvalues.copy())
    else:
        copied_data = eigenvalues.copy()

    if elbow_count == 0:  # nothing to do..
        return np.array([])

    # If copied_data is a 2-dimensional array
    if copied_data.ndim == 2:
        copied_data = np.std(copied_data, axis=0)

    # select values greater than the threshold
    copied_data = copied_data[copied_data > threshold]

    if len(copied_data) == 0:
        return np.array([])

    elbows = []

    if len(copied_data) == 1:
        elbows.append(copied_data[0])
        return np.array(elbows)

    # sort in reverse order.  Numpy arrays do not allow .sort(reverse=True)
    copied_data.sort()
    copied_data = copied_data[::-1]

    n = len(copied_data)

    while len(elbows) < elbow_count and len(copied_data) > 1:
        sample_var = np.var(copied_data, ddof=1)
        sample_scale = sample_var ** (1 / 2)
        elbow = 0
        likelihood_elbow = 0
        for d in range(1, len(copied_data)):
            mean_sig = np.mean(copied_data[:d])
            mean_noise = np.mean(copied_data[d:])
            sig_likelihood = 0
            noise_likelihood = 0
            for i in range(d):
                sig_likelihood += norm.pdf(copied_data[i], mean_sig, sample_scale)
            for i in range(d, len(copied_data)):
                noise_likelihood += norm.pdf(copied_data[i], mean_noise, sample_scale)

            likelihood = noise_likelihood + sig_likelihood

            if likelihood > likelihood_elbow:
                likelihood_elbow = likelihood
                elbow = d
        if len(elbows) == 0:
            elbows.append(elbow)
        else:
            elbows.append(elbow + elbows[-1])
        copied_data = copied_data[elbow:]

    if len(elbows) == elbow_count:
        return np.array(elbows)

    if len(copied_data) == 0:
        return np.array(elbows)
    else:
        elbows.append(n)
        return np.array(elbows)
