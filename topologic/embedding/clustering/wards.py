# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import numpy as np
from sklearn.cluster import AgglomerativeClustering


def wards_clustering(
        embedding: np.ndarray,
        num_clusters: int = 2,
        affinity: str = 'euclidean',
        memory: str = None,
        connectivity: np.ndarray = None,
        compute_full_tree: str = 'auto'
) -> np.ndarray:
    """
    Uses agglomerative clustering with ward linkage

    Recursively merges the pair of clusters that minimally increases
    a given linkage distance.

    :param numpy.ndarray embedding: An n x d array of vectors representing n labels in a d dimensional space
    :param int num_clusters: int, default=2
        The number of clusters to find.
    :param str affinity: string or callable, default: "euclidean"
        Metric used to compute the linkage. Can be "euclidean", "l1", "l2",
        "manhattan", "cosine", or 'precomputed'.
        If linkage is "ward", only "euclidean" is accepted.
    :param memory: None, str or object with the joblib.Memory interface, optional
        Used to cache the output of the computation of the tree.
        By default, no caching is done. If a string is given, it is the
        path to the caching directory.
    :type memory: Optional[Union[str, joblib.Memory]]
    :param numpy.ndarray connectivity: array-like or callable, optional
        Connectivity matrix. Defines for each sample the neighboring
        samples following a given structure of the data.
        This can be a connectivity matrix itself or a callable that transforms
        the data into a connectivity matrix, such as derived from
        kneighbors_graph. Default is None, i.e, the
        hierarchical clustering algorithm is unstructured.
    :param Optional[str] compute_full_tree: bool or 'auto' (optional)
        Stop early the construction of the tree at n_clusters. This is
        useful to decrease computation time if the number of clusters is
        not small compared to the number of samples. This option is
        useful only when specifying a connectivity matrix. Note also that
        when varying the number of clusters and using caching, it may
        be advantageous to compute the full tree.
    :return:  The cluster labels for each vector in the given embedding. The vector at index n in the embedding will
        have the label at index n in this returned array
    :rtype: np.ndarray
    """
    agglomerative_cluster_model = _agglomerative_clustering(
        embedding,
        num_clusters=num_clusters,
        affinity=affinity,
        memory=memory,
        connectivity=connectivity,
        compute_full_tree=compute_full_tree,
        linkage='ward'
    )

    return agglomerative_cluster_model.labels_


def _agglomerative_clustering(
        embedding: np.ndarray,
        num_clusters: int = 2,
        affinity: str = 'euclidean',
        memory: str = None,
        connectivity: np.ndarray = None,
        compute_full_tree: str = 'auto',
        linkage: str = 'ward'
) -> np.ndarray:
    """
    Agglomerative Clustering

    Recursively merges the pair of clusters that minimally increases
    a given linkage distance.

    :param numpy.ndarray embedding: A feature matrix used to generate the model
    :param int num_clusters: int, default=2
        The number of clusters to find.
    :param str affinity: string or callable, default: "euclidean"
        Metric used to compute the linkage. Can be "euclidean", "l1", "l2",
        "manhattan", "cosine", or 'precomputed'.
        If linkage is "ward", only "euclidean" is accepted.
    :param memory: None, str or object with the joblib.Memory interface, optional
        Used to cache the output of the computation of the tree.
        By default, no caching is done. If a string is given, it is the
        path to the caching directory.
    :type memory: Optional[Union[str, joblib.Memory]]
    :param numpy.ndarray connectivity: array-like or callable, optional
        Connectivity matrix. Defines for each sample the neighboring
        samples following a given structure of the data.
        This can be a connectivity matrix itself or a callable that transforms
        the data into a connectivity matrix, such as derived from
        kneighbors_graph. Default is None, i.e, the
        hierarchical clustering algorithm is unstructured.
    :param Optional[str] compute_full_tree: bool or 'auto' (optional)
        Stop early the construction of the tree at n_clusters. This is
        useful to decrease computation time if the number of clusters is
        not small compared to the number of samples. This option is
        useful only when specifying a connectivity matrix. Note also that
        when varying the number of clusters and using caching, it may
        be advantageous to compute the full tree.
    :param str linkage: {"ward", "complete", "average", "single"}, optional (default="ward")
        Which linkage criterion to use. The linkage criterion determines which
        distance to use between sets of observation. The algorithm will merge
        the pairs of cluster that minimize this criterion.

        - ward minimizes the variance of the clusters being merged.
        - average uses the average of the distances of each observation of
          the two sets.
        - complete or maximum linkage uses the maximum distances between
          all observations of the two sets.
        - single uses the minimum of the distances between all observations
          of the two sets.
    :return: Model with attributes:
        labels_ : array [n_samples]
            cluster labels for each point

        n_leaves_ : int
            Number of leaves in the hierarchical tree.

        n_components_ : int
            The estimated number of connected components in the graph.

        children_ : array-like, shape (n_samples-1, 2)
            The children of each non-leaf node. Values less than `n_samples`
            correspond to leaves of the tree which are the original samples.
            A node `i` greater than or equal to `n_samples` is a non-leaf
            node and has children `children_[i - n_samples]`. Alternatively
            at the i-th iteration, children[i][0] and children[i][1]
            are merged to form node `n_samples + i`
    :rtype: Object with attributes labels, n_leaves, n_components, children
    """
    model = AgglomerativeClustering(
        n_clusters=num_clusters,
        affinity=affinity,
        memory=memory,
        connectivity=connectivity,
        compute_full_tree=compute_full_tree,
        linkage=linkage
    )

    model.fit(embedding)

    return model
