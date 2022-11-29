import math
from itertools import combinations
from typing import Any, Callable, Dict, Optional

import numpy as np

Instance = Dict[str, Any]


def parse_distances(
    instance: Instance, distance_rounding: Optional[Callable] = None
) -> Dict[str, np.ndarray]:
    """
    Parses the distances. The specification "edge_weight_type" describes how
    the distances should be parsed. The two main ways are to calculate the
    Euclidean distances using the the node coordinates or by parsing an
    explicit distance matrix.

    instance
        The instance parsed so far. We assume that all VRPLIB specifications
        and data sections are already inside `instance`.
    distance_rounding
        A custom distance rounding function. The default is to follow the
        VRPLIB convention, see ... # TODO
    """
    edge_weight_type = instance["edge_weight_type"]

    if "2D" in edge_weight_type:  # Calculate using node coordinates
        if callable(distance_rounding):
            round_func = distance_rounding
        elif edge_weight_type == "FLOOR_2D":
            round_func = math.floor
        elif edge_weight_type == "EXACT_2D":
            round_func = lambda x: x  # noqa
        elif edge_weight_type == "EUC_2D":
            round_func = round
        else:
            raise ValueError(
                f"2D edge weight type {edge_weight_type} unknown."
            )

        return {"distances": euclidean(instance["node_coord"], round_func)}

    if edge_weight_type == "EXPLICIT":
        edge_weight_format = instance["edge_weight_format"]
        edge_weight = instance["edge_weight"]
        dimension = instance["dimension"]

        if edge_weight_format == "LOWER_ROW":
            lr_repr = get_representation(instance["edge_weight"], n=dimension)

            if lr_repr == "flattened":
                return {"distances": from_flattened(edge_weight, n=dimension)}
            elif lr_repr == "triangular":
                return {"distances": from_triangular(edge_weight)}
            else:
                raise ValueError(f"Lower row represention {lr_repr} unkown.")

        raise ValueError(f"Edge weight format {edge_weight_format} unknown.")

    raise ValueError(f"Edge weight type {edge_weight_type} unknown.")


def _identity(num):
    return num


def euclidean(
    coords: np.ndarray, round_func: Callable = _identity
) -> np.ndarray:
    """
    Computes the pairwise Euclidean distances using the passed-in coordinates.
    `round_func` specifies how to round the computed distances.

    coords
        An n-by-2 array of location coordinates.
    round_func
        A rounding function. Default is the identity function.
    """
    n = len(coords)
    distances = np.zeros((n, n))

    for (i, j) in combinations(range(n), r=2):
        d_ij = round_func(np.linalg.norm(coords[i] - coords[j]))
        distances[i, j] = d_ij
        distances[j, i] = d_ij

    return distances


def get_representation(edge_weights: np.ndarray, n: int) -> str:
    """
    Returns the representation type in which the lower row data is given.
    This assumes that the instance has an explicit edge weight representation.
    In such a case, some instances have a flattened representation (e.g.,
    E-n13-k4), whereas others have a triangular one (e.g., ORTEC-n242-k12).


    Parameters
    ----------
    edge_weights
        The edge weights data.
    n
        The instance dimension.
    """
    if len(edge_weights) == n - 1:
        return "triangular"
    else:
        return "flattened"


def from_triangular(triangular: np.ndarray) -> np.ndarray:
    """
    Computes a full distances matrix from a triangular matrix.
    """
    n = len(triangular) + 1
    distances = np.zeros((n, n))

    for j, i in combinations(range(n), r=2):
        t_ij = triangular[i - 1][j]
        distances[i, j] = t_ij
        distances[j, i] = t_ij

    return distances


def from_flattened(edge_weights: np.ndarray, n: int) -> np.ndarray:
    """
    Computes a full distances matrix from a flattened lower row representation.

    The numbers in a flattened list correspond the matrix element indices
    (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), ...
    """
    distances = np.zeros((n, n))

    flattened = [dist for row in edge_weights for dist in row]
    indices = sorted([(i, j) for (j, i) in combinations(range(n), r=2)])

    for idx, (i, j) in enumerate(indices):
        d_ij = flattened[idx]
        distances[i, j] = d_ij
        distances[j, i] = d_ij

    return distances
