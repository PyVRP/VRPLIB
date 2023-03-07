from typing import Dict, List, Union

import numpy as np

from .parse_distances import pairwise_euclidean
from .parse_utils import text2lines

Instance = Dict[str, Union[str, float, np.ndarray]]


def parse_solomon(text: str) -> Instance:
    """
    Parses the text of a Solomon VRPTW instance.

    Parameters
    ----------
    text
        The instance text.

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
    instance["edge_weight"] = pairwise_euclidean(instance["node_coord"])

    return instance


def is_valid_solomon_instance(lines: List[str]):
    """
    Checks if the passed-in lines follow the Solomon format requirements.
    """
    BASE = "Instance does not conform to the Solomon format. "
    MSG = BASE + "Expected {desired}, got {actual}."

    desired = "VEHICLE"
    if lines[1] != desired:
        raise RuntimeError(MSG.format(actual=lines[1], desired=desired))

    desired = "NUMBER CAPACITY"
    if lines[2].split() != desired.split():
        raise RuntimeError(MSG.format(actual=lines[2], desired=desired))

    # TODO Validate that lines[3] contains the num vehicles and capacity

    desired = "CUSTOMER"
    if lines[4] != desired:
        raise RuntimeError(MSG.format(actual=lines[4], desired=desired))

    # TODO Validate that lines[5] are data headers
