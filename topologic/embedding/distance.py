# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from scipy import spatial
import numpy as np
from typing import Callable, KeysView, Union
from . import EmbeddingContainer


__all__ = [
    "cosine",
    "euclidean",
    "mahalanobis",
    "valid_distance_functions",
    "vector_distance",
    "embedding_distances_from"
]


def cosine(first_vector: np.ndarray, second_vector: np.ndarray) -> float:
    """
    Distance function for two vectors of equal length.    
    
    `Cosine distance <https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.cosine.html>`_    
    
    See also: https://en.wikipedia.org/wiki/Cosine_similarity
    
    :param numpy.ndarray first_vector: nonzero vector.  must be same length as second_vector
    :param numpy.ndarray second_vector: nonzero vector.  must be same length as first_vector
    :return: cosine distance - Resulting range is between 0 and 2.  Values closer to 0 are more similar.  Values closer
        to 2 are approaching total dissimilarity.
    :rtype: float
    :examples:
        >>> cosine(np.array([1,3,5]), np.array([2,3,4]))        
        0.026964528109766017
    
    """  # noqa:501
    return spatial.distance.cosine(first_vector, second_vector)


def euclidean(first_vector: np.ndarray, second_vector: np.ndarray) -> float:
    """
    Distance function for two vectors of equal length    
     
    `Euclidean distance <https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.euclidean.html>`_    
    
    See also: https://en.wikipedia.org/wiki/Euclidean_distance
    
    :param numpy.ndarray first_vector: nonzero vector.  must be same length as second_vector
    :param numpy.ndarray second_vector: nonzero vector.  must be same length as first_vector
    :return: euclidean distance - Resulting range is a positive real number.  Values closer to 0 are more similar.
    :rtype: float
    :examples:
        >>> euclidean(np.array([1,3,5]), np.array([2,3,4]))    
        1.4142135623730951
    
    """  # noqa:501
    return spatial.distance.euclidean(first_vector, second_vector)


def mahalanobis(inverse_covariance: np.ndarray) -> Callable[[np.ndarray, np.ndarray], float]:
    """
    Unlike cosine and euclidean distances which scipy provides that take in only two vectors, mahalanobis also
    requires an inverse covariance matrix. This function can be used but first this matrix must be provided and a
    curried function handler returned, which can then be passed in to the `vector_distance` and
    `embedding_distances_from` functions.

    See: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.mahalanobis.html

    :param np.ndarray inverse_covariance: The inverse covariance matrix
    :return: A curried function that now takes in 2 vectors and determines distance based on the inverse_covariance
        provided.
    """
    def _mahalanobis(first_vector: np.ndarray, second_vector: np.ndarray) -> float:
        return spatial.distance.mahalanobis(first_vector, second_vector, inverse_covariance)
    return _mahalanobis


_valid_distance_functions = {
    "cosine": cosine,
    "euclidean": euclidean
}


def valid_distance_functions() -> KeysView[str]:
    """
    The topologic builtin list of valid distance functions. Any function that return a float when given two
    np.ndarray 1d vectors is a valid choice, but the only ones we support without any other work are cosine or
    euclidean.

    :return: A set-like view of the string names of the functions we support
    """
    return _valid_distance_functions.keys()


def _distance_function(
    method: Union[str, Callable[[np.ndarray, np.ndarray], float]]
) -> Callable[[np.ndarray, np.ndarray], float]:
    if isinstance(method, str):
        if method not in valid_distance_functions():
            raise ValueError(
                f"Method {method} not in list of valid distance functions: {valid_distance_functions()}"
            )
        return _valid_distance_functions[method]
    else:
        return method


def vector_distance(
    first_vector: np.ndarray,
    second_vector: np.ndarray,
    method: Union[str, Callable[[np.ndarray, np.ndarray], float]] = cosine
) -> float:
    """
    Vector distance is a function that will do any distance function you would like on two vectors. This is most
    commonly used by changing the method parameter, as a string, from "cosine" to "euclidean" - allowing you to change
    your flow based on configuration not on code changes to the actual cosine and euclidean functions.

    :param np.ndarray first_vector: A 1d array-like (list, tuple, np.array) that represents the first vector
    :param np.ndarray second_vector: A 1d array-like (list, tuple, np.array) that represents the second vector
    :param method: Method can be any distance function that takes in 2 parameters. It can also be the string mapping
        to that function (as described by valid_distance_functions()). Note that you can also provide other functions,
        such as `mahalanobis`, but they require more information than just the comparative vectors.
    :type method: Union[str, Callable[[np.ndarray, np.ndarray], float]]
    :return: A float indicating the distance between two vectors.
    """
    method = _distance_function(method)
    return method(first_vector, second_vector)


def embedding_distances_from(
    vector: np.ndarray,
    embedding: Union[EmbeddingContainer, np.ndarray],
    method: Union[str, Callable[[np.ndarray, np.ndarray], float]] = cosine
) -> np.ndarray:
    """
    This function will return a 1d np.ndarray of floats by doing a distance calculation from the given `vector` to each
    `vector` stored in the embedding (likely including itself).

    The distance calculation can be provided either as a function reference or a string representation mapped to
    the 2 standard distance functions we natively support.  The functions supported are cosine and euclidean, both of
    which are `scipy` implementations. There is also a mahalanobis generator function that can be used, but first you
    must provide it with the inverse covariance matrix necessary for the distance calculations to be performed.

    :param np.ndarray vector: A 1d array-like (list, tuple, np.array) that represents the vector to compare against
        every other vector in the embedding
    :param Union[EmbeddingContainer, np.ndarray] embedding: The embedding is either a 2d np array, where each row is
        a vector and the number of columns is identical to the length of the vector to compare against.
    :param method: Method can be any distance function that takes in 2 parameters. It can also be the string mapping
        to that function (as described by valid_distance_functions()). Note that you can also provide other functions,
        such as `mahalanobis`, but they require more information than just the comparative vectors.
    :type method: Union[str, Callable[[np.ndarray, np.ndarray], float]]
    :return: np.ndarray of dtype float the same length as the count of embedded vectors
    :examples:
        >>> vector = [0.3, 0.4, 0.5]
        >>> embedding = np.array([[0.3, 0.4, 0.5], [0.31, 0.44, 0.7]])
        >>> embedding_distances_from(vector, embedding, method="cosine") # using string version of method name
        array([0.        , 0.00861606])
        >>> embedding_distances_from(vector, embedding, method=euclidean) # using function handle
        array([0.        , 0.20420578])
    """
    method = _distance_function(method)

    if isinstance(embedding, EmbeddingContainer):
        embedding = embedding.embedding

    length = embedding.shape[0]
    scores = np.zeros(length, dtype=float)
    for i in range(0, length):
        distance = method(vector, embedding[i])
        scores[i] = distance
    return scores
