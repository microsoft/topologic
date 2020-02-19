# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

# Adapted from Youngser Park.
# @references, Zhu, Mu and Ghodsi, Ali (2006), Automatic dimensionality selection
# from the scree plot via the use of profile likelihood,
# Computational Statistics & Data Analysis, Volume 51 Issue 2, pp 918-930, November, 2006

from typing import Union

import numpy as np
from scipy.stats import norm


def find_elbows(
        iterable_to_search: Union[list, np.array],
        num_elbows: int = 1,
        threshold: int = 0
) -> np.array:
    """
    An implementation of profile likelihood as outlined in Zhu and Ghodsi
    References, Zhu, Mu and Ghodsi, Ali (2006), Automatic dimensionality selection from the scree plot via the
    use of profile likelihood, Computational Statistics & Data Analysis, Volume 51 Issue 2, pp 918-930, November, 2006

    :examples:
        >>> input_data = [2, 3, 4, 5, 6, 7, 8, 9]
        >>> result: np.array = find_elbows(input_data, num_elbows=1, threshold=0)
        >>> result.size
        1

    :param iterable_to_search: An ordered or unordered list of values that will be used to find the elbows.
    :param num_elbows: The number of elbows to return
    :param threshold: Smallest value to consider.  Nonzero thresholds will affect elbow selection.
    :return: A numpy array containing elbows
    """
    iterable_copy = iterable_to_search.copy()

    if isinstance(iterable_copy, list):  # cast to array for functionality later
        iterable_copy = np.array(iterable_copy)

    if num_elbows == 0:  # nothing to do..
        return np.array([])

    if iterable_copy.ndim == 2:
        iterable_copy = np.std(iterable_copy, axis=0)

    # select values greater than the threshold
    iterable_copy = iterable_copy[iterable_copy > threshold]

    if len(iterable_copy) == 0:
        return np.array([])

    elbows = []

    if len(iterable_copy) == 1:
        elbows.append(iterable_copy[0])
        return np.array(elbows)

    iterable_copy.sort()
    iterable_copy = iterable_copy[::-1]  # reverse array so that it is sorted in descending order
    n = len(iterable_copy)

    while len(elbows) < num_elbows and len(iterable_copy) > 1:
        d = 1
        sample_var = np.var(iterable_copy, ddof=1)
        sample_scale = sample_var ** (1 / 2)
        elbow = 0
        likelihood_elbow = 0
        while d < len(iterable_copy):
            mean_sig = np.mean(iterable_copy[:d])
            mean_noise = np.mean(iterable_copy[d:])
            sig_likelihood = 0
            noise_likelihood = 0
            for i in range(d):
                sig_likelihood += norm.pdf(iterable_copy[i], mean_sig, sample_scale)
            for i in range(d, len(iterable_copy)):
                noise_likelihood += norm.pdf(iterable_copy[i], mean_noise, sample_scale)

            likelihood = noise_likelihood + sig_likelihood

            if likelihood > likelihood_elbow:
                likelihood_elbow = likelihood
                elbow = d
            d += 1
        if len(elbows) == 0:
            elbows.append(elbow)
        else:
            elbows.append(elbow + elbows[-1])
        iterable_copy = iterable_copy[elbow:]

    if len(elbows) == num_elbows:
        return np.array(elbows)

    if len(iterable_copy) == 0:
        return np.array(elbows)
    else:
        elbows.append(n)
        return np.array(elbows)
