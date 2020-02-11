topologic.partitioning package
==============================

.. automodule:: topologic.partitioning
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: louvain

.. function:: topologic.partitioning.louvain(graph: networkx.classes.graph.Graph, partition=Optional[Dict[Any, int]]=None, \
        weight: str='weight', resolution: float=1.0, randomize: Optional[bool]=None, random_state: Optional[Any]=None)

    This louvain function is an alias to the `community.best_partition <https://python-louvain.readthedocs.io/en/latest/api.html#community.best_partition>`_ function
    in the `python-louvain <https://github.com/taynaud/python-louvain>`_ library written by `Thomas Aynaud <https://github.com/taynaud>`_.

    :param networkx.Graph graph: the networkx graph which is decomposed
    :param partition: the algorithm will start using this partition of the nodes. It's a
        dictionary where keys are their nodes and values the communities
    :type partition: Optional[Dict[Any, int]]
    :param str weight_attribute: the key in graph to use as weight. Default to 'weight'
    :param float resolution: Will change the size of the communities, default to 1. represents the time described in
        "Laplacian Dynamics and Multiscale Modular Structure in Networks", R. Lambiotte, J.-C. Delvenne, M. Barahona
    :param Any random_state: If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.
    :return: The partition, with communities numbered from 0 to number of communities
    :rtype: Dict[Any, int]
    :raises: NetworkXError - If the graph is not Eulerian.

