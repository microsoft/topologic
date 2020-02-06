# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import numpy as np
from typing import Union
from sklearn.manifold import TSNE


def tsne(
        embedding: np.ndarray,
        num_components: int = 2,
        perplexity: float = 30.0,
        early_exaggeration: float = 12.0,
        learning_rate: float = 200.0,
        num_iterations: int = 1000,
        num_iterations_without_progress: int = 300,
        min_grad_norm: float = 1e-7,
        metric: str = "euclidean",
        init: str = "random",
        verbose: int = 1,
        random_state: Union[int, np.random.RandomState, None] = None,
        method: str = 'barnes_hut',
        angle: float = 0.5
) -> np.ndarray:
    """
    t-distributed Stochastic Neighbor Embedding.

    t-SNE is a tool to visualize high-dimensional data. It converts
    similarities between data points to joint probabilities and tries
    to minimize the Kullback-Leibler divergence between the joint
    probabilities of the low-dimensional embedding and the
    high-dimensional data. t-SNE has a cost function that is not convex,
    i.e. with different initializations we can get different results.

    It is highly recommended to use another dimensionality reduction
    method (e.g. PCA for dense data or TruncatedSVD for sparse data)
    to reduce the number of dimensions to a reasonable amount (e.g. 50)
    if the number of features is very high. This will suppress some
    noise and speed up the computation of pairwise distances between
    samples.

    :param numpy.ndarray embedding: The embedding in which PCA will be applied
    :param int num_components: Dimension of the embedded space. Default 2
    :param float perplexity: The perplexity is related to the number of nearest neighbors that
        is used in other manifold learning algorithms. Larger datasets
        usually require a larger perplexity. Consider selecting a value
        between 5 and 50. The choice is not extremely critical since t-SNE
        is quite insensitive to this parameter. Default 30.0
    :param float early_exaggeration: Controls how tight natural clusters in the original space are in
        the embedded space and how much space will be between them. For
        larger values, the space between natural clusters will be larger
        in the embedded space. Again, the choice of this parameter is not
        very critical. If the cost function increases during initial
        optimization, the early exaggeration factor or the learning rate
        might be too high. Default 12.0
    :param float learning_rate: The learning rate for t-SNE is usually in the range [10.0, 1000.0]. If
        the learning rate is too high, the data may look like a 'ball' with any
        point approximately equidistant from its nearest neighbours. If the
        learning rate is too low, most points may look compressed in a dense
        cloud with few outliers. If the cost function gets stuck in a bad local
        minimum increasing the learning rate may help. Default 200.0
    :param int num_iterations: Maximum number of iterations for the optimization. Should be at
        least 250. Default 1000
    :param int num_iterations_without_progress: Maximum number of iterations without progress before we abort the
        optimization, used after 250 initial iterations with early
        exaggeration. Note that progress is only checked every 50 iterations so
        this value is rounded to the next multiple of 50. Default 300
    :param float min_grad_norm: If the gradient norm is below this threshold, the optimization will
        be stopped. Default 1e-7
    :param metric: The metric to use when calculating distance between instances in a
        feature array. If metric is a string, it must be one of the options
        allowed by scipy.spatial.distance.pdist for its metric parameter, or
        a metric listed in pairwise.PAIRWISE_DISTANCE_FUNCTIONS.
        If metric is "precomputed", X is assumed to be a distance matrix.
        Alternatively, if metric is a callable function, it is called on each
        pair of instances (rows) and the resulting value recorded. The callable
        should take two arrays from X as input and return a value indicating
        the distance between them. The default is "euclidean" which is
        interpreted as squared euclidean distance. Default 'euclidean'
    :type metric: Union[str, Callable]
    :param init: Initialization of embedding. Possible options are 'random', 'pca',
        and a numpy array of shape (n_samples, num_components).
        PCA initialization cannot be used with precomputed distances and is
        usually more globally stable than random initialization. Default 'random'
    :type init: Union[string, numpy.ndarray]
    :param int verbose: Verbosity level. Default 1
    :param random_state: If int, random_state is the seed used by the random number
        generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.  Note that different initializations might result in
        different local minima of the cost function.
    :type random_state: Optional[Union[int, numpy.random.RandomState]]
    :param str method: By default the gradient calculation algorithm uses Barnes-Hut
        approximation running in O(NlogN) time. method='exact'
        will run on the slower, but exact, algorithm in O(N^2) time. The
        exact algorithm should be used when nearest-neighbor errors need
        to be better than 3%. However, the exact method cannot scale to
        millions of examples. Default 'barnes_hut'
    :param float angle: Only used if method='barnes_hut'
        This is the trade-off between speed and accuracy for Barnpcaes-Hut T-SNE.
        'angle' is the angular size (referred to as theta in [3]) of a distant
        node as measured from a point. If this size is below 'angle' then it is
        used as a summary node of all points contained within it.
        This method is not very sensitive to changes in this parameter
        in the range of 0.2 - 0.8. Angle less than 0.2 has quickly increasing
        computation time and angle greater 0.8 has quickly increasing error. Default 0.5
    :return: A np.ndarray of principal axes in feature space, representing the directions of
        maximum variance in the data. The components are sorted by variance`
    :rtype: numpy.ndarray
    """
    if embedding is None:
        raise ValueError('embedding must be specified but was None')
    if not num_components:
        raise ValueError('num_components must be specified but was None')

    model = TSNE(
        n_components=num_components,
        perplexity=perplexity,
        early_exaggeration=early_exaggeration,
        learning_rate=learning_rate,
        n_iter=num_iterations,
        n_iter_without_progress=num_iterations_without_progress,
        min_grad_norm=min_grad_norm,
        metric=metric,
        init=init,
        verbose=verbose,
        random_state=random_state,
        method=method,
        angle=angle
    )

    return model.fit_transform(embedding)
