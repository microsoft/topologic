# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import numpy as np
import scipy.linalg as la
from typing import Tuple


def procrustes_error(
        target_matrix: np.ndarray,
        matrix_to_rotate: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Procrustes rotation rotates a matrix to maximum similarity with a target matrix minimizing sum of squared
    differences. Procrustes rotation is typically used in comparison of ordination results. It is particularly useful
    in comparing alternative solutions in multidimensional scaling.

    For more information:
    https://www.rdocumentation.org/packages/vegan/versions/2.4-2/topics/procrustes

    :param numpy.ndarray target_matrix: A matrix representing an embedding
    :param numpy.ndarray matrix_to_rotate: A matrix representing an embedding which will be rotated
    :return: The error which is the difference between the two matrices and the transformation matrix
    """
    dimension = min(target_matrix.shape[1], matrix_to_rotate.shape[1])
    reduced_target_matrix = target_matrix[:, :dimension]
    reduced_matrix_to_rotate = matrix_to_rotate[:, :dimension]

    tmp = np.dot(reduced_target_matrix.T, reduced_matrix_to_rotate)

    left_singular_vectors, eigenvalues, right_singular_vectors = la.svd(tmp)
    w = left_singular_vectors.dot(right_singular_vectors)
    error = la.norm(reduced_target_matrix.dot(w) - reduced_matrix_to_rotate)

    return error, w
