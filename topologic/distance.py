# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from scipy import spatial
import numpy


def cosine_distance(
        first_vector: numpy.ndarray,
        second_vector: numpy.ndarray
) -> float:
    """
    Distance function for two vectors of equal length.    
    
    Cosine distance: https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.cosine.html#scipy.spatial.distance.cosine    
    
    See also: https://en.wikipedia.org/wiki/Cosine_similarity
    
    :param numpy.ndarray first_vector: nonzero vector.  must be same length as second_vector
    :param numpy.ndarray second_vector: nonzero vector.  must be same length as first_vector
    :return: cosine distance - Resulting range is between 0 and 2.  Values closer to 0 are more similar.  Values closer
        to 2 are approaching total dissimilarity.
    :rtype: float
    :examples:
        >>> cosine_distance(numpy.array([1,3,5]), numpy.array([2,3,4]))        
        0.026964528109766017
    
    """  # noqa:501
    return spatial.distance.cosine(first_vector, second_vector)


def euclidean_distance(
        first_vector: numpy.ndarray,
        second_vector: numpy.ndarray
) -> float:
    """
    Distance function for two vectors of equal length    
     
    Euclidean distance: https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.euclidean.html#scipy.spatial.distance.euclidean    
    
    See also: https://en.wikipedia.org/wiki/Euclidean_distance
    
    :param numpy.ndarray first_vector: nonzero vector.  must be same length as second_vector
    :param numpy.ndarray second_vector: nonzero vector.  must be same length as first_vector
    :return: euclidean distance - Resulting range is a positive real number.  Values closer to 0 are more similar.
    :rtype: float
    :examples:
        >>> euclidean_distance(numpy.array([1,3,5]), numpy.array([2,3,4]))    
        1.4142135623730951
    
    """  # noqa:501
    return spatial.distance.euclidean(first_vector, second_vector)


def mahalanobis_distance(
        first_vector: numpy.ndarray,
        second_vector: numpy.ndarray,
        inverse_covariance_matrix: numpy.ndarray
) -> float:
    """
    Distance function for two vectors of equal length   
     
    Mahalanobis distance: https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.mahalanobis.html#scipy.spatial.distance.mahalanobis   
     
    See also: https://en.wikipedia.org/wiki/Mahalanobis_distance    
    
    See also: https://en.wikipedia.org/wiki/Covariance_matrix
    
    :param numpy.ndarray first_vector: nonzero vector.  must be same length as second_vector
    :param numpy.ndarray second_vector: nonzero vector.  must be same length as second_vector
    :param numpy.ndarray inverse_covariance_matrix:
    :return: mahalanobis distance - Resulting range is ____.  Values closer to ____ are more similar.
    :rtype: float
    :examples:
        >>> inverse_covariance = [[1, 0.5, 0.5], [0.5, 1, 0.5], [0.5, 0.5, 1]]
        >>> mahalanobis_distance([1, 0, 0], [0, 1, 0], inverse_covariance)
        1.0
    """  # noqa:501
    return spatial.distance.mahalanobis(first_vector, second_vector, inverse_covariance_matrix)
