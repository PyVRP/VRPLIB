from typing import Dict, List, Union

import numpy as np

from .parse_distances import pairwise_euclidean
from .parse_utils import text2lines

Instance = Dict[str, Union[str, float, np.ndarray]]


def parse_solomon(text: str, compute_edge_weights: bool = True) -> Instance:
    """
    Parses the text of a Solomon VRPTW instance.

    Parameters
    ----------
    text
        The instance text.
    compute_edge_weights
        Whether to compute the edge weights from the node coordinates.
        Defaults to True.

    Returns
    -------
    The instance data as dictionary.
    """
    lines = text2lines(text)

    is_valid_solomon_instance(lines)

    instance: Instance = {"name": lines[0]}
    instance["vehicles"], instance["capacity"] = [
        int(num) for num in lines[3].split()
    ]

    data = np.genfromtxt(lines[6:], dtype=int)

    instance["node_coord"] = data[:, 1:3]
    instance["demand"] = data[:, 3]
    instance["time_window"] = data[:, 4:6]
    instance["service_time"] = data[:, 6]

    if compute_edge_weights:
        instance["edge_weight"] = pairwise_euclidean(instance["node_coord"])

    return instance


def is_valid_solomon_instance(lines: List[str]):
    """
    Checks if the passed-in lines follow the Solomon format requirements.
    """

    try:
        assert lines[0]  # non-empty first line
        assert "VEHICLE" in lines[1]
        assert "NUMBER" in lines[2]
        assert "CAPACITY" in lines[2]
        assert "CUSTOMER" in lines[4]

        # Header names are separated on whitespace because the spacing of
        # some Solomon instances is off.
        headers = [
            "CUST",
            "NO.",
            "XCOORD.",
            "YCOORD.",
            "DEMAND",
            "READY",
            "DUE",
            "DATE",
            "SERVICE",
            "TIME",
        ]
        for header in headers:
            assert header in lines[5]

    except (IndexError, ValueError, AssertionError) as err:
        msg = "Instance does not conform to the Solomon format."
        raise RuntimeError(msg) from err
