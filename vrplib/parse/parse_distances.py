import numpy as np


def parse_distances(
    data: list[float],
    edge_weight_type: str,
    edge_weight_format: str | None = None,
    node_coord: np.ndarray | None = None,
    comment: str | None = None,
    **kwargs: float | str | np.ndarray,
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

        if edge_weight_type == "CEIL_2D":
            return np.ceil(distance)

    if edge_weight_type == "EXPLICIT":
        if edge_weight_format == "LOWER_ROW":
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
    coords = np.atleast_2d(coords)

    sq_sum = (coords**2).sum(axis=1)
    sq_dist = np.add.outer(sq_sum, sq_sum) - 2 * (coords @ coords.T)
    np.fill_diagonal(sq_dist, 0)  # avoids minor numerical issues

    return np.sqrt(sq_dist)


def from_lower_row(data: np.ndarray) -> np.ndarray:
    """
    Computes a full distances matrix from a LOWER_ROW edge weight section.

    The input is treated as a continuous 1D stream of values (as specified
    by TSPLIB95), regardless of how the values are wrapped across lines.

    Parameters
    ----------
    data
        Edge weight data, possibly as a ragged array of rows.

    Returns
    -------
    np.ndarray
        An n-by-n distances matrix.
    """
    flattened = np.concatenate(data).astype(float)

    # The flattened data represents the lower triangle of a symmetric matrix.
    # See https://en.wikipedia.org/wiki/Triangular_number.
    # m = n * (n - 1) / 2 => n = (1 + sqrt(1 + 8m)) / 2
    n = (1 + int((1 + 8 * flattened.size) ** 0.5)) // 2

    distances = np.zeros((n, n))
    distances[np.tril_indices(n, k=-1)] = flattened
    distances += distances.T

    return distances
