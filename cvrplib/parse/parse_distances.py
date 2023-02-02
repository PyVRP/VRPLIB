from itertools import combinations
from typing import Any, Dict

import numpy as np

Instance = Dict[str, Any]


def parse_distances(instance: Instance) -> Dict[str, np.ndarray]:
    """
    Parses the distances. The specification "edge_weight_type" describes how
    the distances should be parsed. The two main ways are to calculate the
    Euclidean distances using the the node coordinates or by parsing an
    explicit distance matrix.

    Parameters
    ----------
    instance
        The (partially) parsed instance. We assume that all VRPLIB
        specifications and data are already stored in `instance`.

    Returns
    -------
    An n-by-n distances matrix.
    """
    edge_weight_type = instance["edge_weight_type"]

    if "2D" in edge_weight_type:  # Euclidean distance on node coordinates
        dists = pairwise_euclidean(instance["node_coord"])

        if edge_weight_type == "EUC_2D":
            dists = np.round(dists)
        elif edge_weight_type == "FLOOR_2D":
            dists = np.floor(dists)
        elif edge_weight_type == "EXACT_2D":
            pass
        else:
            raise ValueError(f"Edge weight type {edge_weight_type} unknown.")

        return {"distance": dists}

    if edge_weight_type == "EXPLICIT":
        edge_weight_format = instance["edge_weight_format"]
        edge_weight = instance["edge_weight"]
        dimension = instance["dimension"]

        if edge_weight_format == "LOWER_ROW":
            lr_repr = get_representation(instance["edge_weight"], n=dimension)

            if lr_repr == "flattened":
                return {"distance": from_flattened(edge_weight, n=dimension)}
            elif lr_repr == "triangular":
                return {"distance": from_triangular(edge_weight)}
            else:
                raise ValueError(f"Lower row represention {lr_repr} unkown.")

        if edge_weight_format == "FULL_MATRIX":
            return {"distance": np.array(instance["edge_weight"])}

        raise ValueError(f"Edge weight format {edge_weight_format} unknown.")

    raise ValueError(f"Edge weight type {edge_weight_type} unknown.")


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
