# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import numpy as np
import logging
from typing import Union
from sklearn.decomposition import PCA


def pca(
        embedding: np.ndarray,
        num_components: Union[str, int],
        whiten: bool = False,
        svd_solver: str = 'auto',
        tolerance: float = 0.0,
        iterated_power: Union[int, str] = 'auto',
        random_state: Union[int, np.random.RandomState, None] = None
) -> np.ndarray:
    """
    Principal component analysis (PCA)

    Linear dimensionality reduction using Singular Value Decomposition of the data to project it to a lower dimensional
    space.

    It uses the LAPACK implementation of the full SVD or a randomized truncated SVD by the method of Halko et al. 2009,
    depending on the shape of the input data and the number of components to extract.

    :param numpy.ndarray embedding: The embedding in which PCA will be applied
    :param num_components: If ``num_components == 'mle'`` and ``svd_solver == 'full'``, Minka's
        MLE is used to guess the dimension. Use of ``num_components == 'mle'``
        will interpret ``svd_solver == 'auto'`` as ``svd_solver == 'full'``.

        If ``0 < num_components < 1`` and ``svd_solver == 'full'``, select the
        number of components such that the amount of variance that needs to be
        explained is greater than the percentage specified by num_components.

        If ``svd_solver == 'arpack'``, the number of components must be
        strictly less than the minimum of number of features and the number of samples.
    :type num_components: Union[str, int]
    :param bool whiten: When True (False by default) the `components_` vectors are multiplied
        by the square root of n_samples and then divided by the singular values
        to ensure uncorrelated outputs with unit component-wise variances.

        Whitening will remove some information from the transformed signal
        (the relative variance scales of the components) but can sometime
        improve the predictive accuracy of the downstream estimators by
        making their data respect some hard-wired assumptions.
    :param str svd_solver:
        auto :
            the solver is selected by a default policy based on `X.shape` and
            `num_components`: if the input data is larger than 500x500 and the
            number of components to extract is lower than 80% of the smallest
            dimension of the data, then the more efficient 'randomized'
            method is enabled. Otherwise the exact full SVD is computed and
            optionally truncated afterwards.
        full :
            run exact full SVD calling the standard LAPACK solver via
            `scipy.linalg.svd` and select the components by postprocessing
        arpack :
            run SVD truncated to num_components calling ARPACK solver via
            `scipy.sparse.linalg.svds`. It requires strictly
            0 < num_components < min(X.shape)
        randomized :
            run randomized SVD by the method of Halko et al.
    :param float tolerance: Tolerance for singular values computed by svd_solver == 'arpack'. A float value >=0 with
        default 0
    :param iterated_power: Number of iterations for the power method computed by
        svd_solver == 'randomized'.
    :type iterated_power: Union[int, str]
    :param Optional[int] random_state: If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`. Used when ``svd_solver`` == 'arpack' or 'randomized'.
    :return: A np.ndarray of principal axes in feature space, representing the directions of
        maximum variance in the data. The components are sorted by variance`
    :rtype: numpy.ndarray
    """
    if embedding is None:
        raise ValueError('embedding must be specified but was None')
    if not num_components:
        raise ValueError('num_components must be specified but was None')

    logger = logging.getLogger(__name__)

    model = PCA(
        n_components=num_components,
        whiten=whiten,
        svd_solver=svd_solver,
        tol=tolerance,
        iterated_power=iterated_power,
        random_state=random_state
    )

    logger.info('Fitting the embedding')

    model.fit(embedding)

    logger.info(f"Explained variance for PCA embedding is {model.explained_variance_}")
    logger.info('Performing dimensionality reduction')

    return model.transform(embedding)
