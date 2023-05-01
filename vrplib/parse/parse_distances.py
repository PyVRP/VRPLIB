from itertools import combinations
from typing import List, Optional, Union

import numpy as np


def parse_distances(
    data: List,
    edge_weight_type: str,
    edge_weight_format: Optional[str] = None,
    node_coord: Optional[np.ndarray] = None,
    comment: Optional[str] = None,
    **kwargs: Union[float, str, np.ndarray],  # noqa
) -> np.ndarray:
    """
    Parses the distances. The specification "edge_weight_type" describes how
    the distances should be parsed. The two main ways are to calculate the
    Euclidean distances using the the node coordinates or by parsing an
    explicit distance matrix.

    Parameters
    ----------
    data
        The edge weight data.
    edge_weight_type
        The type of the edge weight data.
    edge_weight_format, optional
        The format of the edge weight data.
    node_coord, optional
        The customer location coordinates.
    comment, optional
        The comment specification in the instance.
    **kwargs, optional
        Optional keyword arguments.

    Returns
    -------
    np.ndarray
        An n-by-n distances matrix.
    """
    if "2D" in edge_weight_type:  # Euclidean distance on node coordinates
        if node_coord is None:
            msg = (
                "Cannot compute Euclidean distances because node coordinates "
                "are not provided."
            )
            raise ValueError(msg)

        distance = pairwise_euclidean(node_coord)

        if edge_weight_type == "EUC_2D":
            return distance

        if edge_weight_type == "FLOOR_2D":
            return np.floor(distance)

        if edge_weight_type == "EXACT_2D":
            return np.round(distance * 1000)

    if edge_weight_type == "EXPLICIT":
        if edge_weight_format == "LOWER_ROW":
            # TODO Eilon instances edge weight specifications are incorrect in
            # (C)VRPLIB format. Find a better way to identify Eilon instances.
            if comment is not None and "Eilon" in comment:
                return from_eilon(data)
            else:
                return from_lower_row(data)

        if edge_weight_format == "FULL_MATRIX":
            return np.array(data)

    raise ValueError("Edge weight type or format unknown.")


def pairwise_euclidean(coords: np.ndarray) -> np.ndarray:
    """
    Computes the pairwise Euclidean distance between the passed-in coordinates.

    Parameters
    ----------
    coords
        An n-by-2 array of location coordinates.

    Returns
    -------
    np.ndarray
        An n-by-n Euclidean distances matrix.

    """
    diff = coords[:, np.newaxis, :] - coords
    square_diff = diff**2
    square_dist = np.sum(square_diff, axis=-1)
    return np.sqrt(square_dist)


def from_lower_row(triangular: np.ndarray) -> np.ndarray:
    """
    Computes a full distances matrix from a lower row triangular matrix.
    The triangular matrix should not contain the diagonal.

    Parameters
    ----------
    triangular
        A list of lists, each list representing the entries of a row in a
        lower triangular matrix without diagonal entries.

    Returns
    -------
    np.ndarray
        A n-by-n distances matrix.
    """
    n = len(triangular) + 1
    distances = np.zeros((n, n))

    for i in range(n - 1):
        distances[i + 1, : i + 1] = triangular[i]

    return distances + distances.T


def from_eilon(edge_weights: np.ndarray) -> np.ndarray:
    """
    Computes a full distances matrix from the Eilon instances with "LOWER_ROW"
    edge weight format. The specification is incorrect, instead the edge weight
    section needs to be parsed as a flattend, column-wise triangular matrix.

    See https://github.com/leonlan/VRPLIB/issues/40.
    """
    flattened = [dist for row in edge_weights for dist in row]
    n = int((2 * len(flattened)) ** 0.5) + 1  # The (n+1)-th triangular number

    distances = np.zeros((n, n))
    indices = sorted([(i, j) for (i, j) in combinations(range(n), r=2)])

    for idx, (i, j) in enumerate(indices):
        d_ij = flattened[idx]
        distances[i, j] = d_ij
        distances[j, i] = d_ij

    return distances


def is_triangular_number(n):
    """
    Checks if n is a triangular number.
    """
    i = int((2 * n) ** 0.5)
    return i * (i + 1) == 2 * n
