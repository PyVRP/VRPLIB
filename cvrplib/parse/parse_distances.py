from itertools import combinations
from typing import Any, Dict

import numpy as np

Instance = Dict[str, Any]


def parse_distances(instance: Instance) -> np.ndarray:
    """
    Parses the distances. The specification "edge_weight_type" describes how
    the distances should be parsed. The two main ways are to calculate the
    Euclidean distances using the the node coordinates or by parsing an
    explicit distance matrix.

    Parameters
    ----------
    instance
        The (partially) parsed instance. We assume that all VRPLIB
        specifications and data are already contained in ``instance``.

    Returns
    -------
    np.ndarray
        An n-by-n distances matrix.
    """
    edge_type = instance["edge_weight_type"]

    if "2D" in edge_type:  # Euclidean distance on node coordinates
        distance = pairwise_euclidean(instance["node_coord"])

        if edge_type == "EUC_2D":
            return np.round(distance)

        if edge_type == "FLOOR_2D":
            return np.floor(distance)

        if edge_type == "EXACT_2D":
            return distance

    if edge_type == "EXPLICIT":
        fmt = instance["edge_weight_format"]
        weights = instance["edge_weight"]
        dimension = instance["dimension"]

        if fmt == "LOWER_ROW":
            # The Eilon instances with are not correctly specified.
            if "Eilon" in instance["comment"].lower():
                return from_eilon(weights, n=dimension)
            else:
                return from_lower_row(weights)

        if fmt == "FULL_MATRIX":
            return np.array(instance["edge_weight"])

    raise ValueError("Edge weight type or format unknown.")


def pairwise_euclidean(coords: np.ndarray) -> np.ndarray:
    """
    Computes the pairwise Euclidean distances using the passed-in coordinates.

    Parameters
    ----------
    coords
        An n-by-2 array of location coordinates.

    Returns
    -------
    An n-by-n distance matrix.
    """
    n = len(coords)
    distances = np.zeros((n, n))

    for (i, j) in combinations(range(n), r=2):
        d_ij = np.linalg.norm(coords[i] - coords[j])
        distances[i, j] = d_ij
        distances[j, i] = d_ij

    return distances


def from_lower_row(triangular: np.ndarray) -> np.ndarray:
    """
    Computes a full distances matrix from a lower row triangular matrix.
    The triangular matrix does not contain the diagonal.
    """
    n = len(triangular) + 1
    distances = np.zeros((n, n))

    for j, i in combinations(range(n), r=2):
        t_ij = triangular[i - 1][j]
        distances[i, j] = t_ij
        distances[j, i] = t_ij

    return distances


def from_eilon(edge_weights: np.ndarray, n: int) -> np.ndarray:
    """
    Computes a full distances matrix from the Eilon instances with "LOWER_ROW"
    edge weight format. The specification is incorrect, instead the edge weight
    section needs to be parsed as a flattend, column-wise matrix.

    See https://github.com/leonlan/CVRPLIB/issues/40.
    """
    distances = np.zeros((n, n))

    flattened = [dist for row in edge_weights for dist in row]
    indices = sorted([(i, j) for (i, j) in combinations(range(n), r=2)])

    for idx, (i, j) in enumerate(indices):
        d_ij = flattened[idx]
        distances[i, j] = d_ij
        distances[j, i] = d_ij

    return distances
