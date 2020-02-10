# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import csv
import numpy as np
from typing import List, Tuple, Union


def tensor_projection_writer(
        embedding_file_path: str,
        label_file_path: str,
        vectors: np.ndarray,
        labels: Union[List[List[str]], List[str]],
        encoding: str = 'utf-8'
):
    """
    Writes an embedding and labels to a given vector file path and label file path in a form that Tensorboard embedding
    projector can read

    :param str embedding_file_path: Path that the embedding file will be written
    :param str label_file_path: Path that the label file will be written
    :param numpy.ndarray vectors: A embedding represented as a np.ndarray
    :param labels: A list of lists where each inner list is the data for a single row
        in the embedding or a list of strings where each string is the single label for that tensor. If you pass in a
        List[List[str]] you allow multiple labels for a single tensor.
    :type labels: Union[List[List[str]], List[str]]
    :param str encoding: The encoding used to write the file
    """
    # write vector file and label files separately
    np.savetxt(embedding_file_path, vectors, delimiter='\t', encoding=encoding)

    # per python docs newline='' must be specified, see: https://docs.python.org/3/library/csv.html footnotes
    with open(label_file_path, 'w+', encoding=encoding, newline='') as labels_file:
        csv_writer = csv.writer(labels_file, delimiter='\t')

        for label_line in labels:
            if isinstance(label_line, str):
                csv_writer.writerow([label_line])
            else:
                csv_writer.writerow(label_line)


def tensor_projection_reader(
        embedding_file_path: str,
        label_file_path: str
) -> Tuple[np.ndarray, List[List[str]]]:
    """
    Reads the embedding and labels stored at the given paths and returns an np.ndarray and list of labels

    :param str embedding_file_path: Path to the embedding file
    :param str label_file_path: Path to the labels file
    :return: An embedding and list of labels
    :rtype: (numpy.ndarray, List[List[str]])
    """
    embedding = np.loadtxt(embedding_file_path, delimiter='\t')

    labels: List[List[str]] = []
    with open(label_file_path) as f:
        csv_reader = csv.reader(f, delimiter='\t')
        for label_row in csv_reader:
            labels.append(label_row)

    return embedding, labels
